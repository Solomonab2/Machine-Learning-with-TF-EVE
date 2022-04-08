import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import feature_column
from tensorflow import keras
from tensorflow import feature_column

from matplotlib import pyplot as plt

from common import directory_methods as dm
from common import plotting_methods as pm
from common import list_methods as lm
import tf_ktuner
# ----------------------------------------------------------------------------------------------------------------------
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
    """ A utility method to create a tf.data dataset from a Pandas Dataframe """
    dataframe = dataframe.copy()
    labels = dataframe.pop('is_winner')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds
# ----------------------------------------------------------------------------------------------------------------------
""" Directory paths """
root_path = dm.getParentDir(dm.getCurrDir())
data_path = os.path.join(root_path, 'data')
dataframe_path = os.path.join(data_path, 'dataframe_csv.csv')

# ----------------------------------------------------------------------------------------------------------------------
""" Loading data """

# Load the csv file and shuffle
main_df = pd.read_csv(dataframe_path, index_col=0)
main_df = main_df.reindex(np.random.permutation(main_df.index))

batch_size = 32
ds = df_to_dataset(main_df, shuffle=True, batch_size=batch_size)

train_split = 0.7
train_count = int(train_split * len(ds))

train_ds = ds.take(train_count)
test_ds = ds.skip(train_count)

validation_split = 0.2
train_count = train_count - int(validation_split * train_count)

val_ds = train_ds.skip(train_count)
train_ds = train_ds.take(train_count)

# Create vocab list of all ship id's
all_ships_list_path = os.path.join(data_path, 'ship_id_list.txt')
all_ships_list = lm.readListFile(all_ships_list_path)
all_ships_list = [ int(x) for x in all_ships_list ]

# ----------------------------------------------------------------------------------------------------------------------
""" Create feature columns and the feature layer  """

feature_columns = []

# Attacker ship categorical column:
categorical_attacker = feature_column.categorical_column_with_vocabulary_list(
    key='attacker_ship', vocabulary_list=all_ships_list, default_value=0)
feature_columns.append(feature_column.embedding_column(categorical_attacker, dimension=8))
# Victim ship categorical column:
categorical_victim = feature_column.categorical_column_with_vocabulary_list(
    key='victim_ship', vocabulary_list=all_ships_list, default_value=0)
feature_columns.append(feature_column.embedding_column(categorical_victim, dimension=8))

# ----------------------------------------------------------------------------------------------------------------------
""" Build, train, and evaluate the model """

# Parameters for the tuner
min_middle_layer_units = 256
max_middle_layer_units = 512
middle_layer_units_step = 32
learning_rates = [1e-2, 1e-3]
loss_function = keras.losses.BinaryCrossentropy()
classification_threshold = 0.85
metrics = [
    tf.keras.metrics.BinaryAccuracy(name='accuracy', threshold=classification_threshold),
    tf.keras.metrics.Precision(thresholds=classification_threshold, name='precision'),
    tf.keras.metrics.Recall(thresholds=classification_threshold, name='recall'),
]
objective = 'val_accuracy'
max_tuning_epochs = 5
tuning_factor = 3
directory = 'ktuner'
project_name = 'ship_vs_ship_categorical_binary_classification_k_tuner'

tuner = tf_ktuner.setup_tuner_binary_classification(feature_columns, min_middle_layer_units, max_middle_layer_units,
                                                         middle_layer_units_step, learning_rates, loss_function, metrics,
                                                         objective, max_tuning_epochs, tuning_factor, directory, project_name)

# -----------------------------------------------------------------------------------------------------------------------
""" Run the hyperparameter search """
search_epochs = 5
stop_early_monitor = 'val_loss'
stop_early_patience = 5
best_hps = tf_ktuner.tune_hyperparameters(tuner, train_ds, val_ds, search_epochs, stop_early_monitor, stop_early_patience)

print(f"""
Optimal number of units in the first densely-connected
layer is: {best_hps.get('units')}  
""")

print(f"""
Optimal learning rate for the optimizer
is: {best_hps.get('learning_rate')}.
""")

# -----------------------------------------------------------------------------------------------------------------------
""" Train the model with the optimal hyperparameters and get the best epoch """
epochs_to_test = 4
objective = 'val_accuracy'
maximize_objective = True
best_epoch = tf_ktuner.get_best_epoch(tuner, train_ds, val_ds, best_hps, objective, maximize_objective, epochs_to_test)
print('Best epoch: %d' % (best_epoch,))

# -----------------------------------------------------------------------------------------------------------------------
""" Build the hypermodel """
# Re-instantiate the tuner with the optimal hyperparameters
hyperm1 = tuner.hypermodel.build(best_hps)
# Retrain the model with our optimal number of epochs
hyperhistory = hyperm1.fit(train_ds, validation_data=val_ds, epochs=best_epoch)

# Convert history to dataframe
epochs = hyperhistory.epoch
hist = pd.DataFrame(hyperhistory.history)

#-----------------------------------------------------------------------------------------------------------------------
""" Save the model """
saved_models_path = 'savedmodels'
model_name = 'categorical_binary_classification_ktuned'
save_path = os.path.join(saved_models_path, model_name)
hyperm1.save(save_path)

#-----------------------------------------------------------------------------------------------------------------------
""" Plot the accuracy, precision, and recall """
list_of_metrics_to_plot = ['accuracy', 'precision', 'recall']
pm.plot_metrics(epochs, hist, list_of_metrics_to_plot)

# ----------------------------------------------------------------------------------------------------------------------

