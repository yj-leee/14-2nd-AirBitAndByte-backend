from django.urls     import path

from .views          import MainListView

urlpatterns= [
    path('', MainListView.as_view()),
]
