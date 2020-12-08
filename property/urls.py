from django.urls import path
from property.views import PropertiesView

urlpatterns = [
    path('', PropertiesView.as_view()),
]
