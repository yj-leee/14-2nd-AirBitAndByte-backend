
from django.urls import path, include

urlpatterns = [
    path('property', include('property.urls')),
    path('user', include('user.urls'))
]
