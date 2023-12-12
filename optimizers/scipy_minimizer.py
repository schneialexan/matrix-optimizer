from helpers import helpers
from scipy.optimize import minimize

MAX_ITERATIONS = 1000000

def optimize_matrix(initial_matrix, matrices, locked_indices, max_change):
    bounds = [
            ((initial_matrix[i, j] - max_change, initial_matrix[i, j] + max_change) if (i, j) not in locked_indices
            else (initial_matrix[i, j], initial_matrix[i, j]))
            for i in range(initial_matrix.shape[0])
            for j in range(initial_matrix.shape[1])
        ]

    result = minimize(helpers.cost_function_single_matrix, 
                      initial_matrix.flatten(), 
                      args=(matrices),
                      bounds=bounds,
                      method='SLSQP'
                      )

    optimized_matrix = result.x.reshape(initial_matrix.shape)
    return optimized_matrix, result.fun

def minimize_matrix(initial_matrix, matrices, locked_indices, max_change):
    return optimize_matrix(initial_matrix, matrices, locked_indices, max_change)