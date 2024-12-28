"""This file provides a function to read TransCAD FFB tables."""

import csv
import io
import os
import warnings

import numpy as np
import pandas as pd

from model_connector.common import (
    STRING_ENCODING,
    DELETE_FLAG,
    MIN_DELETE_LENGTH,
    NULL_INT,
    NULL_DOUBLE,
    NULL_FLOAT,
    NULL_SHORT,
    NULL_TINY,
)
from model_connector.common import _get_ffb_dictionary


def read_ffb(ffb_file: str, null_to_zero: bool = False) -> pd.DataFrame:
    """Read a FFB file and return a pandas DataFrame.

    Parameters
    ----------
    ffb_file : str
        The path to the FFB file to read.
    null_to_zero : bool, optional
        Whether to replace null values with zeros, by default False

    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the data from the FFB file.

    The `null_to_zero` parameter determines whether null values are replaced
    with zeros. When `null_to_zero` is `False`, null values from TransCAD are
    converted to `NaN`, or `NaT` for dates and times. When `null_to_zero` is
    `True`, null values in numeric columns areconverted to zeros, null values
    in string columns are left as empty strings, and null values in date and
    time columns are converted to `NaT`.

    Because numpy/pandas does not support NaN values in integer columns, null
    values will be left at their TransCAD indicator values unless `null_to_zero`
    is `True`.

    """

    # Get the table structure from the DCB file
    field_def = _get_table_structure(ffb_file)
    data_types = _get_datatypes(field_def)
    record_length = sum([x[2] for x in field_def])

    # Load data from file
    bytedata = _read_bytedata(ffb_file)
    bytedata = _remove_deleted_records(bytedata, record_length)

    # Convert the bytes to a pandas dataframe
    df = _bytes_to_dataframe(bytedata, data_types)

    # Address null values
    df = _check_nulls(df, field_def, null_to_zero)

    # Address strings, dates, and times
    for name, type, length in field_def:
        if type == "C":  # Trim whitespace
            df = _process_string(df, name, null_to_zero)
        elif type == "Date":
            df = _process_date(df, name)
        elif type == "Time":
            df = _process_time(df, name)
        elif type == "DateTime":
            df = _process_datetime(df, name)

    return df


def _get_table_structure(ffb_file: str) -> list[tuple[str, str, int]]:
    """Given a FFB filename, return a list of fields, each with [name, type, length]"""

    dict_file = _get_ffb_dictionary(ffb_file)

    # Read lines into an array
    with open(dict_file, "r") as f:
        lines = f.readlines()

    ## ---- Data integrity checks ----
    # Remove the first line
    # Usually blank, but DCB files attached to a geographic file sometimes have the file label on the first line
    lines.pop(0).strip()

    # Get the record length
    record_length = lines.pop(0).strip()
    try:
        record_length = int(record_length)
    except ValueError:
        fname = os.path.basename(ffb_file)
        warn = f"File {fname} appears to use an older, untested file firmat.\n" + \
                "Use data with caution, and consider re-exporting the file from TransCAD."
        warnings.warn(warn, stacklevel=3)

        try:
            record_length = int(record_length.split(",")[0])
        except ValueError:
            raise FileFormatError("Second line of dictionary file must be an integer")

    # ---- Read the dictionary file ----
    # Read remaining lines into a list of lists using the csv module
    # Place relevant data (name, type, length) into a list.
    field_def: list[tuple[str, str, int]] = list()
    reader = csv.reader(lines, delimiter=",", quotechar='"')
    for row in reader:
        try:
            field_def.append((row[0], row[1], int(row[3])))
        except ValueError:
            raise FileFormatError("Error parsing dictionary file")

    # ---- Data integrity checks ----
    # Verify that the sum of the lengths is equal to the record length
    if sum([x[2] for x in field_def]) != record_length:
        raise FileFormatError("Sum of field lengths does not equal record length")

    # ---- Complete ----
    return field_def


def _get_datatypes(field_def: list[tuple[str, str, int]]) -> list[tuple[str, str]]:
    """Get datatypes formated for use in numpy binary read, each element is
    (field_name, numpy_type) where numpy type is a string like "<i4" or "<f8" """

    dt: list[tuple[str, str]] = []
    valid_types: dict[tuple[str, int], str] = {
        ("I", 4): "<i4",
        ("R", 8): "<f8",
        # "C"
        ("S", 2): "<i2",
        ("S", 1): "<u1",
        ("F", 4): "<f4",
        ("Date", 4): "<i4",
        ("Time", 4): "<i4",
        # "DateTime"
    }

    # Non-standard types for character and datetime
    for name, type, length in field_def:
        if (type, length) in valid_types:
            dt.append((name, valid_types[(type, length)]))
        elif type == "C":
            dt.append((name, f"S{length}"))
        elif type == "DateTime":
            dt.append((name + "_date", "<i4"))
            dt.append((name + "_time", "<i4"))
        else:
            raise FileFormatError(f"Invalid or unknown type for field {name}")

    return dt


def _read_bytedata(ffb_file: str) -> bytes:
    with open(ffb_file, "rb") as f:
        bytedata = f.read()

    return bytedata


def _remove_deleted_records(bytedata: bytes, record_length: int) -> bytes:
    """Look for and remove deleted records"""

    # TransCAD will only allow deleted records if the record length isat least 6 bytes
    if record_length < MIN_DELETE_LENGTH:
        return bytedata

    # If records are less than 16 bytes, the delete pattern is truncated
    delete_pattern = DELETE_FLAG[:record_length]

    start_position = 0
    upd_data = io.BytesIO()

    look_for_deleted_records = True
    while look_for_deleted_records:
        end_position = bytedata.find(delete_pattern, start_position)
        if end_position == -1:
            look_for_deleted_records = False
            upd_data.write(bytedata[start_position:])
        else:
            upd_data.write(bytedata[start_position:end_position])
            start_position = end_position + record_length

    upd_data.seek(0)
    return upd_data.read()


def _bytes_to_dataframe(
    bytedata: bytes, data_types: list[tuple[str, str]]
) -> pd.DataFrame:
    return pd.DataFrame(np.frombuffer(bytedata, dtype=data_types))


def _process_string(
    df: pd.DataFrame, field_name: str, null_to_zero: bool
) -> pd.DataFrame:
    """Process a string field in a DataFrame to remove whitespace, decode from
    bytes, and set empty strings to NaN."""

    df[field_name] = df[field_name].str.decode(STRING_ENCODING).str.strip()
    if not null_to_zero:
        df.loc[df[field_name] == "", field_name] = np.nan

    return df


def _process_date(df: pd.DataFrame, field_name: str) -> pd.DataFrame:
    """Process a date field in a DataFrame to convert from TransCAD format to datetime"""
    df[field_name] = pd.to_datetime(
        df[field_name].astype(str), format="%Y%m%d", errors="coerce"
    )
    return df


def _process_time(df: pd.DataFrame, field_name: str) -> pd.DataFrame:
    """Process a time field in a DataFrame to convert from TransCAD format to datetime"""
    df[field_name] = df[field_name].replace(NULL_INT, np.nan)
    df[field_name] = pd.to_datetime(df[field_name], unit="ms")
    return df


def _process_datetime(df: pd.DataFrame, field_name: str) -> pd.DataFrame:
    """Process a datetime field in a DataFrame to convert from TransCAD format to datetime"""

    # use .loc to only process rows where the date is not null
    not_null = df[field_name + "_date"] != NULL_INT
    df.loc[not_null, field_name] = pd.to_datetime(
        df.loc[not_null, field_name + "_date"].astype(str),
        errors="coerce",
        format="%Y%m%d",
    ) + pd.to_timedelta(df.loc[not_null, field_name + "_time"], unit="ms")

    df = df.drop(columns=[field_name + "_date", field_name + "_time"])
    return df


def _check_nulls(
    df: pd.DataFrame, field_def: list[tuple[str, str, int]], null_to_zero: bool
) -> pd.DataFrame:
    """Convert special values to NaN (null in TransCAD)"""

    null_types: dict = {
        ("I", 4): NULL_INT,
        ("R", 8): NULL_DOUBLE,
        # "C"
        ("S", 2): NULL_SHORT,
        ("S", 1): NULL_TINY,
        ("F", 4): NULL_FLOAT,
        # "Date"
        # "Time"
        # "DateTime"
    }

    if null_to_zero:
        null_replacement = 0
    else:
        null_replacement = np.nan

    for name, type, length in field_def:
        if (type, length) in null_types:
            df[name] = df[name].replace(null_types[(type, length)], null_replacement)

    return df


class FileFormatError(Exception):
    """Raised when a file format error is encountered."""

    pass


if __name__ == "__main__":
    ffb_file = r"C:/test.bin"
    print(_get_ffb_dictionary(ffb_file))
