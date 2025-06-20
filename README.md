# CARB Facility Matching: Desktop GUI
 
## Setting Up the Tool
<ol>
 <li>Install <a href="https://www.python.org/downloads/">Python 3</a> onto your personal computer.</li>
 <ul>
  <li>This application was developed and tested on Python 3.9 but it may be compatible with similar versions.</li>
  <li>DO NOT use ArcGIS Pro's Python installation, it will result in errors when setting up the tool. Please use a stand alone Python installation.</li>
 </ul>
 <li>Download the reposity by clicking the green "Code" button on this page and selecting "Download ZIP".</li>
 <li>Unzip the code into an approprate folder.</li>
 <li>Open CARB-Facility_Matching-DesktopGUI/dev/setup.py and change the pathways on lines 7-9 to the workspace, parcel parquet file, and master facility database file respectively.</li>
 <li>Run CARB-Facility_Matching-DesktopGUI/dev/setup.py.</li>
 <li>A file called FacIdentifier.exe will appear within the CARB-Facility_Matching-DesktopGUI folder. Open this to access the tool.</li>
</ol>

## Running the Tool
<ol>
 <li>Open FacIdentifier.exe.</li>
 <li>Select an excel file and sheet containing the input data for the tool.</li>
 <li>Click "Load".</li>
 <li>Perform field configuration to match the field names from the input excel file to the field names recognized by the tool.</li>
 <li>Select the output file location.</li>
 <li>Click "Execute".</li>
</ol>

## Output of the Tool
The tool outputs an excel file containing the results of facility matching. The output data is distinguish by different colored headers representing:
<ul>
 <li><b>Input Table Records:</b> Records from the input excel file.</li>
 <li><b>Standardized Input Table Records:</b> A subset of the input excel file records that have been standardized for facility matching.</li>
 <li><b>Match Info:</b> The ARBID and score of the match.</li>
 <li><b>Match Criteria:</b> A modified facility matching criteria matrix flagging field values that may be mismatched or blank.</li>
 <li><b>Master Table Records:</b> The standardized matched record from the master facility table.</li>
</ul>

## Updating the Tool
The "main" brach of this repository should contain the most up-to-date operational code for the tool. The "ERG" branch contains the source code of the application delivered to CARB in May 2024. Re-run setup.py to incorporate changes into the tool. <b>DO NOT</b> push the files generated from setup.py onto the repository, it will take up a significant amount of storage space here.

The "docs/Guidance on Potential Tool Updates.pdf" file contains instructions on how to perform the following updates to the tool:
<ul>
 <li>Incorporating an alternative database.</li>
 <li>Adding fields to the matching algorithm.</li>
 <li>Updating the parcel dataset.</li>
</ul>

## Encountered Issues and Solutions
If you encounter a PyInstaller issue during the tool set up, place CARB-Facility_Matching-DesktopGUI-main in the Documents folder, adjust the working directory in setup.py, and re-run setup.py.
<br><br><br>
Please email tyler.richman@erg.com for access to make edits to this repository or if you have any questions regarding this tool.
