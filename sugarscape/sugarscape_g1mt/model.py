import numpy as np
import random

import mesa
from .trader_agents import Trader
from .resource_agents import Sugar, Spice


def fint(x: float, model):
    """
    Fuzzy integer funciton to add noise 
    in converting floats to integers
    """
    int_part = int(x)
    decimal_part = x - int_part
    if model.random.random() < decimal_part:
        return int_part + 1
    else:
        return int_part

# Helper Functions
def flatten(list_of_lists):
    """
    helper function for model datacollector for trade price
    collapses agent price list into one list
    """
    return [item for sublist in list_of_lists for item in sublist]


def geometric_mean(list_of_prices):
    """
    find the geometric mean of a list of prices
    """
    return np.exp(np.log(list_of_prices).mean())


def get_trade(agent):
    """
    For agent reporters in data collector

    return list of trade partners and None for other agents
    """
    if isinstance(agent, Trader):
        return agent.trade_partners
    else:
        return None

class SugarscapeG1mt(mesa.Model):
    """
    Manager class to run Sugarscape with Traders
    """

    def __init__(
        self,
        seed=None,
        h_e=0.5,
        h_m=0.5,
        h_v=0.5,
        max_steps=200,
        width=50,
        height=50,
        initial_population=500,
        endowment_min=25,
        endowment_max=50,
        metabolism_min=1,
        metabolism_max=5,
        vision_min=1,
        vision_max=5,
    ):
        self.max_steps = max_steps
        # Initialize heterogeneity parameters
        self.h_e = h_e
        self.h_m = h_m
        self.h_v = h_v

        # self.collect_data = collect_data
        # Initiate width and heigh of sugarscape
        self.width = width
        self.height = height
        # Initiate population attributes
        self.initial_population = initial_population
        self.endowment_min = endowment_min
        self.endowment_max = endowment_max
        self.metabolism_min = metabolism_min
        self.metabolism_max = metabolism_max
        self.vision_min = vision_min
        self.vision_max = vision_max

        self.running = True
        # random.seed(seed)

        # initiate activation schedule
        self.schedule = mesa.time.RandomActivationByType(self)
        # initiate mesa grid class
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=False)
        # initiate datacollector
        self.datacollector = mesa.DataCollector(
            model_reporters={
                # "Trader": lambda m: m.schedule.get_type_count(Trader),
                # "Trade Volume": lambda m: sum(
                #     len(a.trade_partners)
                #     for a in m.schedule.agents_by_type[Trader].values()
                # ),
                "Price": lambda m: geometric_mean(
                    flatten(
                        [a.prices for a in m.schedule.agents_by_type[Trader].values()]
                    )
                ),
            },
            agent_reporters={
                # "Trade Network": lambda a: get_trade(a),
                # "Prices mean": lambda a: np.mean(a.prices) if isinstance(a, Trader) else None,
                "Resources": lambda a: a.sugar + a.spice if isinstance(a, Trader) else None,
                # "Individual Trade Volume": lambda a: len(a.trade_partners) if isinstance(a, Trader) else None
                },
        )

        # read in landscape file from supplmentary material
        # unhash for run server
        # sugar_distribution = np.genfromtxt("sugarscape_g1mt/sugarscape_g1mt/sugar-map.txt")
        sugar_distribution = np.genfromtxt("sugarscape_g1mt/sugar-map.txt")
        spice_distribution = np.flip(sugar_distribution, 1)

        agent_id = 0
        for _, x, y in self.grid.coord_iter():
            max_sugar = sugar_distribution[x, y]
            if max_sugar > 0:
                sugar = Sugar(agent_id, self, (x, y), max_sugar)
                self.schedule.add(sugar)
                self.grid.place_agent(sugar, (x, y))
                agent_id += 1

            max_spice = spice_distribution[x, y]
            if max_spice > 0:
                spice = Spice(agent_id, self, (x, y), max_spice)
                self.schedule.add(spice)
                self.grid.place_agent(spice, (x, y))
                agent_id += 1

        # scale individual agent parameters with micro params: h_e, h_m, h_v
        mu_sugar = (self.endowment_min + self.endowment_max)/2
        mu_spice = (self.endowment_min + self.endowment_max)/2

        mu_metabolism_sugar = (self.metabolism_min + self.metabolism_max)/2
        mu_metabolism_spice = (self.metabolism_min + self.metabolism_max)/2

        mu_vision = (self.vision_min + self.vision_max)/2

        for i in range(self.initial_population):
            # get agent position
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            # see Growing Artificial Societies p. 108 for initialization
            # give agents initial endowment
            sugar = int(self.random.uniform(self.endowment_min, self.endowment_max + 1))
            spice = int(self.random.uniform(self.endowment_min, self.endowment_max + 1))
            # give agents initial metabolism
            metabolism_sugar = int(
                self.random.uniform(self.metabolism_min, self.metabolism_max + 1)
            )
            metabolism_spice = int(
                self.random.uniform(self.metabolism_min, self.metabolism_max + 1)
            )
            # give agents vision
            vision = int(self.random.uniform(self.vision_min, self.vision_max + 1))

            # scale agent parameters: sugar, spice, metabolism_sugar, metabolism_spice, vision
            sugar_scaled = fint(mu_sugar + self.h_e*(sugar-mu_sugar), self)

            spice_scaled = fint(mu_spice + self.h_e*(spice-mu_spice), self)

            metabolism_sugar_scaled = fint(mu_metabolism_sugar + self.h_m*(metabolism_sugar-mu_metabolism_sugar), self)
            metabolism_spice_scaled = fint(mu_metabolism_spice + self.h_m*(metabolism_spice-mu_metabolism_spice), self)

            vision_scaled = fint(mu_vision + self.h_v*(vision-mu_vision), self)

            # create Trader object
            trader = Trader(
                agent_id,
                self,
                (x, y),
                moore=False,
                sugar=sugar_scaled,
                spice=spice_scaled,
                metabolism_sugar=metabolism_sugar_scaled,
                metabolism_spice=metabolism_spice_scaled,
                vision=vision_scaled,
            )
            # place agent
            self.grid.place_agent(trader, (x, y))
            self.schedule.add(trader)
            agent_id += 1

    def randomize_traders(self):
        """
        helper function for self.step()

        puts traders in randomized list for step function
        """

        traders_shuffle = list(self.schedule.agents_by_type[Trader].values())
        self.random.shuffle(traders_shuffle)

        return traders_shuffle

    def step(self):
        """
        Unique step function that does staged activation of sugar and spice
        and then randomly activates traders
        """
        # step Sugar agents
        for sugar in self.schedule.agents_by_type[Sugar].values():
            sugar.step()

        # step Spice agents
        for spice in self.schedule.agents_by_type[Spice].values():
            spice.step()

        # step trader agents
        # to account for agent death and removal we need a seperate data strcuture to
        # iterate
        trader_shuffle = self.randomize_traders()

        for agent in trader_shuffle: 
            agent.check_death()

            agent.prices = []
            agent.trade_partners = []
            agent.move()
            agent.eat()
            
            agent.phantom_death()

        trader_shuffle = self.randomize_traders()

        for agent in trader_shuffle:
            agent.trade_with_neighbors()

        self.schedule.steps += (
            1  # important for data collector to track number of steps
        )

        # collect model level data
        self.datacollector.collect(self)
        """
        Mesa is working on updating datacollector agent reporter
        so it can collect information on specific agents from
        mesa.time.RandomActivationByType.

        Please see issue #1419 at
        https://github.com/projectmesa/mesa/issues/1419
        (contributions welcome)

        Below is one way to update agent_records to get specific Trader agent data
        """
        # Need to remove excess data
        # Create local variable to store trade data
        agent_trades = self.datacollector._agent_records[self.schedule.steps]
        # Get rid of all None to reduce data storage needs
        agent_trades = [agent for agent in agent_trades if agent[2] is not None]
        # Reassign the dictionary value with lean trade data
        self.datacollector._agent_records[self.schedule.steps] = agent_trades

    def run_model(self):
        for i in range(self.max_steps):
            self.step()
