# APP ID,APP NAME, MEASURE ID,MEASURE NAME,MEASURE DEFINITION, SHEET ID,SHEET NAME,VISUALS
## importing library
import json
import subprocess
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo
import re
import openai


# function defined to process the sheets
def process_sheets(sheets, data, app_name):
    if not sheets:
        data.append({"Dashboard Name": app_name})
    else:
        data.extend([{"Dashboard Name": app_name, **sheet} for sheet in sheets])

## getting equivalent DAX expression
def dax_expression(value):
    try:
        openai.api_type = "azure"
        openai.api_base = "https://maqopenaipoc.openai.azure.com/"
        openai.api_version = "2022-12-01"
        openai.api_key = '4172119d0a8f4f0c863ae040eabc5bd8'
    except:
        print("ERROR: The OPENAI_API_KEY environment variable is not set.")
        return

    prompt = f"Translate this Qlik measure expression to equivalent Dax expression :- {value} and return only Formatted DAX expresion noting else."
    response = openai.Completion.create(
        engine="AzureOpenAIDavinci",
        prompt=prompt,
        temperature=0.5,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        seed=10206,
        stop=None
    )
    result = response.choices[0].text
    # print(response)
    # print(result)
    return result

# Get list of apps
cmd0 = ["qlik", "app"]
result = subprocess.run(cmd0 + ["ls"], capture_output=True, text=True)
rows = result.stdout.strip().split("\n")
header = rows.pop(0)
columns = [c.strip() for c in header.split()]
apps = [{"ID": row.strip().split(maxsplit=1)[0], "NAME": row.strip().split(maxsplit=1)[1]} for row in rows]

## defined dictionary to store the data for each sheets
data = {"dashBoard": [], "dataSource": [], "tableColumn": [], "sheets": [], "measuresDimension": [], "dataSourceQuery" : []}
for app in apps:
    app_id = app["ID"]
    app_name = app["NAME"]
    print("\nApp id :", app_id)
    print("App Name : ", app_name)
    data["dashBoard"].append({"Dashboard ID" : app_id, "Dashboard Name" : app_name})

    ## Result 3----------
    result3 = subprocess.run(cmd0 + ["script", "get", f"--app={app_id}"], capture_output=True, text=True)
    print("App : qlik app script get --app=" + app_id)
    # print("result3 : ", result3)

    ## finding the query for the data loaded either from local system or any other resources
    # Find the index of "ROW COUNT" in the output
    rows = result3.stdout.strip().split("\n")
    # print("rows begin")
    # for i in rows:
    #     print(i)
    # print("rows end")

    idx = -1
    for i in range(len(rows)):
        if len(rows[i])>0 and rows[i][-1]==':':
            idx = i
            break
    if idx!=-1:
        q_list = rows[idx:]
        q_string = '\n'.join([str(elem) for elem in q_list])
        # print("data query:")
        # print(q_string)

        t_s = rows[idx]
        q_s = ""
        for idx1 in range(idx+1, len(rows)):

            ## DATA SOURCES -----------------------------------------------------------------------
            if len(rows[idx1])>=4 and (rows[idx1][0:4]=='[lib'):
                # print(rows[idx1])
                qlik_script_line = rows[idx1]

                # Extract the Connection Name
                connection_name_match = re.search(r'lib://(\w+)', qlik_script_line)
                connection_name = connection_name_match.group(1)

                # Extract the Connection ID
                connection_id_match = re.search(r'\((\w+)', qlik_script_line)
                connection_id = connection_id_match.group(1)

                # Extract the Data source
                data_source_match = re.search(r'\((.*?)\)', qlik_script_line)
                data_source = data_source_match.group(1)

                # Extract the Data source type
                data_source_type_match = re.search(r'lib://\w+\s\((\w+)', qlik_script_line)
                data_source_type = data_source_type_match.group(1)

                # Extract the Table name
                table_name_match = ""
                if "qvd" in qlik_script_line:
                    table_name_match = re.search(r'\\(.+?)\.qvd', qlik_script_line)
                elif "QVD" in qlik_script_line:
                    table_name_match = re.search(r'\\(.+?)\.QVD', qlik_script_line)
                else:
                    pass

                table_name = ""
                if table_name_match==None:
                    table_name = "None"
                else:
                    table_name = table_name_match.group(1)
                data["dataSource"].append({"Dashboard Name": app_name, "Connection Name": connection_name, "Connection ID": connection_id, "Data Source": data_source, "Data Source Type": data_source_type, "Table Name": table_name})


            if len(rows[idx1])>1 and rows[idx1][-1]==':' and (rows[idx1][0]!='/' and rows[idx1][1]!='/'):
                # print("new")
                # print(app_name)
                # print(t_s)
                # print(q_s)
                data["dataSourceQuery"].append({"Dashboard Name": app_name, "Table Name" : t_s, "Source Query": q_s})
                q_s = ""
                t_s = rows[idx1][:-1]
            else:
                q_s = q_s + rows[idx1] + "\n"
        if len(q_s)>0:
            data["dataSourceQuery"].append({"Dashboard Name": app_name, "Table Name": t_s, "Source Query": q_s})

        # data["data5"].append({"App ID": app_id, "App Name": app_name, "Query": q_string})
    else:
        # data["data5"].append({"App ID": app_id, "App Name": app_name, "Query": 'No Query'})
        data["dataSourceQuery"].append({"Dashboard Name": app_name, "Table Name": 'NA', "Source Query": 'NA'})


    ## TABLE COLUMNS ----------------------------------------------------------------------------------------
    result2 = subprocess.run(cmd0 + ["tables", f"--app={app_id}"], capture_output=True, text=True)
    print("qlik app tables --app=" + app_id)
    # print("result2 : ", result2)
    # Find the index of "ROW COUNT" in the output
    rows = result2.stdout.strip().split("\n")
    # print(rows)
    if "ROW COUNT" in result2.stdout and "FIELDS" in result2.stdout and len(rows) > 1:
        r_pos = result2.stdout.index("ROW COUNT")
        f_pos = result2.stdout.index("FIELDS")
        for i in range(len(rows) - 2):
            # row_count = rows[i+1].split("\t")[1]
            # ram = rows[i+1].split("\t")[2]
            row_values = rows[i + 1].split("\t")
            table_name = row_values[0][:r_pos]
            fields = [f.strip() for f in row_values[-1][f_pos:].split(",")]
            for field in fields:
                data["tableColumn"].append(
                    {"Dashboard Name": app_name, "Table Name": table_name, "Table Columns": field})
    else:
        data["tableColumn"].append({"Dashboard Name": app_name, "Table Name": 'NA', "Table Columns": 'NA'})


    ## Result 1----------
    # Get list of sheets
    result1 = subprocess.run(cmd0 + ["object", "ls", f"--app={app_id}"], capture_output=True, text=True)
    print("qlik app object ls --app=" + app_id)
    # print("result1 : ", result1)
    rows = result1.stdout.strip().split("\n")
    # print(rows)
    header = rows.pop(0)
    columns = [c.strip() for c in header.split()]
    sheets1, sheets2, sheets3 = [], [], []
    if len(rows) > 0:
        for row in rows:
            values = [v.strip() for v in row.split()]
            if values[1] == "sheet":
                sheet_id = values[0]
                result1 = subprocess.run(cmd0 + ["object", "properties", sheet_id, f"--app={app_id}"],
                                         capture_output=True, text=True)
                print("Sheet : qlik app object properties " + sheet_id + " --app=" + app_id)

                # sheet_info = json.loads(result1.stdout)
                sheet_info = {}
                if result1.stdout is not None:
                    try:
                        sheet_info = json.loads(result1.stdout)
                        # Process the parsed data here
                    except ValueError as e:
                        print("Error1: Invalid JSON format -", e)
                else:
                    print("Error1: JSON object is None")


                # print("Sheet Info:")
                # print(json.dumps(sheet_info, indent = 3))
                # Append sheet information to the list
                sheets1.append({"Sheet Title": sheet_info["qMetaDef"]["title"]})
                # Get chart information
                for cell in sheet_info["cells"]:
                    chart_id = cell["name"]
                    # Append sheet information to the list
                    sheets2.append({"Sheet Title": sheet_info["qMetaDef"]["title"],
                                    "Chart Name": cell["type"]})
                    result1 = subprocess.run(cmd0 + ["object", "properties", chart_id, f"--app={app_id}"],
                                             capture_output=True, text=True)
                    print("Chart : qlik app object properties " + chart_id + " --app=" + app_id)

                    # chart_info = json.loads(result1.stdout)
                    chart_info = {}
                    if result1.stdout is not None:
                        try:
                            chart_info = json.loads(result1.stdout)
                            # Process the parsed data here
                        except ValueError as e:
                            print("Error2: Invalid JSON format -", e)
                    else:
                        print("Error2: JSON object is None")

                    # print("Chart info:")
                    # print(json.dumps(chart_info, indent = 3))
                    # qFieldDefs = []
                    # flag = []
                    x = 0
                    # print("New row:")
                    if "qHyperCubeDef" in chart_info:
                        qHyperCubeDef = chart_info["qHyperCubeDef"]

                        ## dimensions
                        for dimension in qHyperCubeDef["qDimensions"]:
                            for i in range(len(dimension["qDef"]["qFieldDefs"])):
                                # print("my dimension information is coming as: ",dimension["qDef"]["qFieldDefs"][i])
                                # qFieldDefs.append(dimension["qDef"]["qFieldDefs"][i])
                                # flag.append("Dimension")
                                # print("Dimension :", dimension["qDef"]["qFieldDefs"][i])
                                # print(type(dimension["qDef"]["qFieldDefs"][i]))
                        #                             qFieldDefs.append(dimension["qDef"]["qFieldDefs"])
                                x = 1
                                l = [dimension["qDef"]["qFieldDefs"][i]]
                                print("Dimension")
                                sheets3.append({"Sheet Title": sheet_info["qMetaDef"]["title"],
                                                "Chart Name": cell["type"], "Flag": "Dimension",
                                                "Measure/Dimension": l, "Equivalent DAX": 'No DAX'
                                                })

                        ## measures
                        for measure in qHyperCubeDef["qMeasures"]:
                            if "qLibraryId" in measure:
                                measure_id = measure["qLibraryId"]
                                result1 = subprocess.run(
                                    cmd0 + ["measure", "properties", measure_id, f"--app={app_id}"],
                                    capture_output=True, text=True)
                                print("Measure : qlik app measure properties " + measure_id + " --app=" + app_id)


                                # measure_info = json.loads(result1.stdout)
                                measure_info = {}
                                if result1.stdout is not None:
                                    try:
                                        measure_info = json.loads(result1.stdout)
                                        # Process the parsed data here
                                    except ValueError as e:
                                        print("Error3: Invalid JSON format -", e)
                                else:
                                    print("Error3: JSON object is None")

                                # print("Measure Info:")
                                # print(json.dumps(measure_info, indent = 3))
                                # qFieldDefs.append(measure_info["qMeasure"]["qDef"])
                                # flag.append("Measure")
                                # print("1Measure :", measure_info["qMeasure"]["qDef"])
                                # print(type(measure_info["qMeasure"]["qDef"]))
                                x = 1
                                l = [measure_info["qMeasure"]["qDef"]]
                                print("Measure")
                                dax_l = dax_expression(measure_info["qMeasure"]["qDef"])
                                # print(dax_l)
                                sheets3.append({"Sheet Title": sheet_info["qMetaDef"]["title"],
                                                "Chart Name": cell["type"], "Flag": "Measure",
                                                "Measure/Dimension": l, "Equivalent DAX": dax_l
                                                })
                                # qMeasureDefs.append({"Measure ID": measure_id, "Measure Title": measure_info["qMetaDef"]["title"], "qLabel": measure_info["qMeasure"]["qLabel"], "qDef": measure_info["qMeasure"]["qDef"]})
                            else:
                                # print("my measure information is coming as: ",measure["qDef"]["qDef"])
                                # qFieldDefs.append(measure["qDef"]["qDef"])
                                # flag.append("Measure")
                                # print("2Measure :", measure["qDef"]["qDef"])
                                # print(type(measure["qDef"]["qDef"]))
                                x = 1
                                l = [measure["qDef"]["qDef"]]
                                print("Measure")
                                dax_l = dax_expression(measure["qDef"]["qDef"])
                                # print(dax_l)
                                sheets3.append({"Sheet Title": sheet_info["qMetaDef"]["title"],
                                                "Chart Name": cell["type"], "Flag": "Measure",
                                                "Measure/Dimension": l, "Equivalent DAX": dax_l
                                                })

                    if(x==0):
                        # Append sheet information to the list
                        sheets3.append({"Sheet Title": sheet_info["qMetaDef"]["title"],
                                        "Chart Name": cell["type"],
                                        "Measure/Dimension": "NA", "Flag": "NA", "Equivalent DAX": 'NA'
                                        })

                # If no charts in sheet, append sheet information without chart details
                if len(sheets2) == 0:
                    sheets2.append({"Sheet Title": sheet_info["qMetaDef"]["title"]})
                if len(sheets3) == 0:
                    sheets3.append({"Sheet Title": sheet_info["qMetaDef"]["title"]})

    # print("sheet3 : ", sheets3)
    process_sheets(sheets1, data["sheets"], app_name)
    # process_sheets(sheets2, data["data2"], app_name)
    process_sheets(sheets3, data["measuresDimension"], app_name)

# Convert the data to a pandas dataframe
dashBoard_frame = pd.DataFrame(data["dashBoard"])
dataSource_frame = pd.DataFrame(data["dataSource"])
tableColumn_frame = pd.DataFrame(data["tableColumn"])
sheet_frame = pd.DataFrame(data["sheets"])
measureDimension_frame = pd.DataFrame(data["measuresDimension"])
dataSourceQuery_frame = pd.DataFrame(data["dataSourceQuery"])



# Create an Excel writer using openpyxl as the engine
writer = pd.ExcelWriter('Qlik_Extractor.xlsx', engine='openpyxl')

# Write each dataframe to a separate sheet
dashBoard_frame.to_excel(writer, sheet_name='Dashboard', index=False)
dataSource_frame.to_excel(writer, sheet_name='Data Source', index=False)
tableColumn_frame.to_excel(writer, sheet_name='Table Column', index=False)
sheet_frame.to_excel(writer, sheet_name='Sheet', index=False)
measureDimension_frame.to_excel(writer, sheet_name='Measure Dimension', index=False)
dataSourceQuery_frame.to_excel(writer, sheet_name='Data Source Query', index=False)

# Get the workbook object
workbook = writer.book

cnt = 0
for sheet_name in writer.sheets:
    sheet = workbook[sheet_name]
    cnt = cnt + 1
    # Apply wrap text to each sheet
    for column_cells in sheet.columns:
        for cell in column_cells:
            cell.alignment = Alignment(wrap_text=True)

    # Adjust column width based on content
    for column in sheet.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2  # Add padding and adjust the scaling factor as needed
        sheet.column_dimensions[column[0].column_letter].width = adjusted_width

    # Assign table name to the sheet
    table = Table(displayName='table' + str(cnt), ref=sheet.dimensions)
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    table.tableStyleInfo = style
    sheet.add_table(table)

# Save the workbook
writer.close()




# Convert the data dictionary to a JSON string
output_json = json.dumps(data, indent=4)

# Save the JSON string to a file
with open('Qlik_Extractor.json', 'w') as file:
    file.write(output_json)

