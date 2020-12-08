from django.urls import path

from .views      import ReservationView, PaymentView

urlpatterns = [
    path('', ReservationView.as_view()),
    path('/<int:reservation_id>', PaymentView.as_view()),
]
