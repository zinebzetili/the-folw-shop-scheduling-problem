# -*- coding: utf-8 -*-
"""NMO_project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jCFXLJgFnmh8orIkohwCkcza4lbTjZt6

# ***The implementation***
"""

import numpy as np
import random

# Define problem instance parameters
n = 5  # Number of jobs
m = 3  # Number of machines

p = np.array([[2, 1, 2, 1, 3],   # Processing times for jobs on machines
              [1, 2, 1, 2, 1],
              [2, 2, 3, 2, 1]])

r_min = np.array([1, 1, 0])   # Minimum idle time for each machine
d_max = np.array([5, 2, 0])   # Maximum idle time for each machine

# Tabu search parameters
tabu_tenure = 5
max_iterations = 100
random.seed(42)
# Generate initial solution
def generate_initial_solution():
    return [random.sample(range(1, n+1), n) for _ in range(m)]

# Evaluate the completion time of a solution
def evaluate_completion_time(solution):
    completion_times = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            job = solution[i][j] - 1
            if j == 0:
                completion_times[i, j] = p[i, job]
            else:
                completion_times[i, j] = max(completion_times[i, j-1], completion_times[i-1, j]) + p[i, job]
    return np.max(completion_times)

# Generate successor states by swapping jobs between machines
def generate_successor_states(solution):
    successors = []
    for i in range(m):
        for j in range(n-1):
            for k in range(j+1, n):
                successor = [machine.copy() for machine in solution]
                successor[i][j], successor[i][k] = successor[i][k], successor[i][j]
                successors.append(successor)
    return successors

# Tabu search algorithm
def tabu_search(initial_solution, tabu_tenure, max_iterations):
    current_solution = initial_solution
    best_solution = current_solution
    tabu_list = []
    best_cost = evaluate_completion_time(current_solution)

    for _ in range(max_iterations):
        successor_states = generate_successor_states(current_solution)
        successor_states.sort(key=lambda x: evaluate_completion_time(x))

        new_solution = None
        for successor in successor_states:
            cost = evaluate_completion_time(successor)
            if (cost < best_cost and successor not in tabu_list) or (cost >= best_cost and successor == best_solution):
                new_solution = successor
                break

        if new_solution:
            current_solution = new_solution
            best_solution = current_solution
            best_cost = evaluate_completion_time(current_solution)

        # Update tabu list
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

    return best_solution

# Main function
def main():
    initial_solution = generate_initial_solution()
    best_solution = tabu_search(initial_solution, tabu_tenure, max_iterations)

    print("The best known solution for n =", n, ", m =", m, "is:")
    print("The order of jobs on each machine:")
    for i, machine in enumerate(best_solution, start=1):
        print("Machine", i, ":", machine)
    print("Total completion time:", evaluate_completion_time(best_solution))

if __name__ == "__main__":
    main()

