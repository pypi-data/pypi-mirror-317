"""Utilities to more efficiently work with data in matrix formats."""

import numpy as np
import pandas as pd


def matrix_to_dataframe(
    data: dict[str, np.ndarray], row_index: np.ndarray, col_index: np.ndarray
):
    """Converts a dictionary of 2d numpy matrices into a pandas DataFrame indexed by RowID and ColID.

    Parameters:
    -----------
    data : dict[str, np.ndarray]
        A dictionary of 2d numpy matrices, each with a unique key.
    row_index : np.ndarray
        The row index for the DataFrame.
    col_index : np.ndarray
        The column index for the DataFrame.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame with the data from the numpy matrices. The row
        multi-index includes RowID and ColID. Each column represents a matrix
        from the input dictionary."""

    ROW_ID = "RowID"
    COL_ID = "ColID"

    #Validate data and index compatibility
    if not all(matrix.shape == (len(row_index), len(col_index)) for matrix in data.values()):
        raise ValueError("All matrices must have the same shape as the row and column indices.")
    
    # Make sure both row and column indices are unique
    if len(row_index) != len(np.unique(row_index)):
        raise ValueError("Row index must be unique.")
    if len(col_index) != len(np.unique(col_index)):
        raise ValueError("Column index must be unique.")
    

    # Create an empty DataFrame
    index = pd.MultiIndex.from_product([row_index, col_index], names=[ROW_ID, COL_ID])
    df = pd.DataFrame(index=index)

    # Fill the DataFrame with the data from the numpy matrices
    for key, matrix in data.items():
        df[key] = matrix.flatten()

    return df
