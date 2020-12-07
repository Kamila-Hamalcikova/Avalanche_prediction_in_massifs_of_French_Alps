
import pathlib

# function to iterate over different paths for nc files with data for each year

def meteo_paths():
    meteo_files_path = pathlib.Path(".\\meteo_vars")
    file_paths = [str(meteo_file_path) for meteo_file_path in list(meteo_files_path.glob("*FORCING*.nc"))]
    return file_paths