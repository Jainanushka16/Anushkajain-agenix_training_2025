from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Load trained model
model = joblib.load("random_forest_model.pkl")

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Customer Churn API is up and running!"})

@app.route('/predict', methods=['GET'])
def predict():
    try:
        recency = int(request.args.get('recency'))
        frequency = int(request.args.get('frequency'))
        monetary = float(request.args.get('monetary'))

        input_data = pd.DataFrame([[recency, frequency, monetary]], columns=["Recency", "Frequency", "Monetary"])
        prediction = model.predict(input_data)[0]

        return jsonify({
            "recency": recency,
            "frequency": frequency,
            "monetary": monetary,
            "churn_prediction": int(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True)
