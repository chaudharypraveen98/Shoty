'''The Django Meta class is a special thing through out Django which is used to transfer information about the model or other object to the Django framework; rather than using subclassing
(which might have been another option but significantly more complex to implementing).

ModelForm is a regular Form which can automatically generate certain fields. The fields that are automatically generated depend on the content of the Meta class and on which fields have already been defined declaratively. Basically, ModelForm will only generate fields that are missing from the form, or in other words, fields that weren’t defined declaratively.
Fields defined declaratively are left as-is, therefore any customizations made to Meta attributes such as widgets, labels, help_texts, or error_messages are ignored; these only apply to fields that are generated automatically.
'''

from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        # you can use ---fields = '__all__'--- for rendering all fields
        fields = ('username', 'email', 'password')
