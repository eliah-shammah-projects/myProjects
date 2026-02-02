from flask import Flask, render_template, request
from flask_cors import CORS
from predict import predict_verse

app = Flask(__name__)
CORS(app)  # Allow CORS for React front-end

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    verse = request.form['verse']
    result = predict_verse(verse)
    return render_template('index.html', result=result)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    verse = data.get('verse', '')
    result = predict_verse(verse)
    return result

if __name__ == '__main__':
    app.run(debug=True)