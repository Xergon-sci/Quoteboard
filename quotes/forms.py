from django.forms import ModelForm
from quotes.models import Quote

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ["text", "author"]