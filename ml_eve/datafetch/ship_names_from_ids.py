import os
from os.path import exists
from common import get_esi_names
from common import list_methods as lm
from common import directory_methods as dm
# ----------------------------------------------------------------------------------------------------------------------
"""
ship_names_from_ids.py 

    This script uses the ship_id_list.txt to generate a ship_names_list.txt 
    using the EVE ESI API universe.getnames call.

"""
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
""" Fixed path variables """
root_path = dm.getParentDir(dm.getCurrDir())

data_path = os.path.join(root_path, 'data')

ship_id_file_name = 'ship_id_list.txt'
ship_id_list_path = os.path.join(data_path, ship_id_file_name)

ship_names_list_name = 'ship_names_list.txt'
ship_names_list_path = os.path.join(data_path, ship_names_list_name)

# ----------------------------------------------------------------------------------------------------------------------
"""Write the list and saved it"""
if not exists(ship_names_list_path):
    # Read the id list and store it

    ship_id_list = lm.readListFile(ship_id_list_path)
    # Run the function that calls the ESI API
    response_list = get_esi_names.get(ship_id_list)


    # Generate the names list
    ship_names_list = []
    for item in response_list:
        ship_names_list.append(item['name'])
    # Write names list to file
    lm.writeListFile(ship_names_list_path, ship_names_list)
else:
    print('%s exists!' % ship_names_list_name)
# ----------------------------------------------------------------------------------------------------------------------
