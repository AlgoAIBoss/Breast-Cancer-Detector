from django import forms
from django.forms import ModelForm, fields
from .models import BreastCancerChecker


class BreastCheckerForm(ModelForm):
    class Meta:
        model = BreastCancerChecker
        fields = '__all__'
