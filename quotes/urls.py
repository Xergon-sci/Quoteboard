from django.urls import path

from . import views

urlpatterns = [
    path("board/<str:code>/", views.BordView.as_view(), name="board_view"),
    ]