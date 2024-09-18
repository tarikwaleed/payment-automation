from django.urls import path, include
from .views import SimpleView

urlpatterns = [
    path("", view=SimpleView.as_view()),
]