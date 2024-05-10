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

Note make sure there are no duplicate ARBID's in the master table.
