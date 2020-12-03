from django.urls import path

from .views      import ReservationCreateView

urlpatterns = [
    path('', ReservationCreateView.as_view()),
]
