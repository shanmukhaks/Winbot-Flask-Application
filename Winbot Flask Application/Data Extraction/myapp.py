# app.py
from flask import Flask, jsonify, request, json  # import flask

app = Flask(__name__)  # create an app instance


@app.route("/header", methods=['POST'])  # at the end point /
def header():  # call method start
    data = json.loads(request.data, strict=False)
    import re
    import pandas as pd
    Index = 0

    position = "1"
    headerTable = pd.DataFrame()
    print(headerTable.head(3))
    dict_of_header = dict()
    headerTablePrompts = pd.DataFrame(data["headerData"])
    print(headerTablePrompts.head(4))
    pdfString = data["pdfString"]
    # for i in y:
    # pdfString = i.split('\t', 1)[0]
    print(str(pdfString))
    for headerrow in headerTablePrompts.itertuples():
        position = "2"
        value = ""
        prompt = str(headerrow.COLUMN_PROMPT)
        print("prompt is " + prompt)
        columnname = str(headerrow.COLUMN_NAME)
        print("colname is " + columnname)
        columntype = str(headerrow.COLUMN_TYPE)
        print("coltype is " + columntype)
        columnlength = int(headerrow.COLUMN_LENGTH)
        print("collen is " + str(columnlength))
        end_of_line = int(headerrow.END_OF_LINE)
        print("eol is " + str(end_of_line))
        no_of_words = int(headerrow.NO_OF_WORDS)
        print("now is " + str(no_of_words))
        same_line = int(headerrow.SAME_LINE)
        print("sl is " + str(same_line))
        Nth_Line = int(headerrow.NTH_LINE)
        print("nl is " + str(Nth_Line))
        starting_word_position = int(headerrow.STARTING_WORD_POSITION)
        print("swp is " + str(starting_word_position))
        i = 0

        for item in pdfString:
            item = str(item)
            print(position)
            temp = str(item)
            try:
                if item.__contains__(prompt):
                    print("inside if prompt")
                    if columntype == "String":
                        position = "4"
                        headerTable.insert(Index, columnname, "")
                        print("inserted value is:" + headerTable[columnname])
                        headerTable[columnname] = headerTable[columnname].astype('str')
                        print("inserted value is:" + headerTable[columnname])

                    else:
                        position = "5"
                        headerTable.insert(Index, columnname, "")
                        print("inserted value is:" + headerTable[columnname])
                        headerTable[columnname] = pd.to_numeric(headerTable[columnname])
                        print("inserted value is:" + headerTable[columnname])

                    print("column length is " + str(columnlength))
                    print("value before processing " + item + ".")
                    if same_line == 1:
                        print("no of words " + str(no_of_words))
                        if end_of_line == 1:
                            position = "6"
                            value = str(item)
                            value = value[item.index(prompt) + len(prompt):].strip()
                            print("value at end of line is " + value + ".")
                        else:
                            position = "7"
                            value = ""
                            temp = temp[item.index(prompt) + len(prompt):].strip()
                            print("temp is " + temp)
                            for c in temp:
                                position = "8"
                                print("c is " + c)
                                if no_of_words != 0:
                                    if c == " ":
                                        value = value + c
                                        position = "9"
                                        no_of_words = no_of_words - 1
                                        if no_of_words == 0:
                                            break
                                    else:
                                        position = "10"
                                        value = value + c
                                else:
                                    print("position is " + position)
                                print("value to be stored is " + value)
                    else:
                        print("item to retrieve data" + str(pdfString[i + Nth_Line]))
                        position = "11"
                        val = str(pdfString[i + Nth_Line]).split()
                        if no_of_words > 1:
                            position = "12"
                            value = val[starting_word_position - 1]
                            for a in range(1, no_of_words, 1):
                                position = "13"
                                value = value + " " + val[starting_word_position + a - 1]
                                print("value of a : {0}" + str(a))
                                print("value is " + value)
                        else:
                            position = "14"
                            value = val[starting_word_position - 1]
                        print("value to be stored is " + value)
                    position = "15"
                    if str(columntype).upper() == "INT":
                        value = re.sub("[^.-:]", "", value)
                        print(str("after regex : " + value))
                    headerTable.loc[Index, columnname] = value
                    dict_of_header[columnname] = value
                    print("line value is " + dict_of_header[columnname])
            except:
                headerTable.loc[Index, columnname] = ""
                dict_of_header[columnname] = ""
            else:
                print(position)
            i = i + 1

            if str(value) == "":
                print("value")
            else:
                print(position)
                break

    position = "22"
    print("header data is ")
    headerTable = headerTable[headerTable.columns[::-1]]
    print(headerTable)
    headerData = headerTable.to_json(orient='table')

    headerData = json.dumps(json.loads(headerData), sort_keys=False)

    return headerData


@app.route("/lines", methods=['POST'])  # at the end point /
def lines():  # call method start
    data = json.loads(request.data, strict=False)
    import re
    import pandas as pd
    from collections import OrderedDict
    Index = 0
    c = 0
    # Line data processing
    removable = "abc"
    val_str = ""
    val_dec = None
    Value = ""
    k = ""
    line_start = 10
    lineTable = pd.DataFrame()
    dict_for_line = dict()
    lineTablePrompts = pd.DataFrame(data["lineData"])
    print(lineTablePrompts.head(4))
    formatdt = pd.DataFrame(data["formatData"])
    print(formatdt.head(2))
    pdfString = data["pdfString"]

    for row in lineTablePrompts.itertuples():
        columnName = str(row.COLUMN_NAME)
        print("column name is " + columnName)
        lineTable.insert(Index, columnName, "")
        print("inserted value is:" + lineTable[columnName])
        lineTable[columnName] = lineTable[columnName].astype('str')
        print("inserted value is:" + lineTable[columnName])
        print("Line table column " + columnName + " is created")

        Index = Index + 1

    i = 0
    nth_line_linestart = int(formatdt.loc[formatdt.index[0], 'NTH_LINE_LINESTART'])
    nth_line_lineend = int(formatdt.loc[formatdt.index[0], 'NTH_LINE_LINEEND'])
    for item in pdfString:
        try:
            item = str(item).replace("-", "")
            if str(pdfString[i + nth_line_lineend - 1]).__contains__(str(formatdt.loc[formatdt.index[0], 'LINE_END'])):
                print("end of line found")
                break
            else:
                print("if no line end")
                if str(item).__contains__(str(formatdt.loc[formatdt.index[0], 'LINE_START'])):
                    line_start = 1
                    print("lines started")
                else:
                    if line_start == 1 and str(item) != "":
                        print("Nthline is " + str(nth_line_linestart))
                        Val = pdfString[i + nth_line_linestart - 1].split()
                        print("Working line is: " + pdfString[i + nth_line_linestart - 1])
                        for row in lineTablePrompts.itertuples():
                            column_type = str(row.COLUMN_TYPE)
                            # print("columntype is "+ column_type)
                            columnName = str(row.COLUMN_NAME)
                            # print("column name is " + columnName)
                            line_starting = int(row.LINE_STARTING)
                            next_line = int(row.NEXT_LINE)
                            no_of_words = int(row.NO_OF_WORDS)
                            starting_word_position = int(row.STARTING_WORD_POSITION)
                            length_of_line = len(Val)
                            print("length of line is " + str(length_of_line))
                            if line_starting == 1:
                                print("inside line starting")
                                if starting_word_position <= length_of_line:
                                    if next_line == 0:
                                        if no_of_words > 1:
                                            Value = Val[starting_word_position - 1]
                                            for a in range(1, no_of_words, 1):
                                                Value = Value + " " + Val[starting_word_position + a - 1]
                                        else:
                                            Value = Val[starting_word_position - 1]
                                    else:
                                        print("inside next line")
                                        Val1 = pdfString[i + next_line + nth_line_linestart - 1].split()
                                        if no_of_words > 1:
                                            Value = Val1[starting_word_position - 1]
                                            for a in range(1, no_of_words, 1):
                                                Value = Value + " " + Val1[starting_word_position + a - 1]
                                        else:
                                            Value = Val1[starting_word_position - 1]
                                        print("inside next line" + str(Value))
                                else:
                                    c = 1
                                word_position = starting_word_position - 1
                                for s in Val:
                                    print("values in val after linestarting 1 : " + s)
                            elif line_starting == 0:
                                if starting_word_position <= length_of_line:
                                    if next_line == 0:
                                        if no_of_words > 1:
                                            Value = Val[length_of_line - starting_word_position]
                                            for a in range(1, no_of_words, 1):
                                                Value = Value + " " + Val[length_of_line - (starting_word_position - a)]
                                        else:
                                            Value = Val[length_of_line - (starting_word_position - 1) - 1]
                                            print("Quantity value is " + str(Value))
                                    else:
                                        print("next line value is " + str(next_line))
                                        Val2 = pdfString[i + next_line + nth_line_linestart - 1].split()
                                        length_of_line1 = len(Val2)
                                        if no_of_words > 1:
                                            Value = Val2[length_of_line1 - starting_word_position]
                                            for a in range(1, no_of_words, 1):
                                                Value = Value + " " + Val2[length_of_line1 - (starting_word_position - a)]
                                        else:
                                            print("val2 length " + str(length_of_line1 - (starting_word_position - 1) - 1))
                                            Value = Val2[length_of_line1 - (starting_word_position - 1) - 1]
                                            print("next line value is " + str(Value))
                                else:
                                    c = 1
                                word_position = length_of_line - (starting_word_position - 1) - 1
                                for s in Val:
                                    print("values in val after linestarting 0 : " + s)
                                print("quantity value1 is " + str(Value))
                            elif line_starting == 2:
                                k = str(row.COLUMN_NAME)
                                print("K value is " + str(k))
                            if line_starting == 2:
                                print("do nothing")
                            else:
                                inputString = Value
                                temp = str(row.VALIDATING_PATTERN)  # "\d+"  # "/" # [\x41-\x5A];[\x2F-\x2F]
                                myRegex = temp.replace("^", "\\")
                                if temp.__contains__("#"):
                                    myRegex = temp.replace("#", "£")
                                validatingMethod = str(row.VALIDATING_METHOD)  # "Regex"
                                lenOfString = len(inputString)
                                print("len of str is " + str(lenOfString))
                                SplitRegex = myRegex.split(";")
                                temp_val = ""
                                count = 0

                                if validatingMethod == "Contains":
                                    if str(inputString).__contains__(myRegex):
                                        result = "True"
                                        val_str = Value
                                        removable = ""
                                    else:
                                        result = "False"
                                        val_str = ""
                                        removable = Value
                                    print("Case 1 result:" + result)
                                elif validatingMethod == "ASCII Code":
                                    for char in range(0, len(inputString)):
                                        print(inputString[char])
                                        for reg in SplitRegex:
                                            regex = re.compile(reg)
                                            print("reg is " + str(reg))
                                            match = regex.match(inputString[char])
                                            if match:
                                                count = count + 1
                                                temp_val = temp_val + reg + " "
                                                print("value is " + str(inputString[char]) + " count is " + str(count))
                                                break
                                    print(" total count is " + str(count))
                                    for splitreg in SplitRegex:
                                        if str(temp_val).__contains__(splitreg):
                                            status = "Success"
                                            print(status)
                                        else:
                                            status = "Failed"
                                            print(status)
                                            break

                                    if status == "Success" and count == lenOfString:
                                        result = "True"
                                        val_str = Value
                                        removable = ""
                                    else:
                                        result = "False"
                                        val_str = ""
                                        removable = Value
                                    print("Case 2 result is " + result)
                                elif validatingMethod == "Regex":
                                    regex = re.compile(myRegex)
                                    print("regex is " + str(regex) + inputString)
                                    match = regex.match(inputString)
                                    print("1")
                                    if match:
                                        print("match")
                                        result = "True"
                                        val_str = Value
                                        removable = ""
                                    else:
                                        print("not match")
                                        result = "False"
                                        val_str = ""
                                        removable = Value
                                    print("case 3 result is " + result)
                                print("Final values is " + Value)
                                # print("Final result is " + result)
                                if c == 0:
                                    Val[word_position] = removable
                            if str(column_type).upper() == "INT":
                                Value = re.sub("[^.-:]", "", Value)
                            print("value after regex is " + str(Value))
                            print("index is " + str(Index))
                            print("val_str is " + str(val_str))
                            print(str(column_type))
                            lineTable.loc[Index, columnName] = val_str
                        if k == "":
                            print("no value for line starting is equal to 2")
                        else:
                            x = ","
                            desc = x.join(Val)
                            print("desc " + desc)
                            desc = desc.replace(",", " ").strip()
                            print("k value is " + str(k))
                            print("column name in k is" + columnName)
                            lineTable.loc[Index, k] = desc
                            dict_for_line[k] = desc
                        c = 0
                    else:
                        print("")
        except:
            print("except")
        i = i + 1
        Index = Index + 1

    print("line data is ")
    print(lineTable)

    # multi line process
    # i -- count of rows
    # j -- count of columns
    # s -- First row append
    # descolpos -- description column position
    # dcc -- decimal column check

    dt = lineTable
    print("before dt")
    print(dt)
    print("after dt")
    count = lineTable.shape
    i = count[0]
    print(str(i))
    j = count[1]
    print(str(j))
    Format_dt = lineTablePrompts
    print(Format_dt)

    # adding new column to dataframe
    columnName = "marker"
    dt.insert(j, columnName, "")
    print("h1")
    print("inserted value is:" + dt[columnName])
    print("h2")
    dt[columnName] = pd.to_numeric(dt[columnName],errors='raise', downcast=None)
    print("h3")
    print("inserted value is:" + str(dt[columnName]))
    print("h4")
    print("here")
    #print(dt)

    descolpos = 0
    coltyp_pos = 0
    for row in Format_dt.itertuples():
        print("in for loop")
        if str(int(row.LINE_STARTING)) == "2":
            break
        descolpos = descolpos + 1

    print("value of y1 is " + str(descolpos))

    multiline_sep = str(formatdt.loc[formatdt.index[0], 'MULTILINE_DESC_SEP'])

    for rows in Format_dt.itertuples():
        if str(rows.COLUMN_NAME) == multiline_sep:
            break
        coltyp_pos = coltyp_pos + 1
    print("coltype values is" + str(coltyp_pos))

    for row in range(0, i):
        vall = ""
        if dt.iloc[row, coltyp_pos] != "":
            row_index = row

        else:
            vall = str(dt.iloc[row, descolpos])
            dt.iloc[row_index, descolpos] = str(dt.iloc[row_index, descolpos]) + " " + vall
            dt.iloc[row, -1] = 1

    dt = dt[dt.marker != 1]

    del dt['marker']
    dt = dt.reset_index()
    del dt['index']
    print("before print dt")
    print(dt)
    dt1 = dt.to_json(orient='table')
    print("before print dt1")
    print(dt1)
    dt1 = json.dumps(OrderedDict(json.loads(dt1)), sort_keys=False)
    print("type of dt1 ",type(dt1))
    """val_str = ""


    val_i = 0
    nth_line_end_val = "EXTENDED AMOUNT"
    print("multi line sep ",multiline_sep)
    for item in pdfString:
        pdfval = str(item)

        if(val_i==1):
            print("in if val_i ",val_i)
            val_str = val_str + "^"+pdfval
            print("in if val_i ",val_str)
        if pdfval.__contains__(nth_line_end_val):
            print("in break if" ,pdfval)
            break

        for i in range(len(dt)):
            print("in for pdf val "+str(pdfval))
            print("in for mutliline "+str(dt.loc[i,multiline_sep]))
            if str(pdfval).__contains__(str(dt.loc[i,multiline_sep])):
                print("inside if")
                if str(val_str).__contains__("^"):
                    val_str_arr = val_str.split("^")
                    val_str_length = len(val_str_arr)
                    print("val_str_length in inside if " + str(val_str_length))
                    print("val_str_arr in inside if " , val_str_arr[24])
                    val_str = val_str.replace(val_str_arr[val_str_length-1],"")
                    print("val_str in inside if " + str(val_str))
                val_str = val_str+"~"
                val_i = 1
    print("val_str is  "+val_str)
    val_str_arr_1 = val_str.split("~")
    print("val+_str_arr_1 length " ,len(val_str_arr_1))"""

    return dt1

@app.route("/sublines", methods=['POST'])
def sublines():  # call method start
    data = json.loads(request.data, strict=False)
    import re
    import pandas as pd
    from collections import OrderedDict
    Index = 0
    c = 0
    # Line data processing
    removable = "abc"
    val_str = ""
    val_dec = None
    Value = ""
    k = ""
    line_start = 10
    lineTable = pd.DataFrame()
    dict_for_line = dict()
    lineTablePrompts = pd.DataFrame(data["lineData"])
    print(lineTablePrompts.head(4))
    formatdt = pd.DataFrame(data["formatData"])
    print(formatdt.head(2))
    pdfString = data["pdfString"]

    for row in lineTablePrompts.itertuples():
        columnName = str(row.COLUMN_NAME)
        print("column name is " + columnName)
        lineTable.insert(Index, columnName, "")
        print("inserted value is:" + lineTable[columnName])
        lineTable[columnName] = lineTable[columnName].astype('str')
        print("inserted value is:" + lineTable[columnName])
        print("Line table column " + columnName + " is created")

        Index = Index + 1

    i = 0
    nth_line_linestart = int(formatdt.loc[formatdt.index[0], 'NTH_LINE_LINESTART_SUB'])
    nth_line_lineend = int(formatdt.loc[formatdt.index[0], 'NTH_LINE_LINEEND_SUB'])
    for item in pdfString:
        item = str(item).replace("-", "")
        if str(pdfString[i + nth_line_lineend - 1]).__contains__(str(formatdt.loc[formatdt.index[0], 'LINE_END_SUB'])):
            print("end of line found")
            break
        else:
            print("if no line end")
            if str(item).__contains__(str(formatdt.loc[formatdt.index[0], 'LINE_START_SUB'])):
                line_start = 1
                print("lines started")
            else:
                if line_start == 1 and str(item) != "":
                    print("Nthline is " + str(nth_line_linestart))
                    Val = pdfString[i + nth_line_linestart - 1].split()
                    print("Working line is: " + pdfString[i + nth_line_linestart - 1])
                    for row in lineTablePrompts.itertuples():
                        column_type = str(row.COLUMN_TYPE)
                        # print("columntype is "+ column_type)
                        columnName = str(row.COLUMN_NAME)
                        # print("column name is " + columnName)
                        line_starting = int(row.LINE_STARTING)
                        next_line = int(row.NEXT_LINE)
                        no_of_words = int(row.NO_OF_WORDS)
                        starting_word_position = int(row.STARTING_WORD_POSITION)
                        length_of_line = len(Val)
                        print("length of line is " + str(length_of_line))
                        if line_starting == 1:
                            print("inside line starting")
                            if starting_word_position <= length_of_line:
                                if next_line == 0:
                                    if no_of_words > 1:
                                        Value = Val[starting_word_position - 1]
                                        for a in range(1, no_of_words, 1):
                                            Value = Value + " " + Val[starting_word_position + a - 1]
                                    else:
                                        Value = Val[starting_word_position - 1]
                                else:
                                    print("inside next line")
                                    Val1 = pdfString[i + next_line + nth_line_linestart - 1].split()
                                    if no_of_words > 1:
                                        Value = Val1[starting_word_position - 1]
                                        for a in range(1, no_of_words, 1):
                                            Value = Value + " " + Val1[starting_word_position + a - 1]
                                    else:
                                        Value = Val1[starting_word_position - 1]
                                    print("inside next line" + str(Value))
                            else:
                                c = 1
                            word_position = starting_word_position - 1
                            for s in Val:
                                print("values in val after linestarting 1 : " + s)
                        elif line_starting == 0:
                            if starting_word_position <= length_of_line:
                                if next_line == 0:
                                    if no_of_words > 1:
                                        Value = Val[length_of_line - starting_word_position]
                                        for a in range(1, no_of_words, 1):
                                            Value = Value + " " + Val[length_of_line - (starting_word_position - a)]
                                    else:
                                        Value = Val[length_of_line - (starting_word_position - 1) - 1]
                                        print("Quantity value is " + str(Value))
                                else:
                                    print("next line value is " + str(next_line))
                                    Val2 = pdfString[i + next_line + nth_line_linestart - 1].split()
                                    length_of_line1 = len(Val2)
                                    if no_of_words > 1:
                                        Value = Val2[length_of_line1 - starting_word_position]
                                        for a in range(1, no_of_words, 1):
                                            Value = Value + " " + Val2[length_of_line1 - (starting_word_position - a)]
                                    else:
                                        print("val2 length " + str(length_of_line1 - (starting_word_position - 1) - 1))
                                        Value = Val2[length_of_line1 - (starting_word_position - 1) - 1]
                                        print("next line value is " + str(Value))
                            else:
                                c = 1
                            word_position = length_of_line - (starting_word_position - 1) - 1
                            for s in Val:
                                print("values in val after linestarting 0 : " + s)
                            print("quantity value1 is " + str(Value))
                        elif line_starting == 2:
                            k = str(row.COLUMN_NAME)
                            print("K value is " + str(k))
                        if line_starting == 2:
                            print("do nothing")
                        else:
                            inputString = Value
                            temp = str(row.VALIDATING_PATTERN)  # "\d+"  # "/" # [\x41-\x5A];[\x2F-\x2F]
                            myRegex = temp.replace("^", "\\")
                            if temp.__contains__("#"):
                                myRegex = temp.replace("#", "£")
                            validatingMethod = str(row.VALIDATING_METHOD)  # "Regex"
                            lenOfString = len(inputString)
                            print("len of str is " + str(lenOfString))
                            SplitRegex = myRegex.split(";")
                            temp_val = ""
                            count = 0

                            if validatingMethod == "Contains":
                                if str(inputString).__contains__(myRegex):
                                    result = "True"
                                    val_str = Value
                                    removable = ""
                                else:
                                    result = "False"
                                    val_str = ""
                                    removable = Value
                                print("Case 1 result:" + result)
                            elif validatingMethod == "ASCII Code":
                                for char in range(0, len(inputString)):
                                    print(inputString[char])
                                    for reg in SplitRegex:
                                        regex = re.compile(reg)
                                        print("reg is " + str(reg))
                                        match = regex.match(inputString[char])
                                        if match:
                                            count = count + 1
                                            temp_val = temp_val + reg + " "
                                            print("value is " + str(inputString[char]) + " count is " + str(count))
                                            break
                                print(" total count is " + str(count))
                                for splitreg in SplitRegex:
                                    if str(temp_val).__contains__(splitreg):
                                        status = "Success"
                                        print(status)
                                    else:
                                        status = "Failed"
                                        print(status)
                                        break

                                if status == "Success" and count == lenOfString:
                                    result = "True"
                                    val_str = Value
                                    removable = ""
                                else:
                                    result = "False"
                                    val_str = ""
                                    removable = Value
                                print("Case 2 result is " + result)
                            elif validatingMethod == "Regex":
                                regex = re.compile(myRegex)
                                print("regex is " + str(regex) + inputString)
                                match = regex.match(inputString)
                                print("1")
                                if match:
                                    print("match")
                                    result = "True"
                                    val_str = Value
                                    removable = ""
                                else:
                                    print("not match")
                                    result = "False"
                                    val_str = ""
                                    removable = Value
                                print("case 3 result is " + result)
                            print("Final values is " + Value)
                            # print("Final result is " + result)
                            if c == 0:
                                Val[word_position] = removable
                        if str(column_type).upper() == "INT":
                            Value = re.sub("[^.-:]", "", Value)
                        print("value after regex is " + str(Value))
                        print("index is " + str(Index))
                        print("val_str is " + str(val_str))
                        print(str(column_type))
                        lineTable.loc[Index, columnName] = val_str
                    if k == "":
                        print("no value for line starting is equal to 2")
                    else:
                        x = ","
                        desc = x.join(Val)
                        print("desc " + desc)
                        desc = desc.replace(",", " ").strip()
                        print("k value is " + str(k))
                        print("column name in k is" + columnName)
                        lineTable.loc[Index, k] = desc
                        dict_for_line[k] = desc
                    c = 0
                else:
                    print("")

        i = i + 1
        Index = Index + 1

    print("line data is ")
    print(lineTable)

    # multi line process
    # i -- count of rows
    # j -- count of columns
    # s -- First row append
    # descolpos -- description column position
    # dcc -- decimal column check

    dt = lineTable
    print("before dt")
    print(dt)
    print("after dt")
    count = lineTable.shape
    i = count[0]
    print(str(i))
    j = count[1]
    print(str(j))
    Format_dt = lineTablePrompts
    print(Format_dt)

    # adding new column to dataframe
    columnName = "marker"
    dt.insert(j, columnName, "")
    print("h1")
    print("inserted value is:" + dt[columnName])
    print("h2")
    dt[columnName] = pd.to_numeric(dt[columnName],errors='raise', downcast=None)
    print("h3")
    print("inserted value is:" + str(dt[columnName]))
    print("h4")
    print("here")
    #print(dt)

    descolpos = 0
    coltyp_pos = 0
    for row in Format_dt.itertuples():
        print("in for loop")
        if str(int(row.LINE_STARTING)) == "2":
            break
        descolpos = descolpos + 1

    print("value of y1 is " + str(descolpos))

    multiline_sep = str(formatdt.loc[formatdt.index[0], 'MULTILINE_DESC_SEP_SUB'])

    for rows in Format_dt.itertuples():
        if str(rows.COLUMN_NAME) == multiline_sep:
            break
        coltyp_pos = coltyp_pos + 1
    print("coltype values is" + str(coltyp_pos))

    for row in range(0, i):
        vall = ""
        if dt.iloc[row, coltyp_pos] != "":
            row_index = row

        else:
            vall = str(dt.iloc[row, descolpos])
            dt.iloc[row_index, descolpos] = str(dt.iloc[row_index, descolpos]) + " " + vall
            dt.iloc[row, -1] = 1

    dt = dt[dt.marker != 1]

    del dt['marker']
    dt = dt.reset_index()
    del dt['index']
    print("before print dt")
    print(dt)
    dt1 = dt.to_json(orient='table')
    print("before print dt1")
    print(dt1)
    dt1 = json.dumps(OrderedDict(json.loads(dt1)), sort_keys=False)
    print("type of dt1 ",type(dt1))




    return dt1


if __name__ == "__main__":  # on running python app.py
    app.debug = True
    app.run()  # run the flask app