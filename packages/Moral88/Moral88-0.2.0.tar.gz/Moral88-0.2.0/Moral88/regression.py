def mean_absolute_error(y_true, y_pred, normalize=True, threshold=None, method='mean', library='Moral88'):
    """
    Calculate Mean Absolute Error (MAE) or variants based on method and library.

    Parameters:
    - y_true (list or array): True values (required)
    - y_pred (list or array): Predicted values (required)
    - normalize (bool): If True, normalize the result (default: True)
    - threshold (tuple, optional): Apply a threshold to the predictions (default: None)
    - method (str): Method of calculation. Options: {'mean', 'sum', 'none'}. Default: 'mean'
    - library (str): Library to use for calculations. Options: {'Moral88', 'sklearn', 'torch', 'tensor', 'statsmodel', 'Dask-ML', 'MLlib'}. Default: 'Moral88'.

    Returns:
    - float or list: Calculated error based on selected method and library.
    """
    if library == 'Moral88':
        # Original implementation
        if threshold is not None:
            y_pred = [min(max(pred, threshold[0]), threshold[1]) for pred in y_pred]

        absolute_errors = [abs(y_t - y_p) for y_t, y_p in zip(y_true, y_pred)]

        if method == 'mean':
            result = sum(absolute_errors) / len(y_true)
        elif method == 'sum':
            result = sum(absolute_errors)
        elif method == 'none':
            result = absolute_errors
        else:
            raise ValueError("Invalid method. Choose from {'mean', 'sum', 'none'}.")

        if normalize and method != 'none':
            range_y = max(y_true) - min(y_true)
            result = result / max(abs(range_y), 1)

        return result

    elif library == 'sklearn':
        from sklearn.metrics import mean_absolute_error as sklearn_mae
        return sklearn_mae(y_true, y_pred)

    elif library == 'torch':
        import torch
        y_true_tensor = torch.tensor(y_true, dtype=torch.float32)
        y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
        return torch.mean(torch.abs(y_true_tensor - y_pred_tensor)).item()

    elif library == 'tensorflow':
        import tensorflow as tf
        y_true_tensor = tf.convert_to_tensor(y_true, dtype=tf.float32)
        y_pred_tensor = tf.convert_to_tensor(y_pred, dtype=tf.float32)
        return tf.reduce_mean(tf.abs(y_true_tensor - y_pred_tensor)).numpy()

    # elif library == 'statsmodel':
    #     raise NotImplementedError("Statsmodel does not have a built-in MAE implementation.")

    # elif library == 'Dask-ML':
    #     raise NotImplementedError("Dask-ML support is not implemented yet.")

    # elif library == 'MLlib':
    #     raise NotImplementedError("MLlib support is not implemented yet.")

    else:
        raise ValueError(f"Invalid library: {library}. Choose from {'Moral88', 'sklearn', 'torch', 'tensorflow'}.")


def mean_squared_error(y_true, y_pred, normalize=True, threshold=None, method='mean', library='Moral88'):
    """
    Calculate Mean Squared Error (MSE) or variants based on method and library.

    Parameters:
    - y_true (list or array): True values (required)
    - y_pred (list or array): Predicted values (required)
    - normalize (bool): If True, normalize the result (default: True)
    - threshold (tuple, optional): Apply a threshold to the predictions (default: None)
    - method (str): Method of calculation. Options: {'mean', 'sum', 'none'}. Default: 'mean'
    - library (str): Library to use for calculations. Options: {'Moral88', 'sklearn', 'torch', 'tensor', 'statsmodel', 'Dask-ML', 'MLlib'}. Default: 'Moral88'.

    Returns:
    - float or list: Calculated error based on selected method and library.
    """
    if library == 'Moral88':
        # Original implementation
        if threshold is not None:
            y_pred = [min(max(pred, threshold[0]), threshold[1]) for pred in y_pred]

        squared_errors = [(y_t - y_p) ** 2 for y_t, y_p in zip(y_true, y_pred)]

        if method == 'mean':
            result = sum(squared_errors) / len(y_true)
        elif method == 'sum':
            result = sum(squared_errors)
        elif method == 'none':
            result = squared_errors
        else:
            raise ValueError("Invalid method. Choose from {'mean', 'sum', 'none'}.")

        if normalize and method != 'none':
            range_y = max(y_true) - min(y_true)
            result = result / max(abs(range_y), 1)

        return result

    elif library == 'sklearn':
        from sklearn.metrics import mean_squared_error as sklearn_mse
        return sklearn_mse(y_true, y_pred)

    elif library == 'torch':
        import torch
        y_true_tensor = torch.tensor(y_true, dtype=torch.float32)
        y_pred_tensor = torch.tensor(y_pred, dtype=torch.float32)
        return torch.mean((y_true_tensor - y_pred_tensor) ** 2).item()

    elif library == 'tensorflow':
        import tensorflow as tf
        y_true_tensor = tf.convert_to_tensor(y_true, dtype=tf.float32)
        y_pred_tensor = tf.convert_to_tensor(y_pred, dtype=tf.float32)
        return tf.reduce_mean(tf.square(y_true_tensor - y_pred_tensor)).numpy()

    # elif library == 'statsmodel':
    #     raise NotImplementedError("Statsmodel does not have a built-in MSE implementation.")

    # elif library == 'Dask-ML':
    #     raise NotImplementedError("Dask-ML support is not implemented yet.")

    # elif library == 'MLlib':
    #     raise NotImplementedError("MLlib support is not implemented yet.")

    else:
        raise ValueError(f"Invalid library: {library}. Choose from {'Moral88', 'sklearn', 'torch', 'tensorflow'}.")
def r_squared(y_true, y_pred):
    """
    Compute R-Squared
    """
    import numpy as np
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    ss_total = np.sum((y_true - np.mean(y_true)) ** 2)
    ss_residual = np.sum((y_true - y_pred) ** 2)
    return 1 - (ss_residual / ss_total)