import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import feature_column
from common import directory_methods as dm
from common import plotting_methods as pm
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

# Split into train and test datasets
train_split = 0.7
train = main_df.sample(frac=train_split, random_state=0)
test = main_df.drop(train.index)

# Shuffle the datasets
test = test.reindex(np.random.permutation(test.index))
train = train.reindex(np.random.permutation(train.index))

# Create vocab list of all ship id's
attacker_list = list(main_df['attacker_ship'])
victim_list = list(main_df['victim_ship'])
combined_list = attacker_list + victim_list
ship_vocab_list = []
for item in combined_list:
    if item not in ship_vocab_list:
        ship_vocab_list.append(item)
ship_vocab_list.sort()
print(ship_vocab_list)


# ----------------------------------------------------------------------------------------------------------------------
""" Create feature columns and the feature layer  """

feature_columns = []

# Attacker ship categorical column:
categorical_attacker = feature_column.categorical_column_with_vocabulary_list(
    key='attacker_ship', vocabulary_list=ship_vocab_list, default_value=0)
feature_columns.append(feature_column.embedding_column(categorical_attacker, dimension=8))
# Victim ship categorical column:
categorical_victim = feature_column.categorical_column_with_vocabulary_list(
    key='victim_ship', vocabulary_list=ship_vocab_list, default_value=0)
feature_columns.append(feature_column.embedding_column(categorical_victim, dimension=8))

feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

# ----------------------------------------------------------------------------------------------------------------------
""" Build, train, and evaluate the model """

epochs = 5
batch_size = 5
learning_rate = 0.1
validation_split = 0.2
classification_threshold = 0.65

model = tf.keras.Sequential([
    feature_layer,
    layers.Dense(units=1, input_shape=(1,), activation=tf.sigmoid),
])

METRICS = [
    tf.keras.metrics.BinaryAccuracy(name='accuracy', threshold=classification_threshold),
    tf.keras.metrics.Precision(thresholds=classification_threshold, name='precision'),
    tf.keras.metrics.Recall(thresholds=classification_threshold, name='recall'),
    tf.keras.metrics.AUC(num_thresholds=100, name='auc'),
]


model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=learning_rate),
    loss=tf.keras.losses.BinaryCrossentropy(),
    metrics=METRICS)

train_features = {'attacker_ship': train['attacker_ship'], 'victim_ship': train['victim_ship']}
train_labels = train['is_winner']
history = model.fit(x=train_features, y=train_labels, validation_split=validation_split, epochs=epochs)

epochs = history.epoch
hist = pd.DataFrame(history.history)

list_of_metrics_to_plot = ['accuracy', 'precision', 'recall']

pm.plot_metrics(epochs, hist, list_of_metrics_to_plot)

test_features = {'attacker_ship': test['attacker_ship'], 'victim_ship': test['victim_ship']}
test_labels = test['is_winner']
loss, accuracy, precision, recall, auc = model.evaluate(x=test_features, y=test_labels)
print(model.summary())

model.save('SavedModels/www_binary_classification_1')

# Make Predictions:  ---------------------------------------------------------------------------------------------------
prediction_features = test_features.copy()
prediction_labels = model.predict(prediction_features)
actual_labels = list(test['is_winner'])
for index in range(50):
    print(str(index)+": Actual: "+str(actual_labels[index])+" | Predicted: "+str(prediction_labels[index]))
# ----------------------------------------------------------------------------------------------------------------------



