from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load model, vectorizer, and label encoder
with open('models.pkl', 'rb') as f:
    model_data = pickle.load(f)

model = model_data['model']
vectorizer = model_data['vectorizer']
label_encoder = model_data['label_encoder']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    resume_text = request.form.get('resume_text')

    if not resume_text:
        return "Please enter some resume text!", 400

    try:
        # Preprocess and predict
        X_input = vectorizer.transform([resume_text])
        prediction = model.predict(X_input)[0]
        predicted_label = label_encoder.inverse_transform([prediction])[0]

        return render_template('result.html', prediction=predicted_label)

    except Exception as e:
        return f"Error during prediction: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)



