# model-connector: Library for accessing travel model data

## Installation:

Install using pip

```pip install model-connector```

## Use Cases
 - **TransCAD fixed format binary tables:** fast read and write using pandas dataframes.
 - **TransCAD matrix files:** read a TransCAD matrix into a numpy array _(beta)_


## TransCAD Binary Files

### Reading from a TransCAD binary file

```python
import model_connector as mc

# Read a TransCAD fixed format binary file into a dataframe, 
# retaining null values
df = mc.read_ffb("myfile.bin")

# Read a TransCAD fixed format binary file into a dataframe, 
# converting null values to zeros
dfz = mc.read_ffb("myfile.bin", null_to_zero=True)
```

### Writing to a TransCAD binary file
```python
import model_connector as mc
import pandas as pd

df = pd.DataFrame({"ID":[1,2,3], 
                   "RealField":[1.1, 2.2, 3.3, ],
                   "IntField":[1, 2, 3],
                   "DateField":[20210101, 20210115, 20210130],
                   "DateTimeField":[pd.Timestamp("2021-01-01 00:00:05"),
                                    pd.Timestamp("2021-01-15 00:10:05"),
                                    pd.Timestamp("2021-01-30 00:20:05")]})

mc.write_ffb(df, "sample_output.bin")
```
## TransCAD Matrix Files
Matrix access requires TransCAD 9 or greater with a valid license.

### Reading a TransCAD Matrix File
```python
import model_connector as mc
import numpy as np

# Reading a TransCAD matrix into a dictionary of numpy arrays, 
# using the default behavior of converting null to zero.
matrix = mc.read_matrix_tc("myfile.mtx")
for table in matrix.keys():
    print(f"Sum of {table} = {matrix[table].sum()}" )

# Reading a TransCAD matrix into a pandas dataframe
df = mc.read_matrix_tc("myfile.mtx", format="df")
print(df.head())

# Optionally Convert null to NAN. This will fail for integer matrices since
# numpy doesn't support NAN in integer arrays.
matrix_withnan = mc.read_matrix_tc("myfile.mtx", missing="nan")
for table in matrix_withnan.keys():
    print(f"Sum of {table} = {matrix_withnan[table].sum()}" )

# By default, all matrix tables are loaded. Use the tables parameter to load only
# some matrix tables.
matrix_autos = mc.read_matrix_tc("myfile.mtx", tables=["DA", "SR2", "SR3p"])
for table in matrix_autos.keys():
    print(f"Sum of {table} = {matrix_autos[table].sum()}" )

# By default, data is read using the base index. Use the row_index and 
# col_index parameters to read data using a different index.
# Indices must be specified as an integer. the base index is 0, and
# the remaining indices are ordered as returned by GetMatrixIndexNames()
# in GISDK.

matrix_subset = mc.read_matrix_tc("myfile.mtx", row_index=1, col_index=1)
for table in matrix_subset.keys():
    print(f"Sum of {table} = {matrix_subset[table].sum()}" )

print(f"Shape of matrix is {matrix_subset["DA"].shape}")

```

### Writing a TransCAD Matrix File

```python
import model_connector as mc
import numpy as np

# Writing a dictionary of numpy arrays to a TransCAD matrix
matrix = {"DA": np.random.rand(10, 10), "SR2": np.random.rand(10, 10)}
mc.write_matrix_tc("my_out_file.mtx", matrix)

# Optionally provide row and column ids. The default is a sequence starting at 1
row_ids = np.arange(1, 11, 1)
col_ids = np.arange(10, 110, 10)
mc.write_matrix_tc("my_indexed_file.mtx", matrix, row_ids=row_ids, col_ids=col_ids)
```

### Specifying the TransCAD Installation 

The TransCAD matrix functions search the system registry to locate a TransCAD installation. If the matrix functions fail even with a valid installation, this may be due to multiple versions or licensing methods being present on the computer. 

The TransCAD program location can be specified using `set_tcpath()`. The current path can be obtained using `get_tcpath()`. If the path is not set manually, `get_tcpath()` will report the detected version of TransCAD.

```python
# Set the TransCAD location as shown below
import model_connector as mc
mc.set_tcpath("C:/Program Files/TransCAD 10.0/tcw.exe")
print("TransCAD Path: ", mc.get_tcpath())
```