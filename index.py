from flask import Flask, render_template, request, Response
from flask_kerberos import init_kerberos
from flask_kerberos import requires_authentication
from flask_bootstrap import Bootstrap
from sklearn import datasets

import predict
import os

DEBUG=True

app = Flask(__name__)
Bootstrap(app)


@app.route('/predict')
@requires_authentication
def predict():
    irisData = datasets.load_iris()
    data, target = irisData.data, irisData.target
    predict(data, target)


@app.route('/open/predict')
def predict():
    irisData = datasets.load_iris()
    data, target = irisData.data, irisData.target
    predict(data, target)
