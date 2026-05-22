import os

os.environ['OPENBLAS_NUM_THREADS'] = '1'
from dataset_script import dataset
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import MinMaxScaler


if __name__ == '__main__':

    dataset_0 = [row for row in dataset if row[-1] == 'good']
    dataset_1 = [row for row in dataset if row[-1] == 'bad']

    X_0,y_0 = [row[:-1] for row in dataset_0],[row[-1] for row in dataset_0]
    for row in X_0:
        row[0] += row[10]
    X_0 = [[el for i,el in enumerate(row) if i!=10] for row in X_0]

    X_1, y_1 = [row[:-1] for row in dataset_1], [row[-1] for row in dataset_1]
    for row in X_1:
        row[0] += row[10]
    X_1 = [[el for i, el in enumerate(row) if i != 10] for row in X_1]

    c = int(input())
    p = int(input())

    if c == 0:
        split_index_0 = int(len(X_0)*p/100)
        split_index_1 = int(len(X_1)*p/100)
        train_X = X_0[:split_index_0] + X_1[:split_index_1]
        train_y = y_0[:split_index_0] + y_1[:split_index_1]
        test_X = X_0[split_index_0:] + X_1[split_index_1:]
        test_y = y_0[split_index_0:] + y_1[split_index_1:]
    else:
        split_index_0 = int(len(X_0)*(100-p)/100)
        split_index_1 = int(len(X_1) * (100 - p) / 100)
        train_X = X_0[split_index_0:] + X_1[split_index_1:]
        train_y = y_0[split_index_0:] + y_1[split_index_1:]
        test_X = X_0[:split_index_0] + X_1[:split_index_1]
        test_y = y_0[:split_index_0] + y_1[:split_index_1]

    classifier = GaussianNB()

    classifier.fit(train_X,train_y)
    acc_1 = classifier.score(test_X,test_y)

    scalar = MinMaxScaler(feature_range=(-1,1))
    train_X = scalar.fit_transform(train_X)
    test_X = scalar.transform(test_X)

    classifier.fit(train_X,train_y)
    acc_2 = classifier.score(test_X,test_y)

    print(f"Tochnost so zbir na koloni: {acc_1}")
    print(f"Tochnost so zbir na koloni i skaliranje: {acc_2}")


