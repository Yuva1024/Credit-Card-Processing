from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load and prepare the model pipeline again (as Flask apps restart per session)
df = pd.read_csv(r"D:\aiml intern\task1\clean_dataset.csv")

X = df.drop('Approved', axis=1)
y = df['Approved']

num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
cat_cols = X.select_dtypes(include=['object']).columns.tolist()

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
])

model = RandomForestClassifier(n_estimators=100, random_state=42)
pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('classifier', model)
])

pipeline.fit(X, y)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input values from form
    input_data = {col: request.form[col] for col in request.form}
    input_df = pd.DataFrame([input_data])

    # Convert numeric fields from string to proper types
    for col in num_cols:
        input_df[col] = pd.to_numeric(input_df[col])

    # Predict
    prediction = pipeline.predict(input_df)[0]
    result = 'Approved' if prediction == 1 else 'Rejected'

    return render_template('form.html', prediction_text=f'Credit Application: {result}')

if __name__ == '__main__':
    app.run(debug=True)
