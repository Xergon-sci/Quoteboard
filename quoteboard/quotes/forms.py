from django import forms 
from quotes.models import Quote

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "author"]

class PinForm(forms.Form):
    a = forms.CharField(max_length=1, widget=forms.PasswordInput(attrs={
        'inputmode': 'numeric',
        'pattern': '[0-9]*',
        'maxlength': '1',
        'class': 'pin-input form-control text-center',
        'style': 'width:3rem; display:inline-block; margin:0 0.25rem;',
    }))
    b = forms.CharField(max_length=1, widget=forms.PasswordInput(attrs={
        'inputmode': 'numeric',
        'pattern': '[0-9]*',
        'maxlength': '1',
        'class': 'pin-input form-control text-center',
        'style': 'width:3rem; display:inline-block; margin:0 0.25rem;',
    }))
    c = forms.CharField(max_length=1, widget=forms.PasswordInput(attrs={
        'inputmode': 'numeric',
        'pattern': '[0-9]*',
        'maxlength': '1',
        'class': 'pin-input form-control text-center',
        'style': 'width:3rem; display:inline-block; margin:0 0.25rem;',
    }))
    d = forms.CharField(max_length=1, widget=forms.PasswordInput(attrs={
        'inputmode': 'numeric',
        'pattern': '[0-9]*',
        'maxlength': '1',
        'class': 'pin-input form-control text-center',
        'style': 'width:3rem; display:inline-block; margin:0 0.25rem;',
    }))