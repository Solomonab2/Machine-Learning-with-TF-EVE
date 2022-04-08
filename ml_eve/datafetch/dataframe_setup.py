import os
import json
import pandas as pd
from os.path import exists
from common import list_methods as lm
from common import directory_methods as dm
# ----------------------------------------------------------------------------------------------------------------------
"""
dataframe_setup.py 

    This script takes the downloaded json killmail data from the individual day-folders inside the
    /data folder and uses it to populate and save lists of the kills that satisfy our data
    requirements. Then the script loads these lists into a Pandas dataframe and saves it as a .csv.
"""
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
""" set up the dataframe """
def setup():
    """ read killmail .jsons from inside the /allkillmails directory and,
        - load data into lists
        - preprocess the data as needed
        - populate dataframe
        - save list files and the dataframe
    """

    # Get config file with the data list names
    with open("data_config.json") as json_data_file:
        data_config = json.load(json_data_file)

    ship_id_list_name = data_config['ship_id_list_name']
    is_winner_list_name = data_config['is_winner_list_name']
    attacker_ship_list_name = data_config['attacker_ship_list_name']
    attacker_corp_list_name = data_config['attacker_corp_list_name']
    victim_ship_list_name = data_config['victim_ship_list_name']
    victim_corp_list_name = data_config['victim_corp_list_name']
    time_list_name = data_config['time_list_name']
    hour_list_name = data_config['hour_list_name']
    data_frame_name = data_config['data_frame_name']

    root_path = dm.getParentDir(dm.getCurrDir())
    killmails_path = os.path.join(root_path, 'allkillmails')
    data_path = os.path.join(root_path, 'data')

    ship_id_list_path = os.path.join(data_path, ship_id_list_name)
    is_winner_list_path = os.path.join(data_path, is_winner_list_name)
    attacker_ship_list_path = os.path.join(data_path, attacker_ship_list_name)
    attacker_corp_list_path = os.path.join(data_path, attacker_corp_list_name)
    victim_ship_list_path = os.path.join(data_path, victim_ship_list_name)
    victim_corp_list_path = os.path.join(data_path, victim_corp_list_name)
    time_list_path = os.path.join(data_path, time_list_name)
    hour_list_path = os.path.join(data_path, hour_list_name)
    data_frame_path = os.path.join(data_path, data_frame_name)

    directory_list = dm.listdirs(killmails_path)

    # ------------------------------------------------------------------------------------------------------------------
    """ Do the work """
    if not exists(data_frame_path):
        # Set up lists
        approved_ship_list = lm.readListFile(ship_id_list_path)
        attacker_ship_list, attacker_corp_list, victim_ship_list, victim_corp_list, time_list, is_winner_list = []
        for killmail_folder in directory_list:
            # Iterate each killmail inside the killmails folder
            jsons_extension = killmail_folder + "/killmails/"
            jsons_path = os.path.join(killmails_path, jsons_extension)
            print("    Fetching data from %s ..." % killmail_folder)
            for file_name in [file for file in os.listdir(jsons_path) if file.endswith('.json')]:
                # Open each killmail .json and read the data
                with open(jsons_path + file_name) as json_file:
                    data = json.load(json_file)
                    # Get the keys of the json contents
                    attackerKeys = data['attackers'][0].keys()
                    victimKeys = data['victim'].keys()
                    if len(data['attackers']) == 1 and 'ship_type_id' in attackerKeys and 'ship_type_id' in victimKeys:
                        # Check if killmail was solo kill and both attacker and victim ship ids are included
                        attacker_ship = str(data['attackers'][0]['ship_type_id'])
                        victim_ship = str(data['victim']['ship_type_id'])
                        if attacker_ship in approved_ship_list and victim_ship in approved_ship_list and attacker_ship != victim_ship:
                            # Check if ships are in the approved list and that victim ship and attacker ship are not the same
                            # and then write data to lists
                            attacker_ship_list.append(int(attacker_ship))
                            victim_ship_list.append(int(victim_ship))
                            time_list.append(data['killmail_time'])
                            if 'corporation_id' in attackerKeys:
                                attacker_corp_list.append(data['attackers'][0]['corporation_id'])
                            else:
                                attacker_corp_list.append(0)

                            if 'corporation_id' in victimKeys:
                                victim_corp_list.append(data['victim']['corporation_id'])
                            else:
                                victim_corp_list.append(0)

        print("    Finished loading individual killmail jsons. Preprocessing data now...")

        """Winner list preprocessing:"""
        for index in range(len(attacker_ship_list)):
            is_winner_list.append(1)

        for index in range(len(attacker_ship_list)):
            is_winner_list.append(0)
            attacker_ship_list.append(victim_ship_list[index])
            victim_ship_list.append(attacker_ship_list[index])
            attacker_corp_list.append(victim_corp_list[index])
            victim_corp_list.append(attacker_corp_list[index])
            time_list.append(time_list[index])

        """Time Preprocessing:"""
        hour_list = []
        for item in time_list:
            date, time = item.split('T')
            hour, minute, second = time.split(':')
            hour_list.append(int(hour))

        lm.writeListFile(is_winner_list_path, is_winner_list)
        lm.writeListFile(attacker_ship_list_path, attacker_ship_list)
        lm.writeListFile(victim_ship_list_path, victim_ship_list)
        lm.writeListFile(attacker_corp_list_path, attacker_corp_list)
        lm.writeListFile(victim_corp_list_path, victim_corp_list)
        lm.writeListFile(time_list_path, time_list)
        lm.writeListFile(hour_list_path, hour_list)

        print("    All Data Loaded Successfully! Populating Dataframe...")

        """Create Pandas dataframe, fill with list data, and save as .csv"""
        dataframe_data = {
            'is_winner': is_winner_list,
            'attacker_ship': attacker_ship_list,
            'victim_ship': victim_ship_list,
            'attacker_corp': attacker_corp_list,
            'victim_corp': victim_corp_list,
            'time': time_list,
            'hour': hour_list
        }
        my_dataframe = pd.DataFrame(data=dataframe_data)
        print("    Dataframe Successfully Created. Saving...")
        my_dataframe.to_csv(data_frame_path)
        print("    Dataframe File Saved Successfully.")
    else:
        print("    Dataframe File Already Exists! Delete and Rerun Program To Update!")
    # ------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------








