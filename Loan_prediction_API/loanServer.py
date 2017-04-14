from flask import Flask, request, jsonify
from sklearn.externals import joblib
import numpy as np

app = Flask(__name__)

def predict():
    model = joblib.load('xgboost.pkl')
    test = np.array([[-0.45600094, 0.00580783, 0.0341337, 0. , 1. , 0. , 0. , 0. , 1. , 0.,0.]])
    pred = model.predict_proba(test)
    return pred[0]

data = predict().tolist()

@app.route("/")
def hello():
    return jsonify(result=data)

if __name__ == "__main__":
    app.run(debug=True)