'''
This is the back-end file fot the TruthGuard web app
Developed by Youssef Elebiary
'''

from flask import Flask, render_template, request, jsonify    # For the back-end
import joblib    # For loading the models and the vectorizer
import re    # For regex matching
# For preprocessing the text
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Downloading dependencies
nltk.download('stopwords')

# Creating flask app
app = Flask(__name__)

# Loading the models into a dict
# standard -> XGBoost
# lite     -> LightGBM
MODELS = {
    'standard' : joblib.load(open('./models/model.pkl', 'rb')),
    'lite' : joblib.load(open('./models/model_lite.pkl', 'rb'))
}

# Loading the vectorizer
VECTORIZER = joblib.load(open('./models/vectorizer.pkl', 'rb'))

# Creating the stemmer
portStemmer = PorterStemmer()

# Text cleaning function
def clean(text: str) -> str:
    text = text.lower()    # Converting the text to lower case
    text = re.sub(r'[^a-zA-Z\s]', '', text)    # Removing all non-alphabet characters
    return text

# Text preprocessing fucntion
def preprocess(text: str) -> str:
    text = clean(text)    # Cleaning the text
    text = text.split()    # Splitting the tex
    tokens = [portStemmer.stem(word) for word in text if word not in stopwords.words('english')]    # Removing stopwords using the stemmer
    return ' '.join(tokens)

# HTML renderer
@app.route('/')
def home():
    return render_template('index.html')

# The prediction function
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Getting the inputs from the front-end
        input_text = request.form.get('text')
        model_type = request.form.get('model')

        # Handling empty text
        if input_text == "":
            return jsonify({'error': 'Empty text'}), 400

        # Preprocessing the text
        processed = preprocess(input_text)
        # Vectorizing the text
        vectorized = VECTORIZER.transform([processed])
        # Selecting the model
        model = MODELS[model_type]

        # Handling failed model selection
        if not model:
            # Return error message to front-end
            return jsonify({'error': 'Invlaid model type'}), 400
        
        # Making the prediction
        pred = model.predict(vectorized)

        # Sending the prediction to the front-end
        return jsonify({'prediction': pred.tolist()})
    except Exception as e:
        # Returning the error to the front-end
        return jsonify({'error': str(e)}), 500
    
# Starting the flask app
if __name__ == '__main__':
    app.run()