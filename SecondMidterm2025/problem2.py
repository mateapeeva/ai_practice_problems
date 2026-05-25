import os


os.environ['OPENBLAS_NUM_THREADS'] = '1'
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

import warnings
warnings.filterwarnings("ignore")

#from dataset_script_anomaly import dataset
from d2 import dataset


if __name__ == '__main__':

    #INPUT
    c = int(input())
    n = int(input())
    s = int(input())

    data = []
    for row in dataset:
        new_row = [el for el in row]
        if new_row[-1] > 50:
            new_row[-1] = 1
        else:
            new_row[-1] = 0
        data.append(new_row)

    X,y = [row[:-1] for row in data], [row[-1] for row in data]

    split_index = int(len(X)*0.7)

    train_X, train_y = X[:split_index], y[:split_index]
    test_X, test_y = X[split_index:], y[split_index:]

    params = {
        'hidden_layer_sizes': 50,
        'activation': 'relu',
        'learning_rate_init': 0.001,
        'max_iter': 25,
        'random_state': 0,
    }

    classifier = MLPClassifier(**params)

    #ORIGINAL SET
    classifier.fit(train_X,train_y)
    acc_original_set = classifier.score(test_X,test_y)

    #0 - temperature, 1 - humidity, 2 - wind speed, 3 - CO2, 4 - NO2, 5 - SO2, 6 - PM2.5, 7 - PM10
    data_cns = []
    for row in data:
        new_row = [el for el in row]
        if new_row[3] > c:
            new_row[3] = c
        if new_row[4] > n:
            new_row[4] = n
        if new_row[5] > s:
            new_row[5] = s
        data_cns.append(new_row)

    X_cns,y_cns = [row[:-1] for row in data_cns], [row[-1] for row in data_cns]

    train_X_cns, train_y_cns = X_cns[:split_index], y_cns[:split_index]
    test_X_cns, test_y_cns = X_cns[split_index:], y_cns[split_index:]

    #CNS SET
    classifier.fit(train_X_cns, train_y_cns)
    acc_cns_set = classifier.score(test_X_cns, test_y_cns)

    scaler = StandardScaler()
    scaler.fit(train_X)
    train_X_scaled = scaler.transform(train_X)
    test_X_scaled = scaler.transform(test_X)

    # SCALED SET
    classifier.fit(train_X_scaled, train_y)
    acc_scaled_set = classifier.score(test_X_scaled, test_y)

    scaler.fit(train_X_cns)
    train_X_csn_scaled = scaler.transform(train_X_cns)
    test_X_csn_scaled = scaler.transform(test_X_cns)

    # CSN AND SCALED SET
    classifier.fit(train_X_csn_scaled, train_y)
    acc_cns_scaled_set = classifier.score(test_X_csn_scaled, test_y)

    print("Accuracy with:")
    print(f"The original dataset: {acc_original_set}")
    print(f"Removed anomalies: {acc_cns_set}")
    print(f"Scaled attributes: {acc_scaled_set}")
    print(f"Removed anomalies and scaled attributes: {acc_cns_scaled_set}")


