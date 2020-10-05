from contacts.models import Contact
from django import forms


class FormContato(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('enabled',)
