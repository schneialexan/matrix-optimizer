import numpy as np
import os
import json

def cost_function(matrix, a, A):
    error = np.dot(a, matrix) - A
    return np.mean(error**2)

def apply_constraints(matrix, locked_indices, locked_values, max_change, initial_matrix):
    matrix_copy = matrix.copy()
    
    for (i, j), value in zip(locked_indices, locked_values):
        matrix_copy[i, j] = value

    matrix_copy = np.clip(matrix_copy, initial_matrix - max_change, initial_matrix + max_change)
    return matrix_copy

def gradient(matrix, a, A, locked_indices, locked_values):
    error = np.dot(a, matrix) - A
    # calculate gradient
    grad = grad = 2 * np.dot(error.T, a) / a.shape[0]
    # apply constraint
    for (i, j), _ in zip(locked_indices, locked_values):
        grad[i, j] = 0.0

    return grad

def cost_function_single_matrix(flattened_matrix, matrices):
    matrix = flattened_matrix.reshape((matrices[0].shape[1], matrices[0].shape[1]))
    total_cost = 0.0

    for i in range(len(matrices) - 1):
        input_matrix = matrices[i]
        output_matrix = matrices[i + 1]
        error = np.dot(input_matrix, matrix) - output_matrix
        total_cost += np.mean(error**2)

    return total_cost

def max_change_constraint_single_matrix(flat_matrix, initial_matrix, max_change):
    matrix = flat_matrix.reshape(initial_matrix.shape)
    diff_matrix = np.abs(matrix - initial_matrix)
    return np.max(diff_matrix) - max_change


def constraint(matrix, initial_matrix, locked_indices, values):
    constrained_elements = [matrix[i, j] - value for (i, j), value in zip(locked_indices, values)]
    return np.array(constrained_elements)

def max_change_constraint(matrix, initial_matrix, max_change):
    diff_matrix = np.abs(matrix - initial_matrix)
    return np.max(diff_matrix) - max_change


def make_initial_matrix(matrix_size):
    return [{str(i+1): '1.0' for i in range(matrix_size)} for j in range(matrix_size)]


def make_matrix_from_dict(matrix):
    return np.array([[float(value) for value in row.values()] for row in matrix])


def make_dict_from_matrix(matrix):
    return [{str(i+1): str(value) for i, value in enumerate(row)} for row in matrix]


def make_table_cols(matrix_size):
    return [{"name": str(i+1), "id": str(i+1)} for i in range(matrix_size)]


def make_indices_from_matrixsize(matrix_size):
    indices = []
    for i in range(matrix_size):
        for j in range(matrix_size):
            indices.append({'label': f'({i+1}, {j+1})', 'value': f'{(i, j)}'})
    return indices


def make_matrix(matrix, matrix_size):
    new_matrix = np.ones((matrix_size, matrix_size), dtype=np.float64)
    iters = min(matrix_size, len(matrix))
    for i in range(iters):
        for j in range(iters):
            new_matrix[i][j] = matrix[i].get(str(j+1))
    return make_dict_from_matrix(new_matrix)


def get_best_learn_rate(matrix_to_optimize, matrices, start_lr=1e-10, end_lr=1e2, num_steps=100):
    costs = {}
    for i in range(len(matrices) - 1):
        input_matrix = matrices[i]
        output_matrix = matrices[i + 1]

        grad = gradient(matrix_to_optimize, input_matrix, output_matrix, [], [])
        # iterate through the learning rates and make num_steps steps
        lr_mult = (end_lr / start_lr) ** (1 / num_steps)
        lrs = [start_lr * lr_mult ** i for i in range(num_steps)]
        for lr in lrs:
            new_matrix = matrix_to_optimize - lr * grad
            costs[lr] = cost_function(new_matrix, input_matrix, output_matrix)
    return min(costs, key=costs.get)

# get all available cities from data folder
def get_cities():
    cities = []
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, 'data')
    path = os.path.join(path, 'cities')
    for file in os.listdir(path):
        if file.endswith(".npy"):
            cities.append(file.split('.')[0].capitalize())
    print(cities)
    return cities

def get_columns(city):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(path, 'data')
    path = os.path.join(path, 'cities')
    file_name = f'{city}_parameters.json'
    with open(os.path.join(path, file_name)) as f:
        data = json.load(f)
    return [{"name": col, "id": str(i+1)} for i, col in enumerate(data)]
