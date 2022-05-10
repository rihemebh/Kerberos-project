from sklearn import datasets
from sklearn.model_selection import train_test_split, cross_val_score, ShuffleSplit
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd


irisData = datasets.load_iris()

data, target = irisData.data, irisData.target


def Knnpredict(data, target):

    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=123)
    classifierknn = KNeighborsClassifier(n_neighbors=6)
    classifierknn.fit(X_train, y_train)
    result = classifierknn.predict(X_test)

    k = 0
    testdata = X_test.tolist()
    res = result.tolist()

    for c in res:
        if c == 0:
            res[k] = "setosa"
        elif c == 1:
            res[k] = "versicolor"
        elif c == 2:
            res[k] = "virginica"
        k += 1

    i = 0
    for array in testdata:
        array.append(res[i])
        i += 1

    score = classifierknn.score(X_test, y_test)

    n = np.array(testdata)
    ind = np.argsort(n[:, 4])
    n = n[ind]
    frame = pd.DataFrame(n,
                     columns=["sepal length in cm", "sepal width in cm", "petal length in cm", "petal width in cm",
                              "predicted type"])
    print(f"The prediction is made with accuracy = {score} \n {frame}")
