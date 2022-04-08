import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import feature_column
from matplotlib import pyplot as plt

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

# Create vocab list of all corporation id's
corporation_list = list(main_df['attacker_corp'])
corporation_list += list(main_df['victim_corp'])
corp_vocab_list = []
for item in corporation_list:
    if item not in corp_vocab_list:
        corp_vocab_list.append(item)
corp_vocab_list.sort()
print(corp_vocab_list)

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

# This version of the model includes additional features: --------------------------------------------------------------

# # Attacker corp categorical column:
# categorical_attacker_corp = feature_column.categorical_column_with_vocabulary_list(
#     key='attacker_corp', vocabulary_list=corp_vocab_list, default_value=0)
# feature_columns.append(feature_column.embedding_column(categorical_attacker_corp, dimension=8))
# # Victim corp categorical column:
# categorical_victim_corp = feature_column.categorical_column_with_vocabulary_list(
#     key='victim_corp', vocabulary_list=corp_vocab_list, default_value=0)
# feature_columns.append(feature_column.embedding_column(categorical_victim_corp, dimension=8))
# # Hour numeric column:
# hour_numeric = feature_column.numeric_column('hour')
# feature_columns.append(hour_numeric)

# # Feature Cross (  Probability of collision = -k(k-1)/2(HashBucketSize)  )
# attacker_victim_crossed_column = feature_column.crossed_column(
#     [categorical_attacker, categorical_victim], hash_bucket_size=10000)
# attacker_victim_crossed_feature = feature_column.indicator_column(attacker_victim_crossed_column)
# feature_columns.append(attacker_victim_crossed_feature)

feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

# ----------------------------------------------------------------------------------------------------------------------
""" Build, train, and evaluate the model """

epochs = 10
batch_size = 20
learning_rate = 0.005
validation_split = 0.3
classification_threshold = 0.85

model = tf.keras.Sequential([
    feature_layer,
    layers.Dropout(rate=0.1),
    layers.Dense(units=128, activation='relu'),
    layers.Dropout(rate=0.1),
    layers.Dense(units=16, activation='relu'),
    layers.Dropout(rate=0.1),
    layers.Dense(units=1, input_shape=(1,), activation=tf.sigmoid),
])

METRICS = [
    tf.keras.metrics.BinaryAccuracy(name='accuracy', threshold=classification_threshold),
    tf.keras.metrics.Precision(thresholds=classification_threshold, name='precision'),
    tf.keras.metrics.Recall(thresholds=classification_threshold, name='recall'),
    tf.keras.metrics.AUC(num_thresholds=100, name='auc'),
]


model.compile(
    optimizer='adam',
    #optimizer=tf.keras.optimizers.RMSprop(learning_rate=learning_rate),
    loss=tf.keras.losses.BinaryCrossentropy(),
    metrics=METRICS
)

train_features = {
    'attacker_ship': train['attacker_ship'],
    'victim_ship': train['victim_ship'],
    'attacker_corp': train['attacker_corp'],
    'victim_corp': train['victim_corp'],
    'hour': train['hour']
}
train_labels = train['is_winner']
history = model.fit(x=train_features, y=train_labels, validation_split=validation_split, epochs=epochs)

epochs = history.epoch
hist = pd.DataFrame(history.history)

metrics_to_plot = ['accuracy', 'precision', 'recall']

pm.plot_metrics(epochs, hist, metrics_to_plot)

test_features = {
    'attacker_ship': test['attacker_ship'],
    'victim_ship': test['victim_ship'],
    'attacker_corp': test['attacker_corp'],
    'victim_corp': test['victim_corp'],
    'hour': test['hour']
}
test_labels = test['is_winner']
loss, accuracy, precision, recall, auc = model.evaluate(x=test_features, y=test_labels)
print(model.summary())

plt.plot(epochs, hist['val_loss'], 'b-')
plt.plot(epochs, hist['val_accuracy'], 'b--')
plt.plot(epochs, hist['val_precision'], 'b-.')
plt.plot(epochs, hist['val_recall'], 'b:')
plt.plot(epochs, hist['loss'], 'r-')
plt.plot(epochs, hist['accuracy'], 'r--')
plt.plot(epochs, hist['precision'], 'r-.')
plt.plot(epochs, hist['recall'], 'r:')
plt.legend(['Val_Loss', 'Val_Accuracy', 'Val_Precision', 'Val_Recall', 'Loss', 'Accuracy', 'Precision', 'Recall'])
plt.show()



model.save('SavedModels/www_binary_classification_2')

# Make Predictions:  ---------------------------------------------------------------------------------------------------
prediction_features = test_features.copy()
prediction_labels = model.predict(prediction_features)
actual_labels = list(test['is_winner'])
for index in range(50):
    print(str(index)+": Actual: "+str(actual_labels[index])+" | Predicted: "+str(prediction_labels[index]))
# ----------------------------------------------------------------------------------------------------------------------



# Custom Predictions:

custom_attacker_ships = [
    605,    # Heron
    29984,  # Tengu
    29984,  # Tengu
    29988,  # Proteus
    29990,  # Loki
    29990,  # Loki
]
custom_victim_ships = [
    29990,  # Loki
    29988,  # Proteus
    29986,  # Legion
    29986,  # Legion
    29988,  # Proteus
    29986,  # Legion
]
custom_data = {'attacker_ship': custom_attacker_ships, 'victim_ship': custom_victim_ships}
custom_df = pd.DataFrame(custom_data)

custom_features = {
    'attacker_ship': custom_df['attacker_ship'],
    'victim_ship': custom_df['victim_ship']
}
prediction_labels_custom = model.predict(custom_features)

print(prediction_labels_custom)