# CARB Facility Matching: Desktop GUI
 
## Setting Up the Tool
<ol>
 <li>Install <a href="https://www.python.org/downloads/">Python 3</a> onto your personal computer.</li>
 <ul>
  <li>This application was developed and tested on Python 3.9 but it may be compatible with similar versions.</li>
  <li>DO NOT use ArcGIS Pro's Python installation, it will result in errors when setting up the tool. Please use a stand alone or Anaconda Python installation.</li>
 </ul>
 <li>Download the reposity by clicking the green "Code" button on this page and selecting "Download ZIP".</li>
 <li>Unzip the code into an approprate folder.</li>
 <li>Open CARB-Facility_Matching-DesktopGUI/dev/setup.py and change the pathways on lines 7-9 to the workspace, parcel parquet file, and Golden Master database respectively.</li>
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
This is a sentence in regular text. <span style="color:blue; font-weight:bold;">This sentence is bold and blue.</span> This is another regular sentence.
<ul>
 <li><span style="color:#FFCC66;font-weight:bold;">Input Table Records</span>:</li>
 <li><span style="color:#FF7C80;font-weight:bold;">Standardized Input Table Records</span>:</li>
 <li><span style="color:#66FF33;font-weight:bold;">Match Info</span>:</li>
 <li><span style="color:#9999FF;font-weight:bold;">Match Criteria</span>:</li>
 <li><span style="color:#33CCFF;font-weight:bold;">Master Table Records</span>:</li>
</ul>

Note make sure there are no duplicate ARBID's in the master table.
