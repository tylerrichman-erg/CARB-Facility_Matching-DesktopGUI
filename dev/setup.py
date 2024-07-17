import os
import shutil
import subprocess

class App:
    def __init__(self):
        self.workspace_folder = r""
        self.parcel_parquet_file = r""
        self.facility_database_loc = r""

if __name__ == "__main__":
    App = App()

    main_exe_folder_location = os.path.join(App.workspace_folder, r"exe")
    activate_venv_command = os.path.join(App.workspace_folder, r"fm-desktop-env\Scripts\activate.bat")
    python_exe_location = os.path.join(App.workspace_folder, r"fm-desktop-env\Scripts\python.exe")
    pip_exe_location = os.path.join(App.workspace_folder, r"fm-desktop-env\Scripts\pip.exe")
    pyinstaller_exe_location = os.path.join(App.workspace_folder, r"fm-desktop-env\Scripts\pyinstaller.exe")
    main_py_location = os.path.join(App.workspace_folder, r"dev\main.py")
    icon_location = os.path.join(App.workspace_folder, r"dev\icons\icons8-f-67.png")
    output_exe_location = os.path.join(App.workspace_folder, r"exe\dist\main.exe")
    final_exe_location = os.path.join(App.workspace_folder, r"FacIdentifier.exe")

    if os.path.exists(os.path.join(App.workspace_folder, "fm-desktop-env")):
        shutil.rmtree(os.path.join(App.workspace_folder, "fm-desktop-env"))

    if os.path.exists(main_exe_folder_location):
        shutil.rmtree(main_exe_folder_location)

    if not os.path.exists(main_exe_folder_location):
        os.makedirs(main_exe_folder_location)

    subprocess.run(['python', '-m', 'venv', os.path.join(App.workspace_folder, "fm-desktop-env")], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "geopandas"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "tk"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pillow"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "openpyxl"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pyarrow"], check=True)
    subprocess.run([activate_venv_command, "&&", python_exe_location, pip_exe_location, "install", "pyinstaller"], check=True)
    subprocess.run([activate_venv_command, "&&", "CD", main_exe_folder_location, "&&", pyinstaller_exe_location, "--onefile", f"--icon={icon_location}",main_py_location], check=True)

    shutil.copy(
        output_exe_location,
        final_exe_location
        )
