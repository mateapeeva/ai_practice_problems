import os

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

os.environ['OPENBLAS_NUM_THREADS'] = '1'

#from dataset_script import dataset
from d3 import dataset
from sklearn.ensemble import RandomForestClassifier


if __name__ == '__main__':

    #INPUT
    n = int(input())
    m = int(input())

    X,y = [row[:-1] for row in dataset], [row[-1] for row in dataset]

    split_index_1 = int(len(X)*(1/3))
    split_index_2 = int(len(X)*(2/3))

    p1_X, p1_y = X[:split_index_1], y[:split_index_1]
    p2_X, p2_y = X[split_index_1:split_index_2], y[split_index_1:split_index_2]
    p3_X, p3_y = X[split_index_2:], y[split_index_2:]

    # FOREST CLASSIFIER

    params = {
        'n_estimators': n,
        'criterion': 'gini',
        'random_state':0,
    }

    classifier_forest = RandomForestClassifier(**params)

    # NAIVE BAYES AND DECISION TREE

    classifier_1_nb = GaussianNB()
    params = {
        'max_depth': m,
        'criterion': 'gini',
        'random_state': 0,
    }
    classifier_2_dt = DecisionTreeClassifier(**params)

    # SETS
    test_X_1, test_y_1 = p1_X, p1_y
    train_X_1, train_y_1 = p2_X+p3_X, p2_y+p3_y

    test_X_2, test_y_2 = p2_X, p2_y
    train_X_2, train_y_2 = p1_X + p3_X, p1_y + p3_y

    test_X_3, test_y_3 = p3_X, p3_y
    train_X_3, train_y_3 = p1_X + p2_X, p1_y + p2_y

    # ACCURACY FOREST
    acc_avg_forest = 0

    classifier_forest.fit(train_X_1,train_y_1)
    acc_avg_forest += classifier_forest.score(test_X_1,test_y_1)

    classifier_forest.fit(train_X_2, train_y_2)
    acc_avg_forest += classifier_forest.score(test_X_2, test_y_2)

    classifier_forest.fit(train_X_3, train_y_3)
    acc_avg_forest += classifier_forest.score(test_X_3, test_y_3)

    acc_avg_forest /= 3
    print(f"Accuracy with random forest: {acc_avg_forest}")

    # ACCURACY NB AND DT
    acc_avg_nb_dt = 0

    classifier_1_nb.fit(train_X_1,train_y_1)
    classifier_2_dt.fit(train_X_1,train_y_1)

    pred_nb = classifier_1_nb.predict(test_X_1)
    pred_dt = classifier_2_dt.predict(test_X_1)
    predict_proba_nb = classifier_1_nb.predict_proba(test_X_1)
    predict_proba_dt = classifier_2_dt.predict_proba(test_X_1)

    tr_pr = 0

    for i in range(len(test_y_1)):
        pr1 = pred_nb[i]
        pr2 = pred_dt[i]
        tr = test_y_1[i]
        proba1 = max(predict_proba_nb[i])
        proba2 = max(predict_proba_dt[i])
        if pr1 == pr2 and pr1 == tr:
            tr_pr += 1
        elif pr1 == tr and proba1 > proba2:
            tr_pr += 1
        elif pr2 == tr and proba2 > proba1:
            tr_pr += 1

    acc = tr_pr/len(test_X_1)
    acc_avg_nb_dt += acc

    classifier_1_nb.fit(train_X_2, train_y_2)
    classifier_2_dt.fit(train_X_2, train_y_2)

    pred_nb = classifier_1_nb.predict(test_X_2)
    pred_dt = classifier_2_dt.predict(test_X_2)
    predict_proba_nb = classifier_1_nb.predict_proba(test_X_2)
    predict_proba_dt = classifier_2_dt.predict_proba(test_X_2)

    tr_pr = 0
    for i in range(len(test_y_2)):
        pr1 = pred_nb[i]
        pr2 = pred_dt[i]
        tr = test_y_2[i]
        proba1 = max(predict_proba_nb[i])
        proba2 = max(predict_proba_dt[i])
        if pr1 == pr2 and pr1 == tr:
            tr_pr += 1
        elif pr1 == tr and proba1 > proba2:
            tr_pr += 1
        elif pr2 == tr and proba2 > proba1:
            tr_pr += 1

    acc = tr_pr / len(test_X_2)
    acc_avg_nb_dt += acc

    classifier_1_nb.fit(train_X_3, train_y_3)
    classifier_2_dt.fit(train_X_3, train_y_3)

    pred_nb = classifier_1_nb.predict(test_X_3)
    pred_dt = classifier_2_dt.predict(test_X_3)
    predict_proba_nb = classifier_1_nb.predict_proba(test_X_3)
    predict_proba_dt = classifier_2_dt.predict_proba(test_X_3)

    tr_pr = 0
    for i in range(len(test_y_3)):
        pr1 = pred_nb[i]
        pr2 = pred_dt[i]
        tr = test_y_3[i]
        proba1 = max(predict_proba_nb[i])
        proba2 = max(predict_proba_dt[i])
        if pr1 == pr2 and pr1 == tr:
            tr_pr += 1
        elif pr1 == tr and proba1 > proba2:
            tr_pr += 1
        elif pr2 == tr and proba2 > proba1:
            tr_pr += 1

    acc = tr_pr / len(test_X_3)
    acc_avg_nb_dt += acc

    acc_avg_nb_dt /= 3
    print(f"Accuracy with naive bayes and decision tree: {acc_avg_nb_dt}")

