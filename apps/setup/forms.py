# forms.py
from django import forms

class FormA(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField()

class FormB(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.TextInput()
