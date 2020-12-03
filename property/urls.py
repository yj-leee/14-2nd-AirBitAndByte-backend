from django.urls import path

from .views      import PropertySearchView, PropertyListView, PropertyDetailView

urlpatterns = [
    path('', PropertySearchView.as_view()),
    path('/s', PropertyListView.as_view()),
    path('/<int:property_id>', PropertyDetailView.as_view()),
]
