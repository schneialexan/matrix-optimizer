from helpers import helpers
import numpy as np

LEARNING_RATE = 1e-7
TOLERANCE = 1e-3
MAX_ITERATIONS = 1000000

def optimize_matrix(initial_matrix, matrices, locked_indices, max_change, learning_rate=LEARNING_RATE, tolerance=TOLERANCE, max_iterations=MAX_ITERATIONS):
    current_matrix = initial_matrix.copy()

    iteration = 0
    cost_list = []
    
    locked_values = [initial_matrix[i, j] for (i, j) in locked_indices]

    while iteration < max_iterations:
        for i in range(len(matrices) - 1):
            input_matrix = matrices[i]
            output_matrix = matrices[i + 1]

            grad = helpers.gradient(current_matrix, input_matrix, output_matrix, locked_indices, locked_values)
            current_matrix -= learning_rate * grad
            current_matrix = helpers.apply_constraints(current_matrix, locked_indices, locked_values, max_change, initial_matrix)
        
        new_cost = helpers.cost_function(current_matrix, matrices[0], matrices[-1])
        cost_list.append(new_cost)
        if new_cost < tolerance or (iteration > 1000 and np.round(new_cost, 5) == np.round(cost_list[-1000], 5)):
            break

        iteration += 1

    return np.round(current_matrix, 9), cost_list

def minimize_matrix(initial_matrix, matrices, locked_indices, max_change):
    return optimize_matrix(initial_matrix, matrices, locked_indices, max_change, learning_rate=helpers.get_best_learn_rate(initial_matrix, matrices))