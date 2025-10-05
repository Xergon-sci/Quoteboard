from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("board/<str:code>/", views.BordView.as_view(), name="board_view"),
    path("board/<str:code>/add-quote", views.AddQuoteView.as_view(), name="add-quote")
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
