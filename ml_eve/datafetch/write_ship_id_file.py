import os
from os.path import exists
import json
from common import list_methods as lm
from common import directory_methods as dm
# ----------------------------------------------------------------------------------------------------------------------
"""
write_ship_id_file.py 

    This script uses the converted .json data from the eve .yaml data dump in order to create
    a list of ship ID's based on the group of the ship. This data is then used in the 
    WhoWouldWin_DataSetup.py in order to create lists of only the kills that have these
    ships listed for attacker and victims. 

"""
# ----------------------------------------------------------------------------------------------------------------------

# --------- Variables ----------------------------------------------------------------------------------------------====

item_id_list, total_item_list, item_name_list, item_group_list = []
myJsonData = ""

data_path = os.path.join(dm.getParentDir(dm.getCurrDir()), 'data')

ship_id_file_name = 'ship_id_list.txt'
ship_id_list_path = os.path.join(data_path, ship_id_file_name)

json_file_name = 'yaml_to_json_data.json'
json_data_file_path = os.path.join(data_path, json_file_name)

included_ship_groups_list = ['31', '237', '25', '324', '830', '893', '831', '1527', '420',
                             '1534', '541', '1305', '26', '358', '894', '832', '906', '963',
                             '419', '540', '27', '898', '900', '547', '659', '485', '1538',
                             '30', '513', '902', '28', '1202', '1283', '463', '543', '28',
                             '941', '513', '883']
# ----------------------------------------------------------------------------------------------------------------------

# --------- Write the list ---------------------------------------------------------------------------------------------
if not exists(ship_id_list_path):
    if exists(json_data_file_path):
        print("        Json Data File Found! Reading File...")
        with open(json_data_file_path) as json_file:
            myJsonData = json.load(json_file)

        stop_index = len(myJsonData)
        for index in range(stop_index):
            str_index = str(index)
            item_id_list.append(index)
            try:
                jsonDataKeys = myJsonData[str_index].keys()
                if 'name' in jsonDataKeys and 'groupID' in jsonDataKeys:
                    total_item_list.append(myJsonData[str_index])
                    item_name_list.append(myJsonData[str_index]['name']['en'])
                    item_group_list.append(myJsonData[str_index]['groupID'])
                else:
                    total_item_list.append('N/A')
                    item_name_list.append('N/A')
                    item_group_list.append('N/A')
            except:
                total_item_list.append('N/A')
                item_name_list.append('N/A')
                item_group_list.append('N/A')

        new_id_list = []
        new_name_list = []
        for index in range(0, len(item_id_list)):
            group = str(item_group_list[index])
            if group in included_ship_groups_list:
                new_id_list.append(str(index))
                new_name_list.append(str(item_name_list[index]))

        lm.writeListFile(ship_id_list_path, new_id_list)
    else:
        print("        %s not found!" % json_data_file_path)
else:
    print("    Data Exists!")
# ----------------------------------------------------------------------------------------------------------------------
