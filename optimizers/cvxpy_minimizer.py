import numpy as np
import cvxpy as cp

def optimize_matrix(initial_matrix, matrices, locked_indices, max_change):
    MAX_ITERATIONS = 100000

    # Define optimization variable
    matrix_var = cp.Variable(initial_matrix.shape)

    # Build the objective function
    error_list = [cp.sum_squares(matrices[i] @ matrix_var - matrices[i + 1]) for i in range(len(matrices) - 1)]
    total_cost = cp.sum(error_list) / np.prod(matrices[0].shape)

    # Build the constraint to lock the specified elements
    constraints_lock = [matrix_var[i, j] == initial_matrix[i, j] for i, j in locked_indices]

    # Define the optimization problem with constraints
    problem = cp.Problem(cp.Minimize(total_cost), constraints_lock)

    # Solve the problem
    problem.solve(max_iter=MAX_ITERATIONS)

    # The optimized matrix M
    optimized_matrix = matrix_var.value

    shape = initial_matrix.shape
    final_matrix = np.copy(initial_matrix)
    unlocked_mask = np.ones(shape, dtype=bool)

    for idx in locked_indices:
        unlocked_mask[idx] = False

    diff_matrix = optimized_matrix - initial_matrix
    clipped_diff_matrix = np.clip(diff_matrix, -max_change, max_change)
    final_matrix[unlocked_mask] = initial_matrix[unlocked_mask] + clipped_diff_matrix[unlocked_mask]

    return final_matrix

def minimize_matrix(initial_matrix, matrices, locked_indices, max_change):
    return optimize_matrix(initial_matrix, matrices, locked_indices, max_change)
