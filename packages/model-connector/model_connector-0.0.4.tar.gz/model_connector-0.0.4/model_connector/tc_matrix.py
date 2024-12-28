"""Model connector for TC matrix management such as DLL loading, common constants, and common classes."""

import ctypes
from enum import Enum
import os
from pathlib import Path
from typing import Literal, overload, Optional

import numpy as np
import pandas as pd

from model_connector.tc_matrix_dll import _BaseMatrixTC
from model_connector.common import ConvertMissing, _DataType
from model_connector.matrix_utils import matrix_to_dataframe

_MAX_FLABEL = 64
_MAX_PATH = 260


class _MatrixDim(Enum):
    ROW = 0
    COL = 1


class _ControlType(Enum):
    FALSE = 0
    TRUE = 1
    NEVER = 2
    ALWAYS = 3
    AUTOMATIC = 4


_np_dtype: dict[_DataType, np.dtype] = {
    _DataType.SHORT_TYPE: np.dtype(np.int16),
    _DataType.LONG_TYPE: np.dtype(np.int32),
    _DataType.FLOAT_TYPE: np.dtype(np.float32),
    _DataType.DOUBLE_TYPE: np.dtype(np.float64),
}

# Reverse of _np_dtype for mapping numpy dtypes to _DataType
_mtx_dtype: dict[np.dtype, _DataType] = {v: k for k, v in _np_dtype.items()}

_missing: dict[_DataType, np.int16 | np.int32 | np.float32 | np.float64] = {
    _DataType.SHORT_TYPE: np.int16(-32767),
    _DataType.LONG_TYPE: np.int32(-2147483647),
    _DataType.FLOAT_TYPE: np.float32(-3.402823466e38),
    _DataType.DOUBLE_TYPE: np.float64(-1.7976931348623158e308),
}


# Overloads for return types based on the format parameter
@overload
def read_matrix_tc(  # type: ignore
    matrix_file: Path | str,
    missing: ConvertMissing | Literal["zero", "nan", "ignore"] = "zero",
    tables: list[str] | None = None,
    row_index: int | None = None,
    col_index: int | None = None,
    format: Literal["dict"] = "dict",
) -> dict[str, np.ndarray]: ...


@overload
def read_matrix_tc(
    matrix_file: Path | str,
    missing: ConvertMissing | Literal["zero", "nan", "ignore"] = "zero",
    tables: list[str] | None = None,
    row_index: int | None = None,
    col_index: int | None = None,
    format: Literal["df"] = "df",
) -> pd.DataFrame: ...


def read_matrix_tc(
    matrix_file: Path | str,
    missing: ConvertMissing | Literal["zero", "nan", "ignore"] = "zero",
    tables: list[str] | None = None,
    row_index: int | None = None,
    col_index: int | None = None,
    format: Literal["dict", "df"] = "dict",
) -> dict[str, np.ndarray] | pd.DataFrame:
    """Read a TransCAD matrix file and returns a dictionary of numpy arrays.

    Parameters
    ----------
    matrix_file : Path | str
        The path to the TransCAD matrix file.
    missing : ConvertMissing | Literal["zero", "nan", "ignore"], optional
        Specifies how to handle missing values. Defaults to "zero".
            "zero" - Convert missing data to zero.
            "nan" - Convert missing data to NaN.
            "ignore" - Ignore missing data, leaving sentinel values.
    tables : list[str], optional
        A list of table names to read from the matrix file. If None, all tables
        are read. Defaults to None.
    row_index : int, optional
        The row index to set for the matrix. If None, use the base index.
        Defaults to None.
    col_index : int, optional
        The column index to set for the matrix. If None, use the base index.
        Defaults to None.
    format : str, optional, defaults to "dict"
        The format to return the data. valid options are "dict" or "df".

    Returns
    -------
        dict[str, np.ndarray]
            A dictionary where keys are table names and values are numpy arrays
            representing the matrix data.

            or

        pd.DataFrame
            A dataframe with a row index of (RowID, ColID) and columns for each table.

    The row and column index values must be provided as integers, as index names
    are not currently supported.

    The default behavior is to convert missing data to zero. Missing data can only
    be set to NaN for floating point data types or an error will be raised.
    Convert missing to NAN by setting missing=ConvertMissing.NAN.
    """

    if format not in ["dict", "df"]:
        raise ValueError("Invalid format. Must be 'dict' or 'df'.")

    missing = _validate_missing(missing)

    matrix_file = Path(matrix_file)
    result = {}

    with OpenMatrixTC(matrix_file, missing=missing) as mat:

        mat_tables = mat.table_names
        if tables is not None:
            _validate_tables(mat_tables, tables)
            mat_tables = tables

        if row_index is not None or col_index is not None:
            mat.set_index(row_index, col_index)

        for table in mat_tables:
            result[table] = mat[table]

        if format == "df":
            idx = {"row_index": mat.row_ids, "col_index": mat.col_ids}
            result = matrix_to_dataframe(result, **idx)

    return result


def _validate_tables(available_tables, requested_tables):
    """Validate that the requested tables are available in the matrix."""
    for table in requested_tables:
        if table not in available_tables:
            raise ValueError(f"Table {table} not found in the matrix.")


def _validate_missing(missing) -> ConvertMissing:
    if isinstance(missing, ConvertMissing):
        return missing
    if isinstance(missing, str):
        try:
            missing = ConvertMissing[missing.upper()]
        except KeyError:
            raise ValueError(
                "Invalid missing parameter. Must be 'zero', 'nan', or 'ignore'."
            )
        return missing
    raise TypeError("Invalid missing parameter.")


def write_matrix_tc(
    matrix_file: Path | str,
    data: dict[str, np.ndarray],
    label: str = "Matrix",
    missing: ConvertMissing | Literal["zero", "nan", "ignore"] = "zero",
    row_ids: np.ndarray | list[int] | None = None,
    col_ids: np.ndarray | list[int] | None = None,
    compression: bool = True,
) -> None:
    """Write a dictionary of numpy arrays to a TransCAD matrix file.

    Parameters
    ----------
    matrix_file (Path | str): 
        The path to the output TransCAD matrix file.
    data (dict[str, np.ndarray]): 
        A dictionary where keys are table names and values are numpy arrays containing the data.
    label (str, optional): 
        The label for the matrix. Defaults to "Matrix".
    missing (ConvertMissing | Literal["zero", "nan", "ignore"], optional): 
        The method of writing missing (nan) values from the input dataset. Defaults to "zero".
    row_ids (np.ndarray | list[int] | None, optional): 
        An array or list of row IDs. Defaults to None.
    col_ids (np.ndarray | list[int] | None, optional): 
        An array or list of column IDs. Defaults to None.
    compression (bool, optional): 
        Whether to compress the matrix file. Defaults to True.

    """

    # Validate inputs
    matrix_file = Path(matrix_file)
    _validate_data(data)
    missing = _validate_missing(missing)

    # Use the first table to define the matrix shape and data type
    first_table = next(iter(data.values()))

    with CreateMatrixTC(
        matrix_file=matrix_file,
        label=label,
        shape=first_table.shape,
        data_type=_mtx_dtype[first_table.dtype],
        table_count=len(data),
        row_ids=row_ids,
        col_ids=col_ids,
        table_names=list(data.keys()),
        compression=compression,
        missing=missing,
    ) as mat:
        for table, table_data in data.items():
            mat[table] = table_data


def _validate_data(data):
    """Validate the data dictionary for writing to a matrix."""

    shape = None
    dtype = None
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary of numpy arrays.")
    if not data:
        raise ValueError("Data dictionary is empty.")
    for table, table_data in data.items():
        if not isinstance(table, str):
            raise TypeError("Table names must be strings.")
        if not isinstance(table_data, np.ndarray):
            raise TypeError("Table data must be a numpy array.")
        if table_data.ndim != 2:
            raise ValueError("Table data must be a 2D array.")

        if shape is None:
            shape = table_data.shape
        if table_data.shape != shape:
            raise ValueError("All tables must have the same shape.")

        if dtype is None:
            dtype = table_data.dtype

            try:
                _mtx_dtype[dtype]
            except KeyError:
                raise ValueError(f"Unsupported data type: {dtype}.")

        if table_data.dtype != dtype:
            raise ValueError("All tables must have the same data type.")


class MatrixTC:
    def __init__(
        self,
        handle: ctypes.c_void_p,
        tcw: ctypes.WinDLL,
        filename: Path,
        missing: ConvertMissing = ConvertMissing.ZERO,
    ):
        self.handle: ctypes.c_void_p = handle
        self.tcw: ctypes.WinDLL = tcw
        self.filename: Path = filename
        self._missing: ConvertMissing = missing
        self._dtype: Optional[_DataType] = None
        self._table_count: Optional[int] = None
        self._table_names: Optional[list[str]] = None
        self._shape: Optional[tuple[int, int]] = None
        self._index_count: Optional[tuple[int, int]] = None
        self._index: Optional[tuple[int, int]] = None
        self._row_ids: Optional[np.ndarray] = None
        self._col_ids: Optional[np.ndarray] = None

    def clear_cache(self):
        """Clear cached properties."""
        self._dtype = None
        self._table_count = None
        self._table_names = None
        self._shape = None
        self._index_count = None
        self._index = None
        self._row_ids = None
        self._col_ids = None

    @property
    def missing(self) -> ConvertMissing:
        """Get the missing data conversion setting."""
        return self._missing

    @missing.setter
    def missing(self, value: ConvertMissing) -> None:
        """Set the missing data conversion setting."""
        if value == ConvertMissing.NAN and (
            self.dtype == _DataType.SHORT_TYPE or self.dtype == _DataType.LONG_TYPE
        ):
            raise ValueError("Cannot convert missing to NaN for integer matrix files.")
        self._missing = value

    @property
    def dtype(self) -> _DataType:
        """Get the TransCAD data type of the matrix."""
        if self._dtype is None:
            self._dtype = self._get_dtype()

        return self._dtype

    def _get_dtype(self) -> _DataType:
        dtype = self.tcw.MATRIX_GetDataType(self.handle)
        if dtype == _DataType.UNKNOWN_TYPE.value:
            raise OSError(f"Failed to get data type from matrix {self.filename}.")
        return _DataType(dtype)

    @property
    def np_dtype(self) -> np.dtype:
        """Get the numpy data type of the matrix."""
        return _np_dtype[self.dtype]

    @property
    def shape(self) -> tuple[int, int]:
        """Get the shape of the matrix, using the current index."""
        if self._shape is None:
            self._shape = self._get_shape()
        return self._shape

    def _get_shape(self) -> tuple[int, int]:
        n_rows = self.tcw.MATRIX_GetNRows(self.handle)
        if not n_rows:
            raise OSError(f"Failed to get row  count from matrix {self.filename}.")

        n_cols = self.tcw.MATRIX_GetNCols(self.handle)
        if not n_cols:
            raise OSError(f"Failed to get column count from matrix {self.filename}.")

        return (n_rows, n_cols)

    @property
    def table_count(self) -> int:
        """Get the number of tables in the matrix."""
        if self._table_count is None:
            self._table_count = self._get_table_count()
        return self._table_count

    def _get_table_count(self) -> int:
        table_count = self.tcw.MATRIX_GetNCores(self.handle)
        if not table_count:
            raise OSError(f"Failed to get table count from matrix {self.filename}.")
        return table_count

    @property
    def table_names(self) -> list[str]:
        """Get a list of table names in the matrix."""
        if self._table_names is None:
            self._table_names = self._get_tables()
        return self._table_names

    def _get_tables(self) -> list[str]:
        table_names = []
        sz_label = ctypes.create_string_buffer(_MAX_FLABEL)
        for table_index in range(self.table_count):
            self.tcw.MATRIX_GetLabel(self.handle, table_index, sz_label)
            table_names.append(sz_label.value.decode("utf-8"))

        self._table_names = table_names
        return table_names

    @property
    def index_count(self) -> tuple[int, int]:
        """Get the number of matrix (row, column) indices."""
        if self._index_count is None:
            self._index_count = self._get_index_count()
        return self._index_count

    def _get_index_count(self) -> tuple[int, int]:
        row_count = self.tcw.MATRIX_GetNIndices(self.handle, _MatrixDim.ROW.value)
        col_count = self.tcw.MATRIX_GetNIndices(self.handle, _MatrixDim.COL.value)

        return (row_count, col_count)

    @property
    def index(self) -> tuple[int, int]:
        """Get the current matrix (row, column) index ids."""
        if self._index is None:
            self._index = self._get_index()
        return self._index

    def _get_index(self) -> tuple[int, int]:
        row_index = self.tcw.MATRIX_GetCurrentIndexPos(
            self.handle, _MatrixDim.ROW.value
        )
        col_index = self.tcw.MATRIX_GetCurrentIndexPos(
            self.handle, _MatrixDim.COL.value
        )
        return (row_index, col_index)

    def set_index(self, row_index: Optional[int], col_index: Optional[int]) -> None:
        """Set the current matrix (row, column) index ids. None will leave the index unchanged."""

        self.clear_cache()

        if row_index is not None:
            if row_index < 0 or row_index >= self.index_count[0]:
                raise IndexError(f"Row index {row_index} out of range.")
            self.tcw.MATRIX_SetIndex(self.handle, _MatrixDim.ROW.value, row_index)
        if col_index is not None:
            if col_index < 0 or col_index >= self.index_count[1]:
                raise IndexError(f"Column index {col_index} out of range.")
            self.tcw.MATRIX_SetIndex(self.handle, _MatrixDim.COL.value, col_index)

    @property
    def row_ids(self) -> np.ndarray:
        """Get the row ids for the current matrix index."""
        if self._row_ids is None:
            self._row_ids = self._get_ids(_MatrixDim.ROW)
        return self._row_ids

    @property
    def col_ids(self) -> np.ndarray:
        """Get the column ids for the current matrix index."""
        if self._col_ids is None:
            self._col_ids = self._get_ids(_MatrixDim.COL)
        return self._col_ids

    def _get_ids(self, dimension: _MatrixDim) -> np.ndarray:
        count = self.shape[dimension.value]
        ids = np.zeros(count, np.int32)
        ids_p = ids.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.tcw.MATRIX_GetIDs(self.handle, dimension.value, ids_p)
        return ids

    def __getitem__(self, key: str | int) -> np.ndarray:
        """Get a numpy array of matrix data given a string (table name)
        or integer (zero-based table index)."""
        if isinstance(key, str):
            data = self._read_table(key)
        elif isinstance(key, int):
            data = self._read_table_by_index(key)
        else:
            raise TypeError(
                "Key must be a string (table name) or integer (zero-based table index)."
            )

        match self._missing:
            case ConvertMissing.ZERO:
                self._set_missing_zero(data)  # Modifies data inplace to avoid a copy
            case ConvertMissing.NAN:
                if (
                    self.dtype == _DataType.SHORT_TYPE
                    or self.dtype == _DataType.LONG_TYPE
                ):
                    raise ValueError(
                        "Cannot convert missing to NaN for integer matrix files."
                    )
                self._set_missing_nan(data)  # Modifies data inplace to avoid a copy

        return data

    def _read_table(self, table_name: str) -> np.ndarray:
        """Read a table from a TransCAD matrix file given the table name."""
        try:
            table_index = self.table_names.index(table_name)
        except ValueError:
            raise KeyError(
                f"Table name {table_name} not found in matrix {self.filename}."
            )
        return self._read_table_by_index(table_index)

    def _read_table_by_index(self, table_index: int) -> np.ndarray:
        """Read a table from a TransCAD matrix file given the table index."""

        if table_index < 0 or table_index >= self.table_count:
            raise IndexError(
                f"Table index {table_index} out of range for matrix {self.filename}."
            )

        buffer = np.empty(self.shape, self.np_dtype)
        with _TableAccess(self, table_index):
            if self.index == (0, 0):
                self._read_base_data(table_index, buffer)
            else:
                self._read_indexed_data(table_index, buffer)

        return buffer

    def _read_base_data(self, table_index: int, buffer) -> None:

        for row in range(buffer.shape[0]):
            row_array_p = buffer[row].ctypes.data_as(ctypes.c_void_p)
            rv = self.tcw.MATRIX_GetBaseVector(
                self.handle,
                row,
                _MatrixDim.ROW.value,
                self.dtype.value,
                row_array_p,
            )

            assert rv == 0, f"Failed to read row {row} from table {table_index}."

    def _read_indexed_data(self, table_index: int, buffer) -> None:
        """Read data using the current index."""

        row_ids = self.row_ids
        for row in range(buffer.shape[0]):
            row_array_p = buffer[row].ctypes.data_as(ctypes.c_void_p)
            rv = self.tcw.MATRIX_GetVector(
                self.handle,
                row_ids[row],
                _MatrixDim.ROW.value,
                self.dtype.value,
                row_array_p,
            )

            assert rv == 0, f"Failed to read row {row} from table {table_index}."

    def _set_missing_zero(self, data: np.ndarray) -> None:
        """Convert missing data indicators to zero."""
        np.putmask(data, data == _missing[self.dtype], 0)

    def _set_missing_nan(self, data: np.ndarray) -> None:
        """Convert missing data indicators to NaN."""
        np.putmask(data, data == _missing[self.dtype], np.nan)

    def __setitem__(self, key: str | int, data: np.ndarray) -> None:
        """Set a numpy array of matrix data given a string (table name)
        or integer (zero-based table index)."""

        match self._missing:
            case ConvertMissing.ZERO:
                # Make a copy to avoid modifying the original data
                data = self._set_nan_zero_copy(data)
            case ConvertMissing.NAN:
                # Modifies data inplace to avoid a copy
                data = self._set_nan_missing_copy(data)

        if isinstance(key, str):
            self._write_table(key, data)
        elif isinstance(key, int):
            self._write_table_by_index(key, data)
        else:
            raise TypeError(
                "Key must be a string (table name) or integer (zero-based table index)."
            )

    def _write_table(self, table_name: str, data: np.ndarray) -> None:
        """Write a numpy array to a TransCAD table given the table name"""
        try:
            table_index = self.table_names.index(table_name)
        except ValueError:
            raise KeyError(
                f"Table name {table_name} not found in matrix {self.filename}."
            )
        self._write_table_by_index(table_index, data)

    def _write_table_by_index(self, table_index: int, data: np.ndarray) -> None:
        """Write a numpy array to a TransCAD table given the table index"""

        if table_index < 0 or table_index >= self.table_count:
            raise IndexError(
                f"Table index {table_index} out of range for matrix {self.filename}."
            )

        self._validate_write_data(data)
        data = self._cast_data(data)

        with _TableAccess(self, table_index, read_only=False):
            if self.index == (0, 0):
                self._write_base_data(table_index, data)
            else:
                pass  # self._write_indexed_data(table_index, data)

    def _write_base_data(self, table_index: int, data: np.ndarray) -> None:
        for row in range(data.shape[0]):
            row_array_p = data[row].ctypes.data_as(ctypes.c_void_p)
            rv = self.tcw.MATRIX_SetBaseVector(
                self.handle,
                row,
                _MatrixDim.ROW.value,
                self.dtype.value,
                row_array_p,
            )

            assert rv == 0, f"Failed to write row {row} to table {table_index}."

    def _validate_write_data(self, data: np.ndarray) -> None:
        """Validate that the data is the correct shape and type for writing."""
        self._validate_write_shape(data)
        self._validate_write_dtype(data)

    def _validate_write_shape(self, data: np.ndarray) -> None:
        if data.shape != self.shape:
            raise ValueError(
                f"Data shape {data.shape} does not match matrix shape {self.shape}."
            )

    def _validate_write_dtype(self, data: np.ndarray) -> None:
        """Validate that matrix data type is at least as large as the numpy data type."""

        matrix_dtype = self.dtype
        try:
            data_dtype = _mtx_dtype[data.dtype]
        except KeyError:
            raise ValueError(f"Unsupported data type: {data.dtype}.")

        if matrix_dtype.value < data_dtype.value:
            raise ValueError(
                f"Matrix data type {matrix_dtype.name} is smaller than data type {data_dtype.name} - writing would result in loss of data ."
            )

    def _cast_data(self, data: np.ndarray) -> np.ndarray:
        """Cast the data to the matrix data type."""
        return data.astype(self.np_dtype)

    def _set_nan_zero_copy(self, data: np.ndarray) -> np.ndarray:
        """Convert NaN values to zero."""

        # Create single zero of the same dtype as data
        return np.where(np.isnan(data), 0, data)

    def _set_nan_missing_copy(self, data: np.ndarray) -> np.ndarray:
        """Convert NaN values to missing data."""
        return np.where(np.isnan(data), _missing[self.dtype], data)


class OpenMatrixTC(_BaseMatrixTC):
    """Context manager to open a TransCAD matrix file and close it when done."""

    def __init__(
        self, matrix_file: Path | str, missing: ConvertMissing = ConvertMissing.ZERO
    ):
        # Check for a valid matrix file before proceeding
        # Exit if not found
        matrix_file = Path(matrix_file)
        if not matrix_file.exists():
            raise FileNotFoundError(f"Matrix file not found: {matrix_file}")

        super().__init__(matrix_file, missing=missing)

    def __enter__(self) -> MatrixTC:

        self._init_dll()

        # Open the matrix file
        self.mat = self._open_matrix()
        mat_obj = MatrixTC(self.mat, self._tcw, self._file, self._missing)

        # Check for invalid missing data conversion
        self._validate_missing(mat_obj, self._missing)

        return mat_obj

    def __exit__(self, exc_type, exc_value, traceback) -> bool:

        # Release the matrix
        self._close_matrix(self.mat)

        # Run the parent class exit method
        super().__exit__(exc_type, exc_value, traceback)

        # Returning False propagates exceptions, True suppresses them
        return False

    def _open_matrix(self) -> ctypes.c_void_p:
        """Open a TransCAD matrix file using
        MATRIX  MATRIX_LoadFromFile(char *szFileName, CONTROL_TYPE FileBased);"""

        mat = self._tcw.MATRIX_LoadFromFile(self._file_b, _ControlType.TRUE.value)
        if not mat:
            raise OSError(f"Failed to open matrix file: {self._file}")

        return ctypes.c_void_p(mat)


class CreateMatrixTC(_BaseMatrixTC):
    """Context manager to create a TransCAD matrix file and close it when done."""

    def __init__(
        self,
        matrix_file: Path | str,
        label: str,
        shape: tuple[int, int],
        data_type: _DataType,
        table_count: int,
        row_ids: np.ndarray | list[int] | None = None,
        col_ids: np.ndarray | list[int] | None = None,
        table_names: list[str] | tuple[str, ...] | None = None,
        compression: bool = True,
        missing: ConvertMissing = ConvertMissing.ZERO,
    ):
        # Make sure the filename is valid and writable before proceeding
        # Exit if invald or exists and not replacable
        matrix_file = Path(matrix_file)
        if matrix_file.exists():
            if not os.access(matrix_file, os.W_OK):
                raise PermissionError(f"Matrix file not writable: {matrix_file}")
            os.remove(matrix_file)

        self._label = label
        self._shape = shape
        self._data_type = data_type
        self._table_count = table_count
        self._row_ids = row_ids
        self._col_ids = col_ids
        self._table_names = table_names
        self._compression = compression

        self._validate_inputs()

        super().__init__(matrix_file, missing=missing)

    def __enter__(self) -> MatrixTC:

        self._init_dll()

        self.mat = self._create_matrix()
        mat_obj = MatrixTC(self.mat, self._tcw, self._file, self._missing)

        # Check for invalid missing data conversion
        self._validate_missing(mat_obj, self._missing)

        return mat_obj

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        # Release the matrix
        self._close_matrix(self.mat)

        # Run the parent class exit method
        super().__exit__(exc_type, exc_value, traceback)

        # Returning False propagates exceptions, True suppresses them
        return False

    def _create_matrix(self) -> ctypes.c_void_p:
        """Create a TransCAD matrix file using
        matrix_h = MATRIX_New(...);"""

        matrix_h = self._tcw.MATRIX_New(
            self._file_b,
            self._str_to_bytes(self._label),
            self._shape[0],
            self._process_ids(self._row_ids),
            self._shape[1],
            self._process_ids(self._col_ids),
            self._table_count,
            self._process_string_list(self._table_names),
            self._data_type.value,
            int(self._compression),
        )
        return matrix_h

    # Validate each input to avoid passing invalid data the matrix creation C function
    def _validate_inputs(self) -> None:
        self._validate_label()
        self._validate_shape()
        self._validate_data_type()
        self._validate_table_count()
        self._validate_row_ids()
        self._validate_col_ids()
        self._validate_table_names()
        self._validate_compression()

    def _validate_label(self) -> None:
        if not isinstance(self._label, str):
            raise TypeError("Label must be a string.")
        if len(self._label) > _MAX_FLABEL:
            raise ValueError(f"Label exceeds {_MAX_FLABEL} characters.")

    def _validate_shape(self) -> None:
        if not isinstance(self._shape, tuple):
            raise TypeError(
                "Shape must be a tuple with two values: number of rows and columns."
            )
        if len(self._shape) != 2:
            raise ValueError("Shape must have two values: number of rows and columns.")
        if not all(isinstance(x, int) for x in self._shape):
            raise TypeError("Shape values must be integers.")
        if any(x < 1 for x in self._shape):
            raise ValueError("Shape values must be positive integers.")

    def _validate_data_type(self) -> None:
        if not isinstance(self._data_type, _DataType):
            raise TypeError("Data type must be a _DataType.")

    def _validate_table_count(self) -> None:
        if not isinstance(self._table_count, int):
            raise TypeError("Number of tables must be an integer.")
        if self._table_count < 1:
            raise ValueError("Number of tables must be a positive integer.")

    def _validate_row_ids(self) -> None:
        if self._row_ids is None:
            return
        self._validate_ids(self._row_ids, "Row")

        if len(self._row_ids) != self._shape[0]:
            raise ValueError(
                "Number of row IDs must match the specified number of rows."
            )

    def _validate_col_ids(self) -> None:
        if self._col_ids is None:
            return
        self._validate_ids(self._col_ids, "Column")

        if len(self._col_ids) != self._shape[1]:
            raise ValueError(
                "Number of column IDs must match the specified number of columns."
            )

    def _validate_ids(self, ids, dimension) -> None:
        if not isinstance(ids, list) and not isinstance(ids, np.ndarray):
            raise TypeError(
                f"{dimension} IDs must be a list or numpy array of integers."
            )
        if not all(
            isinstance(x, int) or np.issubdtype(x.dtype, np.integer) for x in ids
        ):
            raise TypeError(f"{dimension} IDs must be integers.")
        if any(x < 0 for x in ids):
            raise ValueError(f"{dimension} IDs must be positive integers.")

    def _validate_table_names(self) -> None:
        if self._table_names is None:
            return
        if not isinstance(self._table_names, list) and not isinstance(
            self._table_names, tuple
        ):
            raise TypeError("Table names must be a list or tuple of strings.")
        if not all(isinstance(x, str) for x in self._table_names):
            raise TypeError("Table names must be a list of strings.")
        if any(len(x) > _MAX_FLABEL for x in self._table_names):
            raise ValueError(f"Table names must not exceed {_MAX_FLABEL} characters.")

        if len(self._table_names) != self._table_count:
            raise ValueError(
                "Number of table names must match the specified number of tables."
            )

    def _validate_compression(self) -> None:
        if not isinstance(self._compression, bool):
            raise TypeError("Compression must be a boolean.")

    # Processing functions for arguments that must be converted to the relevant C types
    def _process_ids(self, ids) -> None | ctypes.c_void_p:
        """Convert a list of integers to a pointer to a C array of integers."""
        if ids is None:
            return None

        if isinstance(ids, list):
            ids = np.array(ids, np.int32)

        # Make sure we have 32-bit integers
        if ids.dtype != np.int32:
            ids = ids.astype(np.int32)

        ids = ids.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        return ctypes.cast(ids, ctypes.c_void_p)

    def _process_string_list(self, string_list) -> ctypes.c_void_p | None:
        """Convert a list of strings to a pointer to a C array of strings."""
        if string_list is None:
            return None

        str_type = ctypes.c_char_p * len(string_list)
        byte_strings = (self._str_to_bytes(x) for x in string_list)

        string_list = str_type(*byte_strings)

        return ctypes.cast(string_list, ctypes.c_void_p)


class _TableAccess:
    """Context manager to access a specific table in a matrix file.
    - Sets the table index on entry and restores it on exit.
    - Uses OpenFile to increase matrix access speed."""

    def __init__(self, mat: MatrixTC, table_index: int, read_only: bool = True):
        self.mat = mat
        self.table_index = table_index
        self.orig_table = None
        self.read_only = read_only

    def __enter__(self):
        self.orig_table = self.mat.tcw.MATRIX_GetCore(self.mat.handle)
        self.mat.tcw.MATRIX_OpenFile(self.mat.handle, self.read_only)
        self.mat.tcw.MATRIX_SetCore(self.mat.handle, self.table_index)
        return None

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        self.mat.tcw.MATRIX_SetCore(self.mat.handle, self.orig_table)
        self.mat.tcw.MATRIX_CloseFile(self.mat.handle)
        return False  # Propagate exceptions
