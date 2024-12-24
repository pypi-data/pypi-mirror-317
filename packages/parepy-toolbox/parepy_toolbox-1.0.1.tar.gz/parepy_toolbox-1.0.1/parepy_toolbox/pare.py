"""PAREpy toolbox: Probabilistic Approach to Reliability Engineering"""
import time
import copy
import os
import itertools
from datetime import datetime
from multiprocessing import Pool

import numpy as np
import pandas as pd

import parepy_toolbox.common_library as parepyco


def sampling_algorithm_structural_analysis_kernel(setup: dict) -> pd.DataFrame:
    """
    This function creates the samples and evaluates the limit state functions in structural reliability problems. Based on the data, it calculates probabilities of failure and reliability indexes.

    Args:
        setup (Dictionary): Setup settings
        'number of samples' (Integer): Number of samples (key in setup dictionary)
        'numerical model' (Dictionary): Numerical model settings (key in setup dictionary)
        'variables settings' (List): Variables settings, listed as dictionaries (key in setup dictionary)
        'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints (key in setup dictionary)
        'none variable' (None, list, float, dictionary, str or any): None variable. User can use this variable in objective function (key in setup dictionary)
        'objective function' (Python function): Objective function. The PAREpy user defined this function (key in setup dictionary)
        'name simulation' (String or None): Output filename (key in setup dictionary)

    Returns:
        results_about_data (DataFrame): Results about reliability analysis
        failure_prob_list (List): Failure probability list
        beta_list (List): Beta list
    """
        

    # General settings
    obj = setup['objective function']
    n_samples = setup['number of samples']
    variables_settings = setup['variables settings']
    for i in variables_settings:
        if 'seed' not in i:
            i['seed'] = None
    n_dimensions = len(variables_settings)
    n_constraints = setup['number of state limit functions or constraints']
    none_variable = setup['none variable']

    # Algorithm settings
    model = setup['numerical model']
    algorithm = model['model sampling']
    if algorithm.upper() == 'MCS-TIME':
        time_analysis = model['time steps']
    else:
        time_analysis = None

    # Creating samples
    dataset_x = parepyco.sampling(n_samples=n_samples, model=model,
                                    variables_setup=variables_settings)
    
    # Starting variables
    capacity = np.zeros((len(dataset_x), n_constraints))
    demand = np.zeros((len(dataset_x), n_constraints))
    state_limit = np.zeros((len(dataset_x), n_constraints))
    indicator_function = np.zeros((len(dataset_x), n_constraints))

    # Singleprocess Objective Function evaluation
    for id, sample in enumerate(dataset_x):
        capacity_i, demand_i, state_limit_i = obj(list(sample), none_variable)
        capacity[id, :] = capacity_i.copy()
        demand[id, :] = demand_i.copy()
        state_limit[id, :] = state_limit_i.copy()
        indicator_function[id, :] = [1 if value <= 0 else 0 for value in state_limit_i]

    # Storage all results (horizontal stacking)
    results = np.hstack((dataset_x, capacity, demand, state_limit, indicator_function))

    # Transforming time results in dataframe X_i T_i R_i S_i G_i I_i
    if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
        tam = int(len(results) / n_samples)
        line_i = 0
        line_j = tam
        result_all = []
        for i in range(n_samples):
            i_sample_in_temp = results[line_i:line_j, :]
            i_sample_in_temp = i_sample_in_temp.T
            line_i += tam
            line_j += tam
            i_sample_in_temp = i_sample_in_temp.flatten().tolist()
            result_all.append(i_sample_in_temp)
        results_about_data = pd.DataFrame(result_all)
    else:
        results_about_data = pd.DataFrame(results)
   
    # Rename columns in dataframe
    column_names = []
    for i in range(n_dimensions):
        if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
            for j in range(time_analysis):
                column_names.append(f'X_{i}_t={j}')
        else:
            column_names.append(f'X_{i}')
    if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
        for i in range(time_analysis):
            column_names.append(f'STEP_t_{i}') 
    for i in range(n_constraints):
        if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
            for j in range(time_analysis):
                column_names.append(f'R_{i}_t={j}')
        else:
            column_names.append(f'R_{i}')
    for i in range(n_constraints):
        if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
            for j in range(time_analysis):
                column_names.append(f'S_{i}_t={j}')
        else:
            column_names.append(f'S_{i}')
    for i in range(n_constraints):
        if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
            for j in range(time_analysis):
                column_names.append(f'G_{i}_t={j}')
        else:
            column_names.append(f'G_{i}') 
    for i in range(n_constraints):
        if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
            for j in range(time_analysis):
                column_names.append(f'I_{i}_t={j}')
        else:
            column_names.append(f'I_{i}')
    results_about_data.columns = column_names

    # First Barrier Failure (FBF) or non-dependent time reliability analysis
    if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
        results_about_data, _ = parepyco.fbf(algorithm, n_constraints, time_analysis, results_about_data)
              
    return results_about_data


def sampling_algorithm_structural_analysis(setup: dict) -> tuple[pd.DataFrame, list, list]:
    """
    This function creates the samples and evaluates the limit state functions in structural reliability problems.

    Args:
        setup (Dictionary): Setup settings.
        'number of samples' (Integer): Number of samples (key in setup dictionary)
        'numerical model' (Dictionary): Numerical model settings (key in setup dictionary)
        'variables settings' (List): Variables settings (key in setup dictionary)
        'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints  
        'none_variable' (None, list, float, dictionary, str or any): None variable. User can use this variable in objective function (key in setup dictionary)           
        'objective function' (Python function): Objective function. The PAREpy user defined this function (key in setup dictionary)
        'name simulation' (String or None): Output filename (key in setup dictionary)
    
    Returns:    
        results_about_data (DataFrame): Results about reliability analysis
        failure_prob_list (List): Failure probability list
        beta_list (List): Beta list
    """

    try:
        # Setup verification
        if not isinstance(setup, dict):
            raise TypeError('The setup parameter must be a dictionary.')

        # Keys verification
        for key in setup.keys():
            if key not in ['objective function',
                           'number of samples',
                           'numerical model',
                           'variables settings',
                           'number of state limit functions or constraints',
                           'none variable',
                           'type process',
                           'name simulation'
                          ]:
                raise ValueError("""The setup parameter must have the following keys:
                                    - objective function;
                                    - number of samples;
                                    - numerical model;
                                    - variables settings;
                                    - number of state limit functions or constraints;
                                    - none variable;
                                    - type process;
                                    - name simulation"""
                                )

        # Number of samples verification
        if not isinstance(setup['number of samples'], int):
            raise TypeError('The key "number of samples" must be an integer.')

        # Numerical model verification
        if not isinstance(setup['numerical model'], dict):
            raise TypeError('The key "numerical model" must be a dictionary.')

        # Variables settings verification
        if not isinstance(setup['variables settings'], list):
            raise TypeError('The key "variables settings" must be a list.')

        # Number of state limit functions or constraints verification
        if not isinstance(setup['number of state limit functions or constraints'], int):
            raise TypeError('The key "number of state limit functions or constraints" must be an integer.')
        
        # Objective function verification
        if not callable(setup['objective function']):
            raise TypeError('The key "objective function" must be Python function.')        
        
        # Name simulation verification
        if not isinstance(setup['name simulation'], (str, type(None))):
            raise TypeError('The key "name simulation" must be a None or string.')
        parepyco.log_message('Checking inputs completed!')

        # Multiprocessing sampling algorithm
        parepyco.log_message('Started State Limit Function evaluation (g)...')
        total_samples = setup['number of samples']
        algorithm = setup['numerical model']['model sampling']
        div = total_samples // 10
        mod = total_samples % 10
        setups = []
        for i in range(10):
            new_setup = copy.deepcopy(setup)
            if i == 9:
                samples = div + mod
            else:
                samples = div
            new_setup['number of samples'] = samples
            setups.append(new_setup)
        start_time = time.perf_counter()
        with Pool() as pool:
            results = pool.map(sampling_algorithm_structural_analysis_kernel, setups)
        end_time = time.perf_counter()
        results_about_data = pd.concat(results, ignore_index=True)
        final_time = end_time - start_time
        parepyco.log_message(f'Finished State Limit Function evaluation (g) in {final_time:.2e} seconds!')

        # Failure probability and beta index calculation
        parepyco.log_message('Started evaluation beta reliability index and failure probability...')
        start_time = time.perf_counter()
        failure_prob_list, beta_list = parepyco.calc_pf_beta(results_about_data, algorithm.upper(), setup['number of state limit functions or constraints'])
        end_time = time.perf_counter()
        final_time = end_time - start_time
        parepyco.log_message(f'Finished evaluation beta reliability index and failure probability in {final_time:.2e} seconds!')

        # Save results in .txt file
        if setup['name simulation'] is not None:
            name_simulation = setup['name simulation']
            file_name = str(datetime.now().strftime('%Y%m%d-%H%M%S'))
            file_name_txt = f'{name_simulation}_{algorithm.upper()}_{file_name}.txt'
            results_about_data.to_csv(file_name_txt, sep='\t', index=False)
            parepyco.log_message(f'Voilà!!!!....simulation results are saved in {file_name_txt}')
        else:
            parepyco.log_message('Voilà!!!!....simulation results were not saved in a text file!')

        return results_about_data, failure_prob_list, beta_list

    except (Exception, TypeError, ValueError) as e:
        print(f"Error: {e}")
        return None, None, None


def concatenates_txt_files_sampling_algorithm_structural_analysis(setup: dict) -> tuple[pd.DataFrame, list, list]:
    """
    Concatenates .txt files generated by the sampling_algorithm_structural_analysis algorithm, and calculates probabilities of failure and reliability indexes based on the data.

    Args:
        setup (Dictionary): Setup settings.
        'folder_path' (String): Path to the folder containing the .txt files (key in setup dictionary)
        'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints  
        'simulation name' (String or None): Name of the simulation (key in setup dictionary)
    
    Returns:    
        results_about_data (DataFrame): A DataFrame containing the concatenated results from the .txt files.
        failure_prob_list (List): A list containing the calculated failure probabilities for each indicator function.
        beta_list (List): A list containing the calculated reliability indices (beta) for each indicator function.
    """

    try:
        # General settings
        if not isinstance(setup, dict):
            raise TypeError('The setup parameter must be a dictionary.')

        folder_path = setup['folder_path']
        algorithm = setup['numerical model']['model sampling']
        n_constraints = setup['number of state limit functions or constraints']

        # Check folder path
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f'The folder path {folder_path} does not exist.')

        # Concatenate files
        start_time = time.perf_counter()
        parepyco.log_message('Uploading files!')
        results_about_data = pd.DataFrame()
        for file_name in os.listdir(folder_path):
            # Check if the file has a .txt extension
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                temp_df = pd.read_csv(file_path, delimiter='\t')
                results_about_data = pd.concat([results_about_data, temp_df], ignore_index=True)
        end_time = time.perf_counter()
        final_time = end_time - start_time
        parepyco.log_message(f'Finished Upload in {final_time:.2e} seconds!')

        # Failure probability and beta index calculation
        parepyco.log_message('Started evaluation beta reliability index and failure probability...')
        start_time = time.perf_counter()
        failure_prob_list, beta_list = parepyco.calc_pf_beta(results_about_data, algorithm.upper(), n_constraints)
        end_time = time.perf_counter()
        final_time = end_time - start_time
        parepyco.log_message(f'Finished evaluation beta reliability index and failure probability in {end_time - start_time:.2e} seconds!')

        # Save results in .txt file
        if setup['name simulation'] is not None:
            name_simulation = setup['name simulation']
            file_name = str(datetime.now().strftime('%Y%m%d-%H%M%S'))
            file_name_txt = f'{name_simulation}_{algorithm.upper()}_{file_name}.txt'
            results_about_data.to_csv(file_name_txt, sep='\t', index=False)
            parepyco.log_message(f'Voilà!!!!....simulation results are saved in {file_name_txt}')
        else:
            parepyco.log_message('Voilà!!!!....simulation results were not saved in a text file!')

        return results_about_data, failure_prob_list, beta_list

    except (Exception, TypeError, ValueError) as e:
        print(f"Error: {e}")
        return None, None, None


def deterministic_algorithm_structural_analysis(setup: dict) -> tuple[pd.DataFrame, float, float]:
    """
    This function solves the deterministic problem in structural reliability problems.
    
    Args:
        setup (dict): Setup settings.
        'objective function' (Python function [def]): Objective function. The Parepy user defined this function (key in setup dictionary)
        'gradient objective function' (Python function [def]): Gradient objective function. The Parepy user defined this function (key in setup dictionary)
        'numerical model' (Dictionary): Numerical model settings (key in setup dictionary)
        'variables settings' (List): Variables settings (key in setup dictionary)
        'number of iterations' (Integer): Number of iterations (key in setup dictionary)
    """
    try:
        # General settings
        initial_time = time.time()
        n_iter = setup['number of iterations']
        obj = setup['objective function']
        grad_obj = setup['gradient objective function']
        model = setup['numerical model']['model']
        none_variable = setup['none variable']
        x_initial_guess = setup['numerical model']['initial guess']
        x_initial_guess = np.array([x_initial_guess])
    except KeyError as e:
        raise KeyError(f"Missing required key in setup: {e}")
    except Exception as e:
        raise Exception(f"Error during setup initialization: {e}")

    try:
        g_sol = []
        grad_sol = []
        beta_sol = []
        y_sol = []
        x_sol = []

        # Hasofer-Lind method part 1
        parameters = setup['variables settings']
        locs = [d['parameters']['mean'] for d in parameters]
        stds = [d['parameters']['sigma'] for d in parameters]
        jacobian_xy = np.diag(stds)
        jacobian_xy_trans = np.transpose(jacobian_xy)
        jacobian_yx = np.linalg.inv(jacobian_xy)
        locs = np.array([locs])
        length = len(setup['variables settings'])
        print("Jxy: ", jacobian_xy)
        print("JxyT ", jacobian_xy_trans)
        print("Jyx: ", jacobian_yx)
    except KeyError as e:
        raise KeyError(f"Missing required key in variables settings: {e}")
    except ValueError as e:
        raise ValueError(f"Error in variable setup or dimensions: {e}")
    except Exception as e:
        raise Exception(f"Error during matrix initialization: {e}")

    try:
        if model.upper() == 'FOSM':
            for i in range(n_iter):
                try:
                    if i == 0:
                        x = x_initial_guess.copy()
                    else:
                        x = x_new.copy()

                    # Hasofer-Lind method part 2
                    y = np.dot(jacobian_yx, np.transpose(x) - np.transpose(locs))
                    y_sol.append(np.transpose(y)[0].tolist())
                    x_sol.append(x[0].tolist())

                    g_y = obj(x[0].tolist(), none_variable)
                    g_diff_x = grad_obj(x[0].tolist(), none_variable)
                    g_diff_x = np.transpose(np.array([g_diff_x]))
                    g_diff_y = np.dot(jacobian_xy_trans, g_diff_x)

                    print('y: ', y)
                    print("g_y: ", g_y)
                    print("g_diff_x: ", g_diff_x)
                    print("g_diff_y: ", g_diff_y)

                    # Hasofer-Lind algorithm
                    y_new = parepyco.hasofer_lind_rackwitz_fiessler_algorithm(y, g_y, g_diff_y)
                    print("y_new: ", y_new)
                    x_new = np.transpose(np.dot(jacobian_xy, y_new) + np.transpose(locs))
                    print("x_new: ", x_new)

                    beta = np.linalg.norm(y_new)
                    g_sol.append(g_y)
                    grad_sol.append(np.linalg.norm(g_diff_y))
                    beta_sol.append(beta)

                except Exception as e:
                    raise Exception(f"Error during iteration {i}: {e}")

            y_sol = np.array(y_sol)
            x_sol = np.array(x_sol)

        elif model.upper() == 'FORM':
            pass
        elif model.upper() == 'SORM':
            pass

    except Exception as e:
        raise Exception(f"Error during model execution: {e}")

    try:
        results_about_data = {
            "x0": x_sol[:, 0],
            "x1": x_sol[:, 1],
            #"x2": x_sol[:, 2],
            "y0": y_sol[:, 0],
            "y1": y_sol[:, 1],
            #"y2": y_sol[:, 2],
            "state limit function": g_sol,
            "ϐ new": beta_sol
        }

        results_about_data = pd.DataFrame(results_about_data)
        failure_prob_list, beta_list = 0, 0

    except Exception as e:
        raise Exception(f"Error during result preparation: {e}")

    return results_about_data, failure_prob_list, beta_list


def sobol_algorithm(setup):
    """
    This function calculates the Sobol indices in structural reliability problems.

    Args:
        setup (Dictionary): Setup settings.
        'number of samples' (Integer): Number of samples (key in setup dictionary)
        'variables settings' (List): Variables settings, listed as dictionaries (key in setup dictionary)
        'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints (key in setup dictionary)
        'none variable' (None, list, float, dictionary, str or any): None variable. User can use this variable in objective function (key in setup dictionary)
        'objective function' (Python function): Objective function defined by the user (key in setup dictionary)

    Returns:
        dict_sobol (DataFrame): A dictionary containing the first-order and total-order Sobol sensitivity indixes for each input variable.
    """
    n_samples = setup['number of samples']
    obj = setup['objective function']
    none_variable = setup['none variable']

    dist_a = sampling_algorithm_structural_analysis_kernel(setup)
    dist_b = sampling_algorithm_structural_analysis_kernel(setup)
    y_a = dist_a['G_0'].to_list()
    y_b = dist_b['G_0'].to_list()
    f_0_2 = (sum(y_a) / n_samples) ** 2

    A = dist_a.drop(['R_0', 'S_0', 'G_0', 'I_0'], axis=1).to_numpy()
    B = dist_b.drop(['R_0', 'S_0', 'G_0', 'I_0'], axis=1).to_numpy()
    K = A.shape[1]

    s_i = []
    s_t = []
    p_e = []
    for i in range(K):
        C = np.copy(B) 
        C[:, i] = A[:, i]
        y_c_i = []
        for j in range(n_samples):
            _, _, g = obj(list(C[j, :]), none_variable)
            y_c_i.append(g[0])  
        
        y_a_dot_y_c_i = [y_a[m] * y_c_i[m] for m in range(n_samples)]
        y_b_dot_y_c_i = [y_b[m] * y_c_i[m] for m in range(n_samples)]
        y_a_dot_y_a = [y_a[m] * y_a[m] for m in range(n_samples)]
        s_i.append((1/n_samples * sum(y_a_dot_y_c_i) - f_0_2) / (1/n_samples * sum(y_a_dot_y_a) - f_0_2))
        s_t.append(1 - (1/n_samples * sum(y_b_dot_y_c_i) - f_0_2) / (1/n_samples * sum(y_a_dot_y_a) - f_0_2))

    s_i = [float(i) for i in s_i]
    s_t = [float(i) for i in s_t]
    dict_sobol = pd.DataFrame(
        {'s_i': s_i,
         's_t': s_t}
    )

    return dict_sobol


def generate_factorial_design(level_dict):
    """
    Generates a full factorial design based on the input dictionary of variable levels. The function computes all possible combinations of the provided levels for each variable and returns them in a structured DataFrame.

    Args:
        level_dict (Dictionary): A dictionary where keys represent variable names, and values are lists, arrays, or sequences representing the levels of each variable.

    Returns:
        DataFrame: A dictionary containing all possible combinations of the levels provided in the input dictionary. Each column corresponds to a variable defined in level_dict. And each row represents one combination of the factorial design.
    """
    combinations = list(itertools.product(*level_dict.values()))
    df = pd.DataFrame(combinations, columns=level_dict.keys())

    return df