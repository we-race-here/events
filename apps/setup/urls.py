# urls.py
from django.urls import path
from .views import DynamicFormView

urlpatterns = [
    path('form/', DynamicFormView.as_view(), name='dynamic_form'),
]
