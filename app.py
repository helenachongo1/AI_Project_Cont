from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

#Data collection
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
df.head()

#Preprocessing
X = df.drop('target', axis=1)
y = df['target']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

#Model training
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model and scaler
joblib.dump(model, 'iris_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

#Flask API Deployment
app = Flask(__name__)

model = joblib.load('iris_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/')
def home():
    return "Iris Classifier API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)
    return jsonify({'class': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)