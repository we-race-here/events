"""
This is file will have custom widgets
"""

from django import forms

class DateInput(forms.TextInput):
    template_name = 'custom_widgets/custom_date_input.html'
