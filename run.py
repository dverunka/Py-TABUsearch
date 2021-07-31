#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import tsplib95

import tabu_search

RUNS = 30

OUTPUT_DIR = "graphs/"

def init_graph(title):
    plt.xlabel("number of iterations")
    plt.ylabel("cost function")
    plt.grid(True)
    plt.title(title)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        INPUT_DATA = sys.argv[1]
        input_data = tsplib95.load(f"./{INPUT_DATA}")

        print(f"Nodes: {len(list(input_data.get_nodes()))}")

        init_graph(f"TABU search, {input_data.name}, {RUNS} runs")

        cost_best_results = []
        cost_history_results = []

        # without cache the algorithm would be much slower
        distance_cache = {}
        total_distance_cache = {}

        for i in range(RUNS):
            cost_best, path_best, costs_history = tabu_search.run(input_data, distance_cache, total_distance_cache)
            cost_best_results.append(cost_best)
            cost_history_results.append(costs_history)

            plt.plot(range(1, len(costs_history) + 1), costs_history, linewidth = 1)

            sys.stdout.write(f"\rRun {i + 1}/{RUNS} completed.")
            sys.stdout.flush()

        print("")

        plt.savefig(f"{OUTPUT_DIR}{input_data.name}_all_runs.png")
        plt.clf()
        plt.cla()
        plt.close()

        average_run_history = np.mean(cost_history_results, axis = 0)

        init_graph(f"TABU search, {input_data.name}, average best run")
        plt.plot(range(1, len(average_run_history) + 1), average_run_history, linewidth = 1)
        plt.savefig(f"{OUTPUT_DIR}{input_data.name}_avg_best_run.png")
        plt.clf()
        plt.cla()
        plt.close()

        minimum = np.min(cost_best_results)
        maximum = np.max(cost_best_results)
        mean = np.mean(cost_best_results)
        median = np.median(cost_best_results)
        stddev = np.std(cost_best_results)

        print(f"TABU search of {input_data.name}: min={minimum}, max={maximum}, mean={mean}, median={median}, stddev={stddev}")

    else:
        print(f"Usage: python3 run.py [input_data_name.tsp]")
