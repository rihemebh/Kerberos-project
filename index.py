from flask import Flask, render_template, request, Response
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
from flask_bootstrap import Bootstrap
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd



DEBUG=True

app = Flask(__name__)
Bootstrap(app)


@app.route('/predict')
@requires_authentication
def predict():
    irisData = datasets.load_iris()
    data, target = irisData.data, irisData.target
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

    n = np.array(testdata)
    ind = np.argsort(n[:, 4])
    n = n[ind]
    frame = pd.DataFrame(n,
                columns=["sepal length in cm", "sepal width in cm", "petal length in cm",
                                      "petal width in cm",
                                      "predicted type"])

    return render_template('view.html',tables=[frame.to_html(classes='data')])

if __name__ == '__main__':
        init_kerberos(app,service='host',hostname='server.insat.tn')
        app.run(host='0.0.0.0',port=8080)
