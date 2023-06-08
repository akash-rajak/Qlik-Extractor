# ✔ Qlik Extractor
- A python tool to extract the metadata from the Qlik Reports.

****

### How the tool works:
- Its basically a tool to extract the `qlik` report `metadata` and store the metadata in `Excel` and `JSON` file.
- This tool extracts the metadata from all the reports uploaded on the `Qlik Cloud` ([Qlik Cloud](https://www.qlik.com/us/products/qlik-cloud)).
- It extracts the following `metadata` from the Qlik Reports:
```
Dashboard
    - Dashboard ID
    - Dashboard Name
Data Source
    - Dashboard Name
    - Connection Name
    - Connection ID
    - Data Source
    - Data Source Type
    - Table Name
Table Column
    - Dashboard Name
    - Table Name
    - Table Columns
Sheet
    - Dashboard Name
    - Sheet Title
Measure Dimension
    - Dashboard Name
    - Sheet Title
    - Chart Name
    - Flag
    - Measure/Dimension
    - Equivalent DAX
Data Source Query
    - Dashboard Name
    - Table Name
    - Source Query
```
- The final output of the metadata are being stored in `Excel` and `JSON` file.

****

### IMP Notes/References:
- 
