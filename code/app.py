from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('iris_model.pkl')

@app.route('/')
def index():
    """
    Serve the HTML file for the front-end interface.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle the API request to predict the Iris species.
    """
    try:
        # Parse the JSON request data
        data = request.get_json()
        sepal_length = data['sepal_length']
        sepal_width = data['sepal_width']
        petal_length = data['petal_length']
        petal_width = data['petal_width']

        # Prepare the input array for prediction
        input_features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        
        # Make the prediction
        prediction = model.predict(input_features)
        species = ['setosa', 'versicolor', 'virginica'][prediction[0]]

        # Return the prediction as JSON
        return jsonify({'species': species})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
