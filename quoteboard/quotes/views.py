from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db.models.functions import Random
from quotes.models import Board
from quotes.forms import QuoteForm, PinForm
import random

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

        latest_quotes = board.quotes.all().order_by('-date')[:10]
        exclude_ids = [q.id for q in latest_quotes]
        random_quotes = list(board.quotes.exclude(id__in=exclude_ids).order_by(Random())[:40])

        quotes = list(latest_quotes) + list(random_quotes)
        random.shuffle(quotes)

        FONTS = [
            "Barrio",
            "Bitter",
            "Borel",
            "Caveat",
            "Coming Soon",
            "Damion",
            "Delicious Handrawn",
            "Fontdiner Swanky",
            "Gluten",
            "Google Sans Code",
            "Homemade Apple",
            "Knewave",
            "Leckerli One",
            "Lily Script One",
            "Montserrat",
            "Mynerve",
            "Oldenburg",
            "Open Sans",
            "Pacifico",
            "Playwrite US Modern",
            "Playwrite US Trad",
            "Shadows Into Light Two",
            "The Girl Next Door",
            "Tilt Prism",
            "Workbench",
            "Yellowtail",
        ]

        for q in quotes:
            q.font = random.choice(FONTS)

        col1 = quotes[0::3]
        col2 = quotes[1::3]
        col3 = quotes[2::3]

        return render(request, "quotes/partials/quoteList.html", {"board":  board, "col1": col1, "col2": col2, "col3": col3})