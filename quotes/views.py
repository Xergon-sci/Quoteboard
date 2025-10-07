from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from quotes.models import Board
from quotes.forms import QuoteForm, PinForm
import json

class BordView(TemplateView):
    template_name = "quotes/board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board = get_object_or_404(Board, code=self.kwargs["code"])
        context["board"] = board
        return context

class PinCheckView(View):
    def get(self, request, code):
        board = get_object_or_404(Board, code=code)

        if request.session.get(f"board_{board.code}_access"):
            return HttpResponse(status=204, headers={"HX-Trigger": "quoteListChanged"})
        
        form = PinForm()
        return render(request, "quotes/partials/pinModal.html", {"board": board, "form": form})
    
    def post(self, request, code):
        board = get_object_or_404(Board, code=code)
        form = PinForm(request.POST)

        if form.is_valid():
            pin = f"{form.cleaned_data['a']}{form.cleaned_data['b']}{form.cleaned_data['c']}{form.cleaned_data['d']}"
            if int(pin) == board.pin:
                request.session[f"board_{board.code}_access"] = True
                return HttpResponse(request, status=204, headers={"HX-Trigger": "pinCorrect"})
            else:
                form.add_error(None, "Incorrect PIN. Please try again.")
        
        return render(request, "quotes/partials/pinModal.html", {"board": board, "form": form})

class AddQuoteView(View):

    def post(self, request, **kwargs):
        addQuoteForm = QuoteForm(request.POST)

        if addQuoteForm.is_valid():
            addQuoteForm.instance.board = get_object_or_404(Board, code=self.kwargs["code"])
            addQuoteForm.save()
            return HttpResponse(status=204, headers={"HX-Trigger": "quoteListChanged"})
        else:
            return render(request, "quotes/partials/addQuoteModal.html", {"form": addQuoteForm})
    
    def get(self, request, **kwargs):
        return render(request, "quotes/partials/addQuoteModal.html", {"form": QuoteForm()})

class LoadQuotesView(View):

    def get(self, request, **kwargs):
        board = get_object_or_404(Board, code=self.kwargs["code"])
        return render(request, "quotes/partials/quoteList.html", {"board": board})