#! /usr/bin/env python3

import time
import argparse
import multiprocess as mp
import numpy as np

from sugarscape_g1mt.model import SugarscapeG1mt

def run_model(args):
    model, args = args
    m = model(**{"seed": args["random_seed"]})

    while m.running and m.schedule.steps < args["time_steps"]:
        m.step()

    return m

def run_model_parallel(args):
    n_cores = args["n_cores"]
    if n_cores is None:
        n_cores = mp.cpu_count()

    repetitions = args["repetitions"]
    results_model  = {}
    results_agents = {}

    with mp.Pool(n_cores) as pool:
        for i, model in enumerate(pool.imap_unordered(
            run_model,
            [(SugarscapeG1mt, args)
             for _ in range(repetitions)]
        )):
            results_model[i] = model.datacollector.get_model_vars_dataframe().to_dict()
            results_agents[i] = model.datacollector.get_agent_vars_dataframe().to_dict()

    return results_model, results_agents


def main(args):
    start = time.time()
    results_model, results_agents = run_model_parallel(args)
    end = time.time()

    print(f"Done! Took {end - start}")
    print(f"------ Saving data to {args['output_file']} --------")
    np.savez(args["output_file"], results_model=results_model,
             results_agents=results_agents)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="Sugarscape Model with Traders runner")

    argparser.add_argument("output_file", type=str,
                           help="location of output file")
    argparser.add_argument("-r", "--repetitions", type=int, default=1,
                           help="number of repeated model runs")
    argparser.add_argument("-t", "--time-steps", type=int, default=1000,
                           help="number of time steps to execute")
    argparser.add_argument("-n", "--n-cores", type=int, default=None,
                           help="number of processes to use in pool")
    argparser.add_argument("-s", "--random_seed", type=int, default=None,
                           help="random seed")

    args = vars(argparser.parse_args())

    main(args)