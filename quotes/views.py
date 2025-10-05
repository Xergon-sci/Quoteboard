from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from quotes.models import Board
from quotes.forms import QuoteForm

class BordView(TemplateView):
    template_name = "quotes/board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board = get_object_or_404(Board, code=self.kwargs["code"])
        context["board"] = board
        return context

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