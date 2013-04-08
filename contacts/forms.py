from django import forms
from django.forms import ModelForm

from contacts.models import *

class UploadFileForm(forms.Form):
    docfile = forms.FileField(
        label = 'Select a file',
        help_text = 'csv only',
        )

class ContactsForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('account_id',)
        
    def set_account(self, account):
        self.instance.account_id = account
