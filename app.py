from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Load the machine learning model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the request
    data = request.json

    # Preprocess the input data if needed
    # ...

    # Make predictions using the loaded model
    predictions = model.predict(data)

    # Return the predictions as JSON response
    return jsonify(predictions.tolist())

@app.route('/scatter', methods=['GET'])
def scatter():
    return render_template('scatter.html')

if __name__ == '__main__':
    app.run()
