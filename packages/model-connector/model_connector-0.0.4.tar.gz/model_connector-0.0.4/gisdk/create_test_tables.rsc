Macro "create_simple_bin"
    /*Create a simple .bin file with two rows and all possible data types*/

    //	Field type - 
    // "Integer" (long integers), 
    // "Real" (double-precision floating point numbers), 
    // "String", 
    // "Short" (short integers), 
    // "Tiny" (one-byte integers), 
    // "Float" (single-precision floating point numbers), 
    // "Date" (4-byte date), 
    // "Time" (4-byte time), or 
    // "DateTime" (8-byte date and time)


    // ---- Create the empty table ----
    filename = "C:\\git\\model_connector\\tests\\test_data\\simple.bin"

    table_spec = {{"fld_integer", "Integer", 10, 0},
                  {"fld_real", "Real", 10, 4},
                  {"fld_string", "String", 10, 0},
                  {"fld_short", "Short", 10, 4},
                  {"fld_tiny", "Tiny", 10, 0},
                  {"fld_float", "Float", 10, 2},
                  {"fld_date", "Date", 10, 0},
                  {"fld_time", "Time", 10, 0},
                  {"fld_datetime", "DateTime", 10, 0}}
    
    field_names = table_spec.map(do (x) Return(x[1]) end)

    vw = CreateTable("vw", filename, "FFB", table_spec)

    // ---- Add some data ----
    data = {{1, 1.1, "one", 1, 1, 1.1, CreateDate(15,1,2001), CreateTime(13,1,1), CreateDateTime(1,1,2001,13,1,1)},
            {2, 2.2, "two", 2, 2, 2.2, CreateDate(25,2,2002), CreateTime(14,2,2), CreateDateTime(2,2,2002,14,2,2)}}

    AddRecords(vw, field_names, data, )

    CloseView(vw)


EndMacro

Macro "create_big_simple_bin"
    /*Create a giant table with many rows, columns of all C data types (no strings, dates and times)*/

    ROW_COUNT = 1000000

    MAX_TINY = 255
    MAX_SHORT = 32767

    // ---- Create the empty table ----
    filename = "C:\\git\\model_connector\\tests\\test_data\\big_simple.bin"

    table_spec = {{"fld_integer", "Integer", 10, 0},
                  {"fld_real", "Real", 10, 4},
                  {"fld_short", "Short", 10, 4},
                  {"fld_tiny", "Tiny", 10, 0},
                  {"fld_float", "Float", 10, 2}}
    
    field_names = table_spec.map(do (x) Return(x[1]) end)

    vw = CreateTable("vw", filename, "FFB", table_spec)

    // ---- Add some data ----
    dim data[ROW_COUNT, 5]
    for ii = 1 to ROW_COUNT do

        data[ii][1] = ii         //int
        data[ii][2] = ii + 0.1   //real
        data[ii][3] = Mod(ii, MAX_SHORT)         //short
        data[ii][4] = MOD(ii, MAX_TINY)         //tiny
        data[ii][5] = ii + 0.1   //float

    end

    AddRecords(vw, field_names, data, )

    CloseView(vw)

EndMacro

Macro "create_big_copmplex_bin"

    ROW_COUNT = 1000000

    MAX_TINY = 255
    MAX_SHORT = 32767

    NULL_MOD = 123 //null values every so often

    START_DATE = {12, 12, 2014}
    MAX_DATE = 3653 //10 years to keep from going out of python's date range

    MAX_TIME = 60*60*24 //seconds in a day

    filename = "C:\\git\\model_connector\\tests\\test_data\\big_complex.bin"

    table_spec = {{"fld_integer", "Integer", 10, 0},
                  {"fld_real", "Real", 10, 4},
                  {"fld_string", "String", 10, 0},
                  {"fld_short", "Short", 10, 4},
                  {"fld_tiny", "Tiny", 10, 0},
                  {"fld_float", "Float", 10, 2},
                  {"fld_date", "Date", 10, 0},
                  {"fld_time", "Time", 10, 0},
                  {"fld_datetime", "DateTime", 10, 0}}

    field_names = table_spec.map(do (x) Return(x[1]) end)

    vw = CreateTable("vw", filename, "FFB", table_spec)

    // ---- Add some data ----
    dim data[ROW_COUNT, 9]
    for ii = 1 to ROW_COUNT do

        if Mod(ii, NULL_MOD) != 0 then do

            data[ii][1] = ii         //int
            data[ii][2] = ii + 0.1   //real
            data[ii][3] = "st_" + String(ii)            //string
            data[ii][4] = Mod(ii, MAX_SHORT)         //short
            data[ii][5] = Mod(ii, MAX_TINY)         //tiny
            data[ii][6] = ii + 0.1   //float
            data[ii][7] = CreateDate(START_DATE[1], START_DATE[2], START_DATE[3]).AddDays(Mod(ii, MAX_DATE))
            data[ii][8] = CreateTime(x).AddSeconds(Mod(ii, MAX_TIME))
            data[ii][9] = CreateDateTime(START_DATE[1], START_DATE[2], START_DATE[3], 0, 0, 0).AddDays(Mod(ii, MAX_DATE)).AddSeconds(Mod(ii, MAX_TIME))
        end

    end

    AddRecords(vw, field_names, data, )

    CloseView(vw)



EndMacro

Macro "DeleteRecords"
    /*Copy a table, then delete lots of records*/

    DELETE_FREQ = 10

    source_file = "C:\\git\\model_connector\\tests\\test_data\\big_complex.bin"
    updated_file = "C:\\git\\model_connector\\tests\\test_data\\big_complex_deleted.bin"

    CopyTableFiles(null, "FFB", source_file, null, updated_file, null)

    vw = OpenTable("vw", "FFB", {updated_file})

    // ---- Delete some data ----
    SetView(vw)
    cnt = SelectByQuery("Del", "Several", "Select * Where Mod(fld_integer, "+string(DELETE_FREQ)+") = 0", )
    //cnt = SelectByQuery("Del", "Several", "Select * Where fld_integer = 4 or fld_integer = 5000", )
    if cnt > 0 then do
        DeleteRecordsInSet("Del")
    end
    CloseView(vw)
            


EndMacro