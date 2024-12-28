"""This file provides a function to write TransCAD FFB tables."""

import pandas as pd
import numpy as np

from model_connector.common import (
    STRING_ENCODING,
    NULL_INT,
    NULL_DOUBLE,
    NULL_FLOAT,
    NULL_SHORT,
    NULL_TINY,
)
from model_connector.common import _get_ffb_dictionary


def write_ffb(df: pd.DataFrame, ffb_file: str) -> None:
    """Write a pandas DataFrame to a TransCAD FFB file. NaN / NaT values are
    converted to the appropriate NULL value for the data type.

    Parameters
    ----------
    df: pd.DataFrame
        The DataFrame to write to the FFB file.
    ffb_file: str
        The path to the FFB file to write.

    """

    # Work with a copy to avoid changing the original dataframe
    df = df.copy()

    # Get information about the data types for each column
    dcb_string, tc_types = _create_dcb_string(df)

    # Check for invalid data types, raise an error if found.
    # Downcast data types as needed, pad strings, convert dates
    # and times to integers. NaT Date/Time values are converted to NULL_INT
    df = _process_dtypes(df, tc_types)

    # Convert NaN float values to appropriate null values
    df = _convert_nulls(df)

    # Process formatting for file writes
    fmt_string = _create_numpy_formats(df)

    # write the bin files
    _write_to_bin(df, fmt_string, dcb_string, ffb_file)


def _process_dtypes(df: pd.DataFrame, tc_types: list[str]) -> pd.DataFrame:
    """Check for invalid data types, raise an error if found.
    Process data types as needed for writing to the FFB file
    """

    valid_dtypes = ["int32", "float64", "int16", "uint8", "float32"]

    # Check for invalid data types
    for col, tc_type in zip(df.columns, tc_types):
        if df[col].dtype in valid_dtypes:
            continue

        elif df[col].dtype == "int64":
            df[col] = _downcast(df[col], "int32")

        elif df[col].dtype == "object" and _is_pd_string(df[col]):
            df[col] = _pad_strings(df[col])

        elif df[col].dtype == "datetime64[ns]" or df[col].dtype == "datetime64[ms]":
            if df[col].dtype != "datetime64[ms]":
                # convert to milliseconds if needed
                df[col] = df[col].astype("datetime64[ms]")
            if tc_type == "Date":
                # Convert date to integer YYYYMMDD, handling None
                df[col] = _convert_date(df[col])

            elif tc_type == "Time":
                # Convert time to ingeger, ms since midnight, handling None
                df[col] = _convert_time(df[col])

            elif tc_type == "DateTime":
                df = _convert_datetime(df, col)

        else:
            raise DataframeFormatError(
                f"Column {col} has an unsupported type {df[col].dtype}"
            )

    return df


def _downcast(series: pd.Series, dtype: str) -> pd.Series:
    """Downcast a series to a smaller dtype if possible, otherwise raise an error"""

    if series.max() > np.iinfo(dtype).max:
        raise ValueError(
            f"Column {series.name} max value is too large for dtype {dtype} and cannot be written to a TransCAD FFB File"
        )

    if series.min() < np.iinfo(dtype).min:
        raise ValueError(
            f"Column {series.name} min value is too small for dtype {dtype} and cannot be written to a TransCAD FFB File"
        )

    series = series.astype(np.dtype(dtype))

    return series


def _datetime_type(series: pd.Series) -> str:
    """Determine the appropriate datetime type for a given series.
    Times all have a date of 1970-01-01, so only the time is stored.
    Dates all have a time of.
    """

    zero_time = pd.Timestamp("1970-01-01")

    # Check if all times are 00:00:00
    if all((series.dt.time == zero_time.time()) | series.isnull() | series.isna()):
        return "date"

    # Check if all dates are 1970-01-01
    if all((series.dt.date == zero_time.date()) | series.isnull() | series.isna()):
        return "time"

    # If neither of the above are true, the field contains both date and time
    return "datetime"


def _convert_date(series: pd.Series) -> pd.Series:
    """Convert a datetime series to a date series, handling None/NaN values"""
    return series.apply(
        lambda x: x.strftime("%Y%m%d") if not pd.isnull(x) else NULL_INT
    ).astype("int32")


def _convert_time(series: pd.Series) -> pd.Series:
    """Convert a datetime series to a time series, handling None/NaN values"""
    return series.apply(
        lambda x: x.asm8.astype("int32") if not pd.isnull(x) else NULL_INT
    ).astype("int32")


def _convert_datetime(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Convert a datetime column to separate date and time columns, each as int32"""

    date = _convert_date(df[col])

    # Time portion of DateTime is converted by subtracting the date, different process than standalone DateTime
    time = df[col] - pd.to_datetime(df[col].dt.strftime("%Y-%m-%d"))
    time = np.where(
        date == NULL_INT, NULL_INT, (time.dt.total_seconds() * 1000)
    )  # 1000 = sec to ms
    time = time.astype("int32")

    df[col] = date
    df = df.rename(columns={col: f"{col}_date"})
    col_idx = df.columns.get_loc(f"{col}_date")
    assert isinstance(col_idx, int)
    df.insert(col_idx + 1, f"{col}_time", time)

    return df


def _convert_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Convert null values to the appropriate value for the data type"""

    for col in df.columns:

        if df[col].dtype == "float64":
            df[col] = df[col].fillna(NULL_DOUBLE).astype("float64")

        elif df[col].dtype == "float32":
            df[col] = df[col].fillna(NULL_FLOAT).astype("float32")

        elif df[col].dtype == "object":
            if _is_pd_string(df[col]):
                df[col] = df[col].fillna("")

            elif _is_pd_bytestring(df[col]):
                df[col] = df[col].fillna(b"")

        # elif df[col].dtype == "datetime64[ns]" or df[col].dtype == "datetime64[ms]":
        #    df[col] = df[col].fillna(NULL_INT).astype("int32")

    return df


def _create_numpy_formats(df: pd.DataFrame) -> str:
    """Create a format string for use in binary writing"""

    valid_types: dict[str, str] = {
        "int32": "<i4",
        "float64": "<f8",
        # C - special case
        "int16": "<i2",
        "uint8": "<u1",
        "float32": "<f4",
        # "DateTime" - special cases
    }

    fmt_string = ""

    for col in df.columns:
        s_type = str(df[col].dtype)
        if s_type in valid_types:
            fmt_string += valid_types[s_type]

        elif s_type == "object" and _is_pd_bytestring(df[col]):
            # define based on the longest string in the column
            max_len = np.max(df[col].str.len())
            fmt_string += f"S{max_len}"

        elif s_type == "datetime64[ns]":
            raise NotImplementedError  # TODO: Implement
            # - but should now be int types since processed before this

        else:
            raise DataframeFormatError(
                f"Column {col} has an unsupported type {df[col].dtype}"
            )

    return fmt_string


def _create_dcb_string(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Create a DCB string for use in the TransCAD file"""

    # Format starts with a blank line followed by the record size in bytes
    dcb_lines = ["", 0]
    tc_types = []
    loc_counter = 1
    # type, length, index flag, digits, decimal places, aggregation rule
    valid_types: dict[str, tuple[str, int, int, int, int, str]] = {
        "int32": ("I", 4, 0, 8, 0, "Sum"),
        "int64": ("I", 4, 0, 8, 0, "Sum"),  # downcast, fail if it overflows
        "float64": ("R", 8, 0, 10, 2, "Sum"),
        # C - special case
        "int16": ("S", 2, 0, 6, 0, "Sum"),
        "uint8": ("S", 1, 0, 4, 0, "Sum"),
        "float32": ("F", 4, 0, 10, 2, "Sum"),
        # "DateTime" - special cases
    }

    for col in df.columns:
        s_type = str(df[col].dtype)
        if s_type in valid_types:
            # field name, str type, starting position, length, index flag, digits, decimal places, [null, "", "", null], aggregation rule

            dcb_lines.append(_dcb_line(col, valid_types[s_type], loc_counter))
            tc_types.append(valid_types[s_type][0])
            loc_counter += valid_types[s_type][1]

        elif s_type == "object" and _is_pd_string(df[col]):
            # define based on the longest string in the column
            str_len = np.max(df[col].str.len())
            fld_def = ("C", str_len, 0, str_len, 0, "Copy")
            dcb_lines.append(_dcb_line(col, fld_def, loc_counter))
            tc_types.append(fld_def[0])
            loc_counter += str_len

        elif s_type == "datetime64[ns]" or s_type == "datetime64[ms]":
            dt_type = _datetime_type(df[col])
            if dt_type == "date":
                fld_def = ("Date", 4, 0, 12, 0, "Copy")

            elif dt_type == "time":
                fld_def = ("Time", 4, 0, 12, 0, "Copy")

            elif dt_type == "datetime":
                fld_def = ("DateTime", 8, 0, 22, 0, "Copy")
            else:
                raise ValueError(f"Unknown datetime type {dt_type}")

            dcb_lines.append(_dcb_line(col, fld_def, loc_counter))
            tc_types.append(fld_def[0])
            loc_counter += fld_def[1]

        else:
            raise DataframeFormatError(
                f"Column {col} has an unsupported type {df[col].dtype}"
            )

    dcb_lines[1] = str(loc_counter - 1)  # Set the record size in bytes

    return dcb_lines, tc_types


def _dcb_line(name: str, fld_def: tuple, pos: int) -> str:
    [ftype, length, index_flag, digits, decimal_places, aggregation_rule] = [
        str(x) for x in fld_def
    ]
    nulls = ',"","",'  # TransCAD indicators Not used by this function, left blank

    return ",".join(
        [
            f'"{name}"',
            ftype,
            f"{pos:.0f}",
            length,
            index_flag,
            digits,
            decimal_places,
            nulls,
            aggregation_rule,
        ]
    )


def _convert_datetime_to_tc(df: pd.DataFrame) -> pd.DataFrame:
    pass
    raise NotImplementedError


def _pad_strings(series: pd.Series) -> pd.Series:
    """pad a string column to the max length, converting None/NaN strings to all spaces"""

    series = series.fillna("")
    max_len = np.max(series.str.len())
    series = series.str.pad(max_len, fillchar=" ", side="right")
    series = series.str.encode(STRING_ENCODING)

    return series


def _is_pd_string(data: pd.Series) -> bool:
    if isinstance(data.dtype, pd.StringDtype):
        return True

    elif data.dtype == "object":
        try:
            return all(isinstance(v, str) or (v is None) or np.isnan(v) for v in data)
        except Exception:
            # address arbitrary objects that cannot be checked for nan
            return False

    else:
        return False


def _is_pd_bytestring(data: pd.Series) -> bool:

    if data.dtype == "object":
        try:
            return all(isinstance(v, bytes) for v in data)
        except Exception:
            # address arbitrary objects that cannot be checked
            return False
    else:
        return False


def _write_to_bin(
    df: pd.DataFrame, fmt_string: str, dcb_string: list[str], ffb_file: str
) -> None:
    """Write a FFB file given an already processed/checked dataframe, format string, and DCB string"""

    # Set type for strings in pandas to numpy conversion
    dtypes = {}
    for col in df.columns:
        if df[col].dtype == "object":
            if not _is_pd_bytestring(df[col]):
                raise DataframeFormatError(
                    f"Column {col} has an unsupported type {df[col].dtype}"
                )
            # Get max length of string (again)
            max_len = np.max(df[col].str.len())
            dtypes[col] = f"S{max_len}"

    data = df.to_records(
        index=False, column_dtypes=dtypes
    )  # to_records preserves data types

    # Open both bin and dict file at the same time so if one is locked, the whole
    # operation will fail.
    with (
        open(ffb_file, "wb") as bin_f,
        open(_get_ffb_dictionary(ffb_file), "w") as dict_f,
    ):
        data.tofile(ffb_file, format=fmt_string)
        dict_f.write("\n".join(dcb_string))
        data.tofile(bin_f, format=fmt_string)

    return None


class DataframeFormatError(Exception):
    """Raised when a dataframe contains one or more field types that cannot be written to a FFB file"""

    pass


if __name__ == "__main__":

    max_flt = 2_147_483_647
    over_flt = max_flt + 1

    df = pd.DataFrame(
        {
            "fld_int": [1, 2, 3, 4, 5],
            "fld str": ["one", None, "three", np.nan, "fiveVeryLongString"],
            "fld,real": [1.1, None, 3.3, 4.4, 5.5],
            "fld_date": [
                pd.Timestamp("2021-01-01"),
                pd.Timestamp("2022-01-02"),
                # pd.Timestamp("2023-01-03"),
                None,
                pd.Timestamp("2024-01-04"),
                pd.Timestamp("2025-01-05"),
            ],
            "fld_time": [
                pd.Timestamp("1970-01-01 13:02:59"),
                pd.Timestamp(5000, unit="ms"),
                pd.Timestamp(6000, unit="ms"),
                # pd.Timestamp(7000, unit="ms"),
                None,
                pd.Timestamp(8000, unit="ms"),
            ],
            "fld_datetime": [
                pd.Timestamp("2021-01-01 00:00:00"),
                # pd.Timestamp("2021-01-02 01:00:00"),
                None,
                pd.Timestamp("2021-01-03 02:00:00"),
                pd.Timestamp("2021-01-04 03:00:00"),
                pd.Timestamp("2021-01-05 23:59:59"),
            ],
        }
    )

    write_ffb(df, "tests/test_data/not_real.bin")
