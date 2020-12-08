from django.urls import path

from .views      import PropertyListView, PropertyDetailView

urlpatterns = [
    path('', PropertyListView.as_view()),
    path('/<int:property_id>', PropertyDetailView.as_view()),
]
