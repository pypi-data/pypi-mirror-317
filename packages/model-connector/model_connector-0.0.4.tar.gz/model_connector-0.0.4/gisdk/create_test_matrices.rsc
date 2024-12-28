/* Create some test matrix files for use in testing the matrix read functions */

Macro "create_simple_all"

    RunMacro("create_simple_float")
    RunMacro("create_simple_short")
    RunMacro("create_simple_long")
    RunMacro("create_simple_double")

EndMacro

Macro "create_simple_float" 
    /*Simple 3x3 matrix with three cores, float datatype, missing as the final element*/

    filename = "C:\\git\\model_connector\\tests\\test_data\\mtx_simple_float.mtx"

    type = "Float"
    mat_cores = {"Core1", "Table2", "Matrix 3"}
    mat_data = {{{1.1, 2.2, 3.3},
                 {4.4, 5.5, 6.6},
                 {7.7, 8.8, 9.9}}, 
                
                {{10.1, 20.2, 30.3},
                 {40.4, 50.5, 60.6},
                 {70.7, 80.8, 90.9}}, 
                
                {{100.1, 200.2, 300.3},
                 {400.4, 500.5, 600.6},
                 {700.7, 800.8, null}}}

    RunMacro("create_simple", filename, type, mat_cores, mat_data)

EndMacro

Macro "create_simple_short" 
    /*Simple 3x3 matrix with three cores, short datatype, missing as the final element*/

    filename = "C:\\git\\model_connector\\tests\\test_data\\mtx_simple_short.mtx"

    type = "Short"
    mat_cores = {"Core1", "Table2", "Matrix 3"}
    mat_data = {{{1, 2, 3},
                 {4, 5, 6},
                 {7, 8, 9}}, 
                
                {{10, 20, 30},
                 {40, 50, 60},
                 {70, 80, 90}}, 
                
                {{100, 200, 300},
                 {400, 500, 600},
                 {700, 800, null}}}

    RunMacro("create_simple", filename, type, mat_cores, mat_data)

EndMacro

Macro "create_simple_long"
    /*Simple 3x3 matrix with three cores, long datatype, missing as the final element*/

    filename = "C:\\git\\model_connector\\tests\\test_data\\mtx_simple_long.mtx"

    type = "Long"
    mat_cores = {"Core1", "Table2", "Matrix 3"}
    mat_data = {{{1, 2, 3},
                 {4, 5, 6},
                 {7, 8, 9}}, 
                
                {{10, 20, 30},
                 {40, 50, 60},
                 {70, 80, 90}}, 
                
                {{100, 200, 300},
                 {400, 500, 600},
                 {700, 800, null}}}

    RunMacro("create_simple", filename, type, mat_cores, mat_data)

EndMacro

Macro "create_simple_double"
    /*Simple 3x3 matrix with three cores, double datatype, missing as the final element*/

    filename = "C:\\git\\model_connector\\tests\\test_data\\mtx_simple_double.mtx"

    type = "Double"
    mat_cores = {"Core1", "Table2", "Matrix 3"}
    mat_data = {{{1.1, 2.2, 3.3},
                 {4.4, 5.5, 6.6},
                 {7.7, 8.8, 9.9}}, 
                
                {{10.1, 20.2, 30.3},
                 {40.4, 50.5, 60.6},
                 {70.7, 80.8, 90.9}}, 
                
                {{100.1, 200.2, 300.3},
                 {400.4, 500.5, 600.6},
                 {700.7, 800.8, null}}}

    RunMacro("create_simple", filename, type, mat_cores, mat_data)

EndMacro

Macro "create_simple" (filename, type, mat_cores, mat_data)
    Opts.[File Name] = filename
    Opts.Label = "Simple test matrix"
    Opts.Type = type
    Opts.Tables = mat_cores
    Opts.Complression = 1

    mat = CreateSimpleMatrix("simple_mtx", mat_data.length, mat_data[1].length, Opts)

    for _core = 1 to mat_cores.length do
        cur = CreateMatrixCurrency(mat, mat_cores[_core], , , )
        for _row = 1 to mat_data[_core].length do
            SetMatrixVector(cur, A2V(mat_data[_core][_row]), {"Row":_row})
        end
        cur = null
    end

    //Create a subset index of the matrix
    RunMacro("SubsetIndices", mat)  

    mat = null

EndMacro

Macro "SubsetIndices" (mat)
    /* This creates the following indices for testing (in this order):
     - Subset: row/col index that excludes the first row [1]
     - Reverse: row/col index that reverses the data order [2]
     - Row1: row index that only includes the first row only [4] - ROW ONLY
     */

    vw = RunMacro("SequenceView", 3)
    SetView(vw)

    // Create an index that excluses row 1
    SelectByQuery("Subset", "Several", "Select * Where ID > 1")
    CreateMatrixIndex("Subset", mat, "Both", vw+"|Subset", "ID", "ID", )

    // Create an index that reverses the data order
    CreateMatrixIndex("Reverse", mat, "Both", vw+"|", "ID", "REV", )

    // Create an index with a gap
    CreateMatrixIndex("Gapped", mat, "Both", vw+"|", "ID", "GAP", )

    // Create an index that only includes row 1
    SelectByQuery("Row1", "Several", "Select * Where ID = 1")
    CreateMatrixIndex("Row1", mat, "Row", vw+"|Row1", "ID", "ID", )


    CloseView(vw)

EndMacro

Macro "SequenceView" (count)

    vw = CreateTable("vw", null, "MEM", {{"ID", "Integer", 10, }, 
        {"REV", "Integer", 10, },
        {"GAP", "Integer", 10, }})
    AddRecords(vw, null, null, {"Empty Records":count})
    SetDataVector(vw+"|", "ID", Vector(count, "Long", {{"Sequence", 1, 1}}), )
    SetDataVector(vw+"|", "REV", Vector(count, "Long", {{"Sequence", count, -1}}), )
    GAP = Vector(count, "Long", {{"Sequence", 1, 1}})
    GAP[count] = GAP[count]*10
    SetDataVector(vw+"|", "GAP", GAP, )

    Return(vw)

EndMacro