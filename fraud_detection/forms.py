from django import forms

class FraudDetectionForm(forms.Form):
    step = forms.FloatField(label='Step')
    amount = forms.FloatField(label='Amount')
    oldbalanceOrg = forms.FloatField(label='Old Balance Origin')
    newbalanceOrig = forms.FloatField(label='New Balance Origin')
    oldbalanceDest = forms.FloatField(label='Old Balance Destination')
    newbalanceDest = forms.FloatField(label='New Balance Destination')
    type = forms.ChoiceField(
    choices=[
        ('CASH_OUT', 'Cash Out'),
        ('DEBIT', 'Debit'),
        ('PAYMENT', 'Payment'),
        ('TRANSFER', 'Transfer'),
        ('CASH_IN', 'Cash In'),
    ],
    label='Transaction Type'
) 