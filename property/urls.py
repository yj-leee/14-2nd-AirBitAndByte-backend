from django.urls import path
from property.views import PropertiesView, PropertyDetailView

urlpatterns = [
    path('', PropertiesView.as_view()),
    path('/<int:property_id>', PropertyDetailView.as_view())
]
