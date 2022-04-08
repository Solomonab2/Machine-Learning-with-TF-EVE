import os
import pandas as pd
import tensorflow as tf
# ----------------------------------------------------------------------------------------------------------------------
"""
ModelTester.py 

    This script uses the built models to generate predictions. Modify the list of desired ships and run script to
    generate custom predictions.
    
"""
# ----------------------------------------------------------------------------------------------------------------------

# Variables to modify: -------------------------------------------------------------------------------------------------
custom_attacker_ship_names = [
    'Tengu',
    'Rifter',
    'Loki'
]
custom_victim_ship_names = [
    'Loki',
    'Heron',
    'Legion'
]

model_to_use = 'www_binary_classification_2'
# ----------------------------------------------------------------------------------------------------------------------

# Methods: -------------------------------------------------------------------------------------------------------------
def readListFile(filePath):
    inList = []
    f = open(filePath, 'r', encoding='utf-8')
    for x in f.readlines():
        temp = x.rstrip("\n")
        inList.append(temp)
    print("File: "+filePath+" Read Successfully!")
    return inList

def getCurrDir():
    return os.getcwd()

def getParentDir(path):
    return os.path.abspath(os.path.join(path, os.pardir))
# ----------------------------------------------------------------------------------------------------------------------

# Fixed paths: ---------------------------------------------------------------------------------------------------------
main_directory_path = getParentDir(getParentDir(getCurrDir()))

storage_files_path = os.path.join(main_directory_path, 'Storage_Files')

ml_code_folder_extension = 'Code/ML Code/SavedModels'

saved_models_path = os.path.join(main_directory_path, ml_code_folder_extension)

model_path = os.path.join(saved_models_path, model_to_use)

ship_id_file_name = 'ship_id_list.txt'
ship_id_list_path = os.path.join(storage_files_path, ship_id_file_name)

ship_names_list_name = 'ship_names_list.txt'
ship_names_list_path = os.path.join(storage_files_path, ship_names_list_name)
# ----------------------------------------------------------------------------------------------------------------------

# Convert ship names to id's using the ship_id_list.txt and ship_names_list.txt files: ---------------------------------
custom_attacker_ship_ids = []
custom_victim_ship_ids = []

ship_id_list = readListFile(ship_id_list_path)
ship_names_list = readListFile(ship_names_list_path)

for attacker_name in custom_attacker_ship_names:
    name_index = ship_names_list.index(attacker_name)
    custom_attacker_ship_ids.append(int(ship_id_list[name_index]))

for victim_name in custom_victim_ship_names:
    name_index = ship_names_list.index(victim_name)
    custom_victim_ship_ids.append(int(ship_id_list[name_index]))
# ----------------------------------------------------------------------------------------------------------------------

# Create the custom features with the ID numbers: ----------------------------------------------------------------------
custom_data = {'attacker_ship': custom_attacker_ship_ids, 'victim_ship': custom_victim_ship_ids}
custom_df = pd.DataFrame(custom_data)

custom_features = {
    'attacker_ship': custom_df['attacker_ship'],
    'victim_ship': custom_df['victim_ship']
}
# ----------------------------------------------------------------------------------------------------------------------

# Load model and make predictions: -------------------------------------------------------------------------------------
# model = tf.keras.models.load_model('SavedModels/www_binary_classification_2')
model = tf.keras.models.load_model(model_path)
prediction_labels_custom = model.predict(custom_features)
# ----------------------------------------------------------------------------------------------------------------------

# Print formatted results: ---------------------------------------------------------------------------------------------
for prediction_index in range(len(prediction_labels_custom)):
    var1 = custom_attacker_ship_names[prediction_index]
    var2 = custom_victim_ship_names[prediction_index]
    var3 = prediction_labels_custom[prediction_index][0]
    print('%s vs %s: %.3f' % (var1, var2, var3))
# ----------------------------------------------------------------------------------------------------------------------
