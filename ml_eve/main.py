from datafetch import dataframe_setup, download_json_data
# ----------------------------------------------------------------------------------------------------------------------
"""
main.py 

    This script uses the Data Fetching And Management scripts to download killmails from a desired number of days,
    create lists of the target data, and finally generate the dataframe to be used in the TensorFlow ML models.

    Modify the desired variables below and run the script to get the data lists and generate the dataframe. 
    Currently only supports one month of data at a time.
"""
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
""" Variables to modify """
download_year = '2022'           # Download year
download_month = '01'            # Download month
download_first_day = '01'        # First day to download
download_number_of_days = 25     # Number of days of json data to download

# ----------------------------------------------------------------------------------------------------------------------
""" Setting up the data """

# Run the Json_Data_Download.py using our custom values to populate the data lists
print('1. Attempting to download json data...')
download_json_data.download(download_year, download_month, download_first_day,
                                download_number_of_days)
print('\n')

# Run the Dataframe_Setup_and_Save.py to use the data lists to generate the dataframe
print('2. Attempting to convert json data to lists and populate dataframe...')
dataframe_setup.setup()
print('\n')
# ----------------------------------------------------------------------------------------------------------------------


