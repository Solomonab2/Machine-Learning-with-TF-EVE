import urllib.request
from urllib.parse import urljoin
import shutil
import os
import tarfile
from os.path import exists
from common import directory_methods as dm
# ----------------------------------------------------------------------------------------------------------------------
"""
download_json_data.py 

    This script navigates to 'https://data.everef.net/killmails/' and downloads the .tar.bz2 killmail
    json dumps for a given year, month, and day. The script then extracts the data into folders 
    inside of Killmail_Storage for later use with the WhoWouldWin_DataSetup.py.

"""
# ----------------------------------------------------------------------------------------------------------------------

# --------- Functions, Methods, and Classes: ---------------------------------------------------------------------------
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()

# ----------------------------------------------------------------------------------------------------------------------

# --------- Variables --------------------------------------------------------------------------------------------------
download_year = "2022"
download_month = "01"
download_first_day = "01"
# ----------------------------------------------------------------------------------------------------------------------

# ---------- Download the data -----------------------------------------------------------------------------------------
def download(download_year, download_month, download_first_day, number_of_days):
    """ download and extract json data from the everef website """

    download_page_url = "https://data.everef.net/killmails/"
    download_page_extension = download_year + '/'
    download_page_string = urljoin(download_page_url, download_page_extension)
    root_path = dm.getParentDir(dm.getCurrDir())
    killmails_path = os.path.join(root_path, 'allkillmails')

    if not os.path.isdir(killmails_path):
        print('    %s does not exist. Creating...')
        os.mkdir(killmails_path)

    print("    Preparing to download %d days of killmail data, beginning with %d-%d-%d" %
          (number_of_days, int(download_year), int(download_month), int(download_first_day)))
    for index in range(int(download_first_day), int(download_first_day) + number_of_days):
        """Correct days from 1 -> 01, 2 -> 02, etc."""
        day_number = index
        if day_number < 10:
            day_string = "0" + str(day_number)
        else:
            day_string = str(day_number)

        """Set up strings and paths"""
        download_extension_string = "killmails-" + download_year + "-" + download_month + "-" + day_string + ".tar.bz2"
        download_url = urljoin(download_page_string, download_extension_string)
        file_extension_string = "killmails-" + download_year + "-" + download_month + "-" + day_string + ".tar.bz2"
        file_path = os.path.join(killmails_path, file_extension_string)
        directory_extension_string = "killmails-" + download_year + "-" + download_month + "-" + day_string + ""
        directory_name = os.path.join(killmails_path, directory_extension_string)

        """Check if the specific killmail directory already exists:"""
        if not os.path.isdir(directory_name):
            """Check if the .tar file already exists"""
            if not exists(file_path):
                print("        - Downloading file: %s ..." % file_path)
                with opener.open(download_url) as response, open(file_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            else:
                print("        - File: %s exists, skipping download..." % file_extension_string)

            print("        - Extracting and creating directory %s ..." % directory_name)

            """Extract the tar file"""
            with tarfile.open(file_path) as tar:
                subdir_and_files = [
                    tarinfo for tarinfo in tar.getmembers()
                    if tarinfo.name.startswith("killmails/")
                ]
                tar.extractall(members=subdir_and_files, path=directory_name)

            """Delete the downloaded .tar files"""
            if exists(file_path):
                print("        - Deleting zipped file...")
                os.remove(file_path)
            else:
                pass
        else:
            print("        - Directory: %s exists, skipping..." % directory_extension_string)
    print("    Setup file directories successfully!")
# ----------------------------------------------------------------------------------------------------------------------





