""" This module provides functions to set up TransCAD matrix access. 
TODO: Add a lock to prevent multiple threads from setting the path at the same time."""

import ctypes
from ctypes import windll
import os
from pathlib import Path
import winreg

from model_connector.common import ConvertMissing, _DataType

_MIN_TC_VERSION = 9.0
_DLL_NAME = "CaliperMTX.dll"
_REG_MAIN_KEY = winreg.HKEY_LOCAL_MACHINE
_REG_KEY = r"SOFTWARE\Caliper Corporation\TransCAD"
_PATH_KEY = "Installed In"

_dll_path: str = ""


def set_tcpath(tcw_path: str) -> None:
    """Sets up TransCAD matrix access based on the path to the TransCAD executable, usually tcw.exe."""
    global _dll_path

    if not os.path.isfile(tcw_path):
        raise TransCADNotFoundError(f"TransCAD not found at {tcw_path}.")

    tcw_path = os.path.dirname(tcw_path)
    dll_path = os.path.join(tcw_path, _DLL_NAME)
    _validate_path(dll_path)
    _dll_path = dll_path


def get_tcpath() -> str:
    """Returns the TransCAD DLL path. If not already set, tries to find it."""
    global _dll_path

    if not _dll_path:
        _dll_path = _find_transcad()

    return _dll_path


def _find_transcad() -> str:
    """Tries to find the TransCAD program by searching the registry.
    Returns the path if found, otherwise raises an error."""
    key = _open_transcad_registry_key()
    installed_versions = _get_installed_versions(key)
    max_version = _get_max_version(installed_versions)
    path = _get_installation_path(key, max_version)
    key.Close()

    path = os.path.join(path, _DLL_NAME)
    _validate_path(path)
    return path


def _open_transcad_registry_key() -> winreg.HKEYType:
    """Opens the TransCAD registry key and returns it."""
    reg = winreg.ConnectRegistry(None, _REG_MAIN_KEY)
    try:
        key = winreg.OpenKey(reg, _REG_KEY)
    except FileNotFoundError:
        raise TransCADNotFoundError

    reg.Close()
    return key


def _get_installed_versions(key: winreg.HKEYType) -> list[str]:
    """Returns a list of installed TransCAD versions."""
    try:
        version_count = winreg.QueryInfoKey(key)[0]
        version_list = [winreg.EnumKey(key, i) for i in range(version_count)]
    except OSError:
        raise TransCADNotFoundError
    if not version_list:
        raise TransCADNotFoundError

    return version_list


def _get_max_version(version_list: list[str]) -> str:
    """Returns a string representing the highest version from a list of version strings."""
    valid_versions = [ver for ver in version_list if _is_value_string(ver)]

    if not valid_versions:
        raise TransCADNotFoundError

    max_version = max(valid_versions, key=lambda ver: float(ver))

    if float(max_version) < _MIN_TC_VERSION:
        raise TransCADNotFoundError(
            f"TransCAD version must be at least {_MIN_TC_VERSION}."
        )

    return max_version


def _is_value_string(ver: str) -> bool:
    """Checks if a version string can be converted to a float."""
    try:
        float(ver)
        return True
    except ValueError:
        return False


def _get_installation_path(key: winreg.HKEYType, version: str) -> str:
    """Returns the installation path for the given version."""
    try:
        key = winreg.OpenKey(key, version)
        path = winreg.QueryValueEx(key, _PATH_KEY)[0]
    except OSError:
        raise TransCADNotFoundError
    return path


def _validate_path(path: str) -> None:
    """Validates the installation path."""
    if not os.path.exists(path):
        raise TransCADNotFoundError(f"TransCAD matrix DLL not found at {path}.")


class TransCADNotFoundError(FileNotFoundError):
    """Exception raised when TransCAD is not found."""

    def __init__(
        self,
        message="TransCAD installation not found. Please provide the path using set_tcpath.",
    ):
        self.message = message
        super().__init__(self.message)


class _BaseMatrixTC:
    """Context manager to open a TransCAD matrix file and close it when done.
    This base class is used to define the DLL functions and parameters and
    should not be created directly. Instead, use it as a base class for
    open and create matrix context managers."""

    def __init__(self, matrix_file: Path, missing: ConvertMissing) -> None:
        self._file = matrix_file
        self._file_b = self._str_to_bytes(str(matrix_file))
        self._missing = missing

    def __exit__(self, exc_type, exc_value, traceback) -> bool:

        # Unload the matrix DLL
        self._unload_dll()
        return False  # Do not supress exceptions

    def _init_dll(self) -> None:
        self._dll_path = get_tcpath()
        self._tcw = self._load_dll()
        self._define_dll_params()

    def _load_dll(self) -> ctypes.WinDLL:
        """Load the TransCAD matrix DLL."""
        tcw = windll.LoadLibrary(self._dll_path)

        ignored = ctypes.pointer(ctypes.c_short(0))
        tcw.InitMatDLL(ignored)
        return tcw

    def _unload_dll(self) -> None:
        """Unload the TransCAD matrix DLL."""
        self._tcw.UnloadMatDLL()

    def _close_matrix(self, mat) -> None:
        """Close a transcad matrix file using
        short   MATRIX_Done(MATRIX  hMatrix);"""

        rv = self._tcw.MATRIX_Done(mat)

        if rv:
            raise OSError(f"Failed to release matrix file: {self._file}")
    
    def _validate_missing(self, mat_obj, missing) -> None:
        """Validate the missing data conversion."""
        if not isinstance(missing, ConvertMissing):
            raise ValueError("missing must be a ConvertMissing enum.")
        
        if missing == ConvertMissing.NAN and (
            mat_obj.dtype == _DataType.SHORT_TYPE
            or mat_obj.dtype == _DataType.LONG_TYPE
        ):
            self.__exit__(None, None, None)
            raise ValueError("Cannot convert missing data to NaN for integer data types.")

    def _define_dll_params(self) -> None:

        # This defines the arguments and return values of the TransCAD matrix functions

        # Initializes the matrix dll.  This function used to
        # accept an integer pointer argument, but it is ignored.
        # void    InitMatDLL(int *ignored);
        self._tcw.InitMatDLL.argtypes = [ctypes.POINTER(ctypes.c_short)]
        self._tcw.InitMatDLL.restype = None

        # Call UnloadMatrixDLL when you are done using the DLL.  Among
        # other things, this releases the license.
        # void UnloadMatDLL();
        self._tcw.UnloadMatDLL.argtypes = []
        self._tcw.UnloadMatDLL.restype = None

        # MATRIX_GetInfo
        #
        #  PARAMETERS:
        #      hMatrix    - matrix handle
        #      Info    - pointer to structure to fill
        #
        #  DESCRIPTION:
        #       Fills a matrix info structure based on 'hMatrix'.
        #
        #  RETURNS:
        #      Nothing.
        # void MATRIX_GetInfo(MATRIX hMatrix, MAT_INFO *Info);
        self._tcw.MATRIX_GetInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self._tcw.MATRIX_GetInfo.restype = None

        # Read a matrix from a file.
        # The last argument can be used to force the loading mode of a dense matrix.
        # If it is passed as CONTROL_AUTOMATIC, the mode is read from the file.
        # If the stored file was created in memory, it will be read into memory.
        # A file-based matrix remains in the file (only the header is read).
        # MATRIX  MATRIX_LoadFromFile(char *szFileName, CONTROL_TYPE FileBased);
        self._tcw.MATRIX_LoadFromFile.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self._tcw.MATRIX_LoadFromFile.restype = ctypes.c_void_p

        # Decrements the matrix reference count and closes the matrix if the
        #      reference count is zero
        # short   MATRIX_Done(MATRIX  hMatrix);
        self._tcw.MATRIX_Done.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_Done.restype = ctypes.c_short

        # Returns the matrix file name.
        # void    MATRIX_GetFileName(MATRIX  hMatrix, char *szFileName);
        self._tcw.MATRIX_GetFileName.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self._tcw.MATRIX_GetFileName.restype = None

        # Returns the number of dim indices
        # short MATRIX_GetNIndices(MATRIX m, MATRIX_DIM dim);
        self._tcw.MATRIX_GetNIndices.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self._tcw.MATRIX_GetNIndices.restype = ctypes.c_short

        # Returns the number of cores in the matrix.
        # short   MATRIX_GetNCores(MATRIX  hMatrix);
        self._tcw.MATRIX_GetNCores.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetNCores.restype = ctypes.c_short

        # Returns the number of rows in the matrix.
        # short   MATRIX_GetNRows(MATRIX  hMatrix);
        self._tcw.MATRIX_GetNRows.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetNRows.restype = ctypes.c_short

        # Returns the number of columns in the matrix.
        # short   MATRIX_GetNCols(MATRIX  hMatrix);
        self._tcw.MATRIX_GetNCols.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetNCols.restype = ctypes.c_short

        # Returns the number of rows in the matrix core.
        # long    MATRIX_GetBaseNRows(MATRIX hMatrix);
        self._tcw.MATRIX_GetBaseNRows.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetBaseNRows.restype = ctypes.c_long

        # Returns the number of columns in the matrix core.
        # long    MATRIX_GetBaseNCols(MATRIX hMatrix);
        self._tcw.MATRIX_GetBaseNCols.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetBaseNCols.restype = ctypes.c_long

        # Returns an array of index IDs for the matrix.
        # short   MATRIX_GetIDs(MATRIX hMatrix, MATRIX_DIM dim,  long *ids);
        self._tcw.MATRIX_GetIDs.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_long),
        ]
        self._tcw.MATRIX_GetIDs.restype = ctypes.c_short

        # Returns the data type of the elements in the matrix.
        # DATA_TYPE   MATRIX_GetDataType(MATRIX hMatrix);
        self._tcw.MATRIX_GetDataType.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetDataType.restype = ctypes.c_int

        # Tests whether the matrix is in column-major order.
        # int    MATRIX_IsColMajor(MATRIX hMatrix);
        self._tcw.MATRIX_IsColMajor.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_IsColMajor.restype = ctypes.c_int

        # Sets the internal currency to the specified core.
        # short MATRIX_SetCore(MATRIX hMatrix, short iCore);
        self._tcw.MATRIX_SetCore.argtypes = [ctypes.c_void_p, ctypes.c_short]
        self._tcw.MATRIX_SetCore.restype = ctypes.c_short

        # Gets the index of the current core.
        # short MATRIX_GetCore(MATRIX hMatrix);
        self._tcw.MATRIX_GetCore.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_GetCore.restype = ctypes.c_short

        # Fills p with the value of the cell at (idRow, idCol) converted to Type.
        # short MATRIX_GetElement(MATRIX hMatrix, long idRow, long idCol, DATA_TYPE Type, void *p);
        self._tcw.MATRIX_GetElement.argtypes = [
            ctypes.c_void_p,
            ctypes.c_long,
            ctypes.c_long,
            ctypes.c_int,
            ctypes.c_void_p,
        ]
        self._tcw.MATRIX_GetElement.restype = ctypes.c_short

        # Reads a row or column of a matrix using the base index.
        # Arguments:
        #     iPos    -   the core position of the row or the column.
        #     dim     -   dimension to extract: MATRIX_ROW or MATRIX_COL.
        #     Type    -   Requested data type of returned values.
        #     Array   -   Previously allocated array for receiving values.
        # short MATRIX_GetBaseVector(MATRIX hMatrix, long iPos, MATRIX_DIM dim, DATA_TYPE Type, void *Array);
        self._tcw.MATRIX_GetBaseVector.argtypes = [
            ctypes.c_void_p,
            ctypes.c_long,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_void_p,
        ]
        self._tcw.MATRIX_GetBaseVector.restype = ctypes.c_short

        # Reads a row or column of a matrix using the current index.
        #     ID      -   the identifier of the row or the column.
        #     dim     -   dimension to extract: MATRIX_ROW or MATRIX_COL.
        #     Type    -   Requested data type of returned values.
        #     Array   -   Previously allocated array for receiving values.
        # short MATRIX_GetVector(MATRIX hMatrix, long ID, MATRIX_DIM dim, DATA_TYPE Type, void *Array);
        self._tcw.MATRIX_GetVector.argtypes = [
            ctypes.c_void_p,
            ctypes.c_long,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_void_p,
        ]
        self._tcw.MATRIX_GetVector.restype = ctypes.c_short

        # Arguments:
        #     iCore   -   the index of the matrix core to use
        #     ID      -   the identifier of the row or the column.
        #     dim     -   dimension to extract: MATRIX_ROW or MATRIX_COL.
        #     Type    -   Requested data type of returned values.
        #     Array   -   Previously allocated array for receiving values.
        # short MATRIX_GetBaseVectorFromCore(MATRIX hMatrix, long iCore, long ID, MATRIX_DIM dim, DATA_TYPE Type, void *Array);
        # **** NOT FOUND IN TC10 DLL *****
        ## self._tcw.MATRIX_GetBaseVectorFromCore.argtypes = [
        ##     ctypes.c_void_p,
        ##     ctypes.c_long,
        ##     ctypes.c_long,
        ##     ctypes.c_int,
        ##     ctypes.c_int,
        ##     ctypes.c_void_p,
        ## ]
        ## self._tcw.MATRIX_GetBaseVectorFromCore.restype = ctypes.c_short

        # Sets an element of the matrix
        # short MATRIX_SetElement(MATRIX hMatrix, long idRow, long idCol, DATA_TYPE Type, void *p);
        self._tcw.MATRIX_SetElement.argtypes = [
            ctypes.c_void_p,
            ctypes.c_long,
            ctypes.c_long,
            ctypes.c_int,
            ctypes.c_void_p,
        ]

        # Sets a row or column of a matrix using the base index.
        # Arguments:
        #     iPos    -   the core position of the row or the column.
        #     dim     -   dimension to set: MATRIX_ROW or MATRIX_COL.
        #     Type    -   data type of provided values.
        #     Array   -   array of values to store.
        # short MATRIX_SetBaseVector(MATRIX hMatrix, long iPos, MATRIX_DIM dim, DATA_TYPE Type, void *Array);
        self._tcw.MATRIX_SetBaseVector.argtypes = [
            ctypes.c_void_p,
            ctypes.c_long,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_void_p,
        ]
        self._tcw.MATRIX_SetBaseVector.restype = ctypes.c_short

        # Sets a row or a column  of a matrix using the current index.
        # Arguments:
        #     ID      -   the identifier of the row or the column.
        #     dim     -   dimension to set: MATRIX_ROW or MATRIX_COL.
        #     Type    -   data type of provided values.
        #     Array   -   array of values to store.
        # short MATRIX_SetVector(MATRIX hMatrix, long ID, MATRIX_DIM dim, DATA_TYPE Type, void *Array);
        self._tcw.MATRIX_SetVector.argtypes = [
            ctypes.c_void_p,
            ctypes.c_long,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_void_p,
        ]
        self._tcw.MATRIX_SetVector.restype = ctypes.c_short

        # Returns the position of the current index.
        # short MATRIX_GetCurrentIndexPos(MATRIX hMatrix, MATRIX_DIM dim);
        self._tcw.MATRIX_GetCurrentIndexPos.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self._tcw.MATRIX_GetCurrentIndexPos.restype = ctypes.c_short

        # Sets the current matrix index for the the requested dimension.
        # short MATRIX_SetIndex(MATRIX hMatrix, MATRIX_DIM dim, short iIdx);
        self._tcw.MATRIX_SetIndex.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_short,
        ]
        self._tcw.MATRIX_SetIndex.restype = ctypes.c_short

        # Add an index to an exiting file
        # short MATRIX_AddIndex(MATRIX hMatrix, MAT_INDEX *pIndex);
        self._tcw.MATRIX_AddIndex.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self._tcw.MATRIX_AddIndex.restype = ctypes.c_short

        # Marks index as deleted.
        # short MATRIX_DropIndex(MATRIX hMatrix, MATRIX_DIM dim, short iIdx);
        self._tcw.MATRIX_DropIndex.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_short,
        ]
        self._tcw.MATRIX_DropIndex.restype = ctypes.c_short

        # For file-based matrices - creates a cache, not greater than nSize bytes.
        # Type is either SERIAL_CACHE or RANDOM_CACHE.
        # The serial cache is only useful for a sequential read of the
        #     matrix, in natural (base) order.
        # The random cache is only useful for random access where each element
        #     is accessed several times.
        # Apply is either CACHE_ONE or CACHE_ALL.  In case of CACHE_ONE - the
        #     cache is created for the current core, and every time the core is
        #     changed (via MATRIX_SetCore), the old cache is destroyed and a
        #     new one is created.  For CACHE_ALL - a separate cache is created
        #     for each core, the actual size determined by the number of cores.
        # Note: This should be called in pairs with MATRIX_DestroyCache().
        #     Nested calls are allowed.
        # short MATRIX_CreateCache(MATRIX hMatrix, MAT_CACHE_TYPE Type, MAT_CACHE_APPLY apply, long nSize);
        self._tcw.MATRIX_CreateCache.argtypes = [
            ctypes.c_void_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_long,
        ]
        self._tcw.MATRIX_CreateCache.restype = ctypes.c_short

        # Destroys a matrix cache.
        # void    MATRIX_DestroyCache(MATRIX hMatrix);
        self._tcw.MATRIX_DestroyCache.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_DestroyCache.restype = None

        # Disables the use of the cache.
        # short MATRIX_DisableCache(MATRIX hMatrix);
        self._tcw.MATRIX_DisableCache.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_DisableCache.restype = ctypes.c_short

        # Enables the cache.
        # short MATRIX_EnableCache(MATRIX hMatrix);
        self._tcw.MATRIX_EnableCache.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_EnableCache.restype = ctypes.c_short

        # Reads back the cache buffer(s) for a matrix.
        # short MATRIX_RefreshCache(MATRIX hMatrix);
        self._tcw.MATRIX_RefreshCache.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_RefreshCache.restype = ctypes.c_short

        # Fills szLabel with the label of the specified core.
        # void    MATRIX_GetLabel(MATRIX hMatrix, short iCore, char *szLabel);
        self._tcw.MATRIX_GetLabel.argtypes = [
            ctypes.c_void_p,
            ctypes.c_short,
            ctypes.c_char_p,
        ]
        self._tcw.MATRIX_GetLabel.restype = None

        # Set the label for a specified core.
        # void MATRIX_SetLabel(MATRIX hMatrix, short iCore, char *szLabel);
        self._tcw.MATRIX_SetLabel.argtypes = [
            ctypes.c_void_p,
            ctypes.c_short,
            ctypes.c_char_p,
        ]
        self._tcw.MATRIX_SetLabel.restype = None

        # Tests whether the matrix is in sparse representation.
        # BOOL    MATRIX_IsSparse(MATRIX hMatrix);
        self._tcw.MATRIX_IsSparse.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_IsSparse.restype = ctypes.c_bool

        # Tests whether the matrix is in file-based.
        # BOOL    MATRIX_IsFileBased(MATRIX hMatrix);
        self._tcw.MATRIX_IsFileBased.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_IsFileBased.restype = ctypes.c_bool

        # Increases the reference count of the matrix. This call should be used to increase access speed.
        # It must be called in pair with MATRIX_CloseFile.
        # short MATRIX_OpenFile(MATRIX hMatrix, BOOL fRead);
        self._tcw.MATRIX_OpenFile.argtypes = [ctypes.c_void_p, ctypes.c_bool]
        self._tcw.MATRIX_OpenFile.restype = ctypes.c_short

        # Decreases the reference count of the matrix.
        # short MATRIX_CloseFile(MATRIX hMatrix);
        self._tcw.MATRIX_CloseFile.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_CloseFile.restype = ctypes.c_short

        # Clears the contents of the matrix.
        # short MATRIX_Clear(MATRIX hMatrix);
        self._tcw.MATRIX_Clear.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_Clear.restype = ctypes.c_short

        # Checks whether the matrix is read only.
        # BOOL MATRIX_IsReadOnly(MATRIX hMatrix);
        self._tcw.MATRIX_IsReadOnly.argtypes = [ctypes.c_void_p]
        self._tcw.MATRIX_IsReadOnly.restype = ctypes.c_bool

        # Matrix_New
        #
        # PARAMETERS:
        #      file_name - file name full path where the matrix should be stored
        #      Label - matrix label name
        #      n_rows - number of rows
        #      row_ids - null for natural order base index, or an array of size n_rows with the IDs for each row.
        #      n_cols - number of cols
        #      col_ids - null for natural order base index, or an array of size n_rows with the IDs for each row.
        #      n_cores - the number of matrix cores
        #      core_names - core_name[i] = name of core matrix i.  if core_name is null then
        #              core names are: "Matrix 1", "Matrix 2", ... , "Matrix N".
        #      data_type - numeric data type to store in the matrix (SHORT_TYPE, LONG_TYPE, FLOAT_TYPE or DOUBLE_TYPE)
        #      compression - 0 if no compression, 1 if matrix should use compression.
        #
        #  DESCRIPTION:
        #      Creates a new matrix file.
        #
        # RETURNS:
        #      New matrix handle
        #
        # MATRIX MATRIX_New(char *file_name, char *Label, long n_rows, long *row_ids, long n_cols, long *col_ids, long n_cores, char **core_names,DATA_TYPE data_type, short compression);
        self._tcw.MATRIX_New.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_long,
            ctypes.c_void_p, #ctypes.POINTER(ctypes.c_long),
            ctypes.c_long,
            ctypes.c_void_p, #ctypes.POINTER(ctypes.c_long),
            ctypes.c_long,
            ctypes.c_void_p, #ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_int,
            ctypes.c_short,
        ]
        self._tcw.MATRIX_New.restype = ctypes.c_void_p

        # MATRIX_Copy
        #
        #  PARAMETERS:
        #      hSource - source matrix
        #      Info    - matrix creation parameters
        #      iCore   - core to copy.  Use -1 to copy all cores.
        #      CopyAllIndices   - True for copy base and all indices, False for copy current
        #                index only (making it into base of new matrix).
        #      copy_cores - an array with the indeces of the cores to copy, or null to copy all cores.
        #                         e.g., copy_cores[i] = core index to copy
        #      nCopyCores - -1 to copy all cores, else the number of cores to copy (the size of the copy_cores array)
        #
        #  DESCRIPTION:
        #      Copy one or more cores to a new matrix.
        #
        #  RETURNS:
        #      New matrix handle.
        # MATRIX MATRIX_Copy(MATRIX hSource, MAT_INFO *Info, short iCore, BOOL CopyAllIndices, long *copy_cores, long nCopyCores);
        self._tcw.MATRIX_Copy.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_short,
            ctypes.c_bool,
            ctypes.POINTER(ctypes.c_long),
            ctypes.c_long,
        ]
        self._tcw.MATRIX_Copy.restype = ctypes.c_void_p

    @staticmethod
    def _str_to_bytes(input: str) -> bytes:
        """Convert a Path object to a bytes object."""
        return str(input).encode("utf-8")
