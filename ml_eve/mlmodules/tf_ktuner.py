import keras_tuner as kt
import tensorflow as tf
from tensorflow import keras
# ----------------------------------------------------------------------------------------------------------------------
"""
tf_tuner.py

    This module is used by other modules to:
      - tune the hyperparameters for a given model
      - find the optimal number of epochs
"""
#-----------------------------------------------------------------------------------------------------------------------

def setup_tuner_linreg(feature_columns, min_middle_layer_units, max_middle_layer_units, middle_layer_units_step,
                learning_rates, loss_function, metrics, objective,
                max_tuning_epochs, tuning_factor, directory, project_name):
    """ Set up the keras tuner for a linear regression model """
    def model_builder(hp):
        """ Builds the model """
        # Define the model type and input layer
        model = keras.Sequential()
        model.add(keras.layers.DenseFeatures(feature_columns, name='features'))
        # Number of units in the first dense relu layer
        hp_units = hp.Int('units', min_value=min_middle_layer_units, max_value=max_middle_layer_units, step=middle_layer_units_step)
        model.add(keras.layers.Dense(units=hp_units, activation='relu', name='middlerelu'))
        # Define the output layer
        model.add(keras.layers.Dense(units=1, input_shape=[1]))
        # Define the learning rate values
        hp_learning_rate = hp.Choice('learning_rate', values=learning_rates)
        # Compile the model and return it
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
            loss=loss_function,
            metrics=metrics)
        return model

    # Instantiate the tuner
    tuner = kt.Hyperband(model_builder,
                         objective=objective,
                         max_epochs=max_tuning_epochs,
                         factor=tuning_factor,
                         directory=directory,
                         project_name=project_name)
    """ return the tuner """
    return tuner
#-----------------------------------------------------------------------------------------------------------------------

def setup_tuner_binary_classification(feature_columns, min_middle_layer_units, max_middle_layer_units, middle_layer_units_step,
               learning_rates, loss_function, metrics, objective,
               max_tuning_epochs, tuning_factor, directory, project_name):
    """ Set up the keras tuner for a binary classification model """
    def model_builder(hp):
        """ Builds the model """
        # Define the model type and input layer
        model = keras.Sequential()
        model.add(keras.layers.DenseFeatures(feature_columns, name='features'))
        # Number of units in the first dense relu layer
        hp_units = hp.Int('units', min_value=min_middle_layer_units, max_value=max_middle_layer_units, step=middle_layer_units_step)
        model.add(keras.layers.Dense(units=hp_units, activation='relu', name='middlerelu'))
        # Define the output layer
        model.add(keras.layers.Dense(units=1, activation=tf.sigmoid))
        # Define the learning rate values
        hp_learning_rate = hp.Choice('learning_rate', values=learning_rates)
        # Compile the model and return it
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
            loss=loss_function,
            metrics=metrics)
        return model

    # Instantiate the tuner
    tuner = kt.Hyperband(model_builder,
                         objective=objective,
                         max_epochs=max_tuning_epochs,
                         factor=tuning_factor,
                         directory=directory,
                         project_name=project_name)
    """ return the tuner """
    return tuner
#-----------------------------------------------------------------------------------------------------------------------

def tune_hyperparameters(tuner, train_ds, val_ds, search_epochs, stop_early_monitor, stop_early_patience):
    """ Tune the hyperparameters for a given tuner and dataset """
    # Create a callback for the early stopping
    stop_early = tf.keras.callbacks.EarlyStopping(monitor=stop_early_monitor, patience=stop_early_patience)
    # Run the hyperparameter search """
    tuner.search(train_ds, epochs=search_epochs, validation_data=val_ds, callbacks=[stop_early])
    # Get the optimal hyperparameters
    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    """ return the tuned hyperparameters """
    return best_hps
#-----------------------------------------------------------------------------------------------------------------------

def get_best_epoch(tuner, train_ds, val_ds, best_hps, objective, maximize_objective, epochs_to_test):
    """ Train the model with the optimal hyperparameters and get the history """
    # Create the model with our optimal hyperparameters
    m1 = tuner.hypermodel.build(best_hps)
    # Train the model and get the history
    history = m1.fit(train_ds, epochs=epochs_to_test, validation_data=val_ds)
    # Validation loss per epoch
    objective_per_epoch = history.history[objective]
    if maximize_objective:
        best_epoch = objective_per_epoch.index(max(objective_per_epoch)) + 1
    else:
        best_epoch = objective_per_epoch.index(min(objective_per_epoch)) + 1
    """ return the optimal epoch """
    return best_epoch
#-----------------------------------------------------------------------------------------------------------------------



















