from django.shortcuts import render
import joblib
import numpy as np
from .forms import FraudDetectionForm
import os
from datetime import datetime

# Load model and scaler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'trained_model', 'rf_model.pkl')
scaler_path = os.path.join(BASE_DIR, 'trained_model', 'scaler.pkl')

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# In-memory history for demo
history_list = []

def predict_view(request):
    prediction = None
    confidence = None

    if request.method == 'POST':
        form = FraudDetectionForm(request.POST)
        print("✅ Form Submitted")
        if form.is_valid():
            print("✅ Form is valid")
            
            # Extract values
            step = form.cleaned_data['step']
            amount = form.cleaned_data['amount']
            oldbalanceOrg = form.cleaned_data['oldbalanceOrg']
            newbalanceOrig = form.cleaned_data['newbalanceOrig']
            oldbalanceDest = form.cleaned_data['oldbalanceDest']
            newbalanceDest = form.cleaned_data['newbalanceDest']
            selected_type = form.cleaned_data['type']

            # One-hot encode type
            type_mapping = ['CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER', 'CASH_IN']
            type_encoded = [1 if selected_type == t else 0 for t in type_mapping]

            # Final input vector
            data = [step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest] + type_encoded
            print("📦 Data:", data)

            X = np.array(data).reshape(1, -1)
            X_scaled = scaler.transform(X)

            # Prediction and probability
            result = model.predict(X_scaled)[0]
            proba = model.predict_proba(X_scaled)[0][1]  # Probability for class '1' (Fraud)

            prediction = "Fraud" if result == 1 else "Not Fraud"
            confidence = proba * 100

            # Save to in-memory history
            history_list.append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'amount': amount,
                'type': selected_type,
                'prediction': result,
                'confidence': f"{confidence:.2f}"
            })

        else:
            print("❌ Form is not valid")
            print(form.errors)
    else:
        form = FraudDetectionForm()

    return render(request, 'predict.html', {
        'form': form,
        'prediction': prediction,
        'confidence': confidence,
        'history': history_list[::-1]
    }) 