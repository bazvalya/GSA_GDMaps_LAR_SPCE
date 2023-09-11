"""
Script to write data for GSA
"""
from sugarscape_g1mt.model import SugarscapeG1mt
import numpy as np
import os
import tqdm

import time
import argparse
import multiprocess as mp


if not os.path.exists('data/Sobol'):
    os.makedirs('data/Sobol')

# problem for saltelli sampler
problem = {
    'h_e': [float, [0.01, 1]],
    'h_m': [float, [0.01, 1]],
    'h_v': [float, [0.01, 1]],
}

# for SALib's saltelli sampler
problem_sampler = {
    'num_vars': len(problem),
    'names': [key for key in sorted(problem.keys())],
    'bounds': [problem[key][1] for key in sorted(problem.keys())]
}

# set fixed parametes (all model parameters excluding the ones used in sampler)
fixed_parameters = {'initial_population': 320,
                    'width': 50,
                    'height': 50,
                    'endowment_min': 25,
                    'endowment_max': 50,
                    'metabolism_min': 1,
                    'metabolism_max': 5,
                    'vision_min': 1,
                    'vision_max': 5
                    }


def run_model(args):
    model, args, problem_sampler, param_combos, fixed_parameters, seed, i = args
    # create dictionary with variable parameters
    var_param = {}
    for key, val in zip(problem_sampler['names'], param_combos.T):
        var_param[key] = val

    # print(f"Row {i} of parameter values array,  RUN {seed} with seed {seed}")

    m = model(**var_param, **fixed_parameters, seed=seed)

    while m.running and m.schedule.steps < args["time_steps"]:
        m.step()

    return seed, i, m


def run_model_parallel(args):
    n_cores = args["n_cores"]
    if n_cores is None:
        n_cores = mp.cpu_count()

    # load saltelli sample
    task_id = args["task_id"]
    param_values = np.loadtxt('data/Sobol/saltellisample_1024')
    run_length=int(len(param_values)/10)
    lower=task_id*run_length
    upper=(task_id + 1)*run_length

    runs = args["repetitions"]
    results_model  = {}
    # results_agents = {}

    with mp.Pool(n_cores) as pool:
        for r, p, model in tqdm.tqdm(pool.imap_unordered(
            run_model,
            [(SugarscapeG1mt, args, problem_sampler,
              param_values[i], fixed_parameters, j, i+lower) for i in range(len(param_values)) if i+lower < upper for j in range(runs)]
        )):
            if r not in results_model:
                results_model[r] = {}
            # if r not in results_agents:
            #     results_agents[r] = {}
            results_model[r][p] = model.datacollector.get_model_vars_dataframe().to_dict()
            # results_agents[r][p] = model.datacollector.get_agent_vars_dataframe().to_dict()
    
    return results_model


def main(args):
    start = time.time()
    results_model = run_model_parallel(args)
    end = time.time()

    print(f"Done! Took {end - start}")
    print(f"------ Saving data to {args['output_file']} --------")
    np.savez("data/Sobol/"+args['output_file'],
             results_model=results_model, fixed_parameters=fixed_parameters, 
             problem=problem_sampler)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Sugarscape Model with Trader: writing data for GSA")

    argparser.add_argument("output_file", type=str,
                           help="location of output file")
    argparser.add_argument("-r", "--repetitions", type=int, default=1,
                           help="number of stochastic model runs")
    argparser.add_argument("-t", "--time-steps", type=int, default=100,
                           help="number of time steps to execute")
    argparser.add_argument("-n", "--n-cores", type=int, default=None,
                           help="number of processes to use in pool")
    argparser.add_argument("-i", "--task-id", type=int, default=None,
                           help="task id of all run chunks 0-9")

    args = vars(argparser.parse_args())

    main(args)