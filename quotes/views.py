from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from quotes.models import Board

class BordView(TemplateView):
    template_name = "quotes/board.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        board = get_object_or_404(Board, code=self.kwargs["code"])
        context["board"] = board
        return context