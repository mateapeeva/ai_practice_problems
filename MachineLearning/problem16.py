import os


os.environ['OPENBLAS_NUM_THREADS'] = '1'

from dataset_script import dataset
from sklearn.tree import DecisionTreeClassifier


if __name__ == '__main__':
    p = int(input())
    criterion = input()
    l = int(input())
    split_index = int(len(dataset)*p/100)

    X,y = [row[:-1] for row in dataset],[row[-1] for row in dataset]

    train_X,train_y = X[:split_index],y[:split_index]
    test_X,test_y = X[split_index:],y[split_index:]

    params ={
        'criterion':criterion,
        'max_leaf_nodes':l,
        'random_state':0,
    }
    classifier_1 = DecisionTreeClassifier(**params)
    classifier_1.fit(train_X,train_y)

    acc_1 = classifier_1.score(test_X,test_y)

    params ={
        'criterion': criterion,
        'max_leaf_nodes': l,
        'random_state': 0,
    }

    y_perch,y_roach,y_bream = [],[],[]
    for el in y:
        if el == 'Perch':
            y_perch.append(1)
            y_roach.append(0)
            y_bream.append(0)
        elif el == 'Roach':
            y_perch.append(0)
            y_roach.append(1)
            y_bream.append(0)
        else:
            y_perch.append(0)
            y_roach.append(0)
            y_bream.append(1)

    train_y_perch, train_y_roach, train_y_bream = y_perch[:split_index], y_roach[:split_index], y_bream[:split_index]
    test_y_perch, test_y_roach, test_y_bream = y_perch[split_index:], y_roach[split_index:], y_bream[split_index:]

    classifier_perch = DecisionTreeClassifier(**params)
    classifier_perch.fit(train_X,train_y_perch)

    classifier_roach = DecisionTreeClassifier(**params)
    classifier_roach.fit(train_X, train_y_roach)

    classifier_bream = DecisionTreeClassifier(**params)
    classifier_bream.fit(train_X, train_y_bream)

    pred_perch, pred_roach, pred_bream = classifier_perch.predict(test_X), classifier_roach.predict(test_X), classifier_bream.predict(test_X)

    tr_pred = 0
    for pr_p,pr_r,pr_b,tr_p,tr_r,tr_b in zip(pred_perch,pred_roach,pred_bream,test_y_perch,test_y_roach,test_y_bream):
        if pr_p == tr_p and pr_r == tr_r and pr_b == tr_b:
            tr_pred += 1

    acc_2 = tr_pred/len(test_X)

    print(f"Tochnost so originalniot klasifikator: {acc_1}")
    print(f"Tochnost so kolekcija od klasifikatori: {acc_2}")
