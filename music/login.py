'''
It is a django form class with some validation in the views.py such cleaned text and much more.
'''
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
