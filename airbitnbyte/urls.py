from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('property', include('property.urls')),
    path('reservation', include('reservation.urls')),
]
