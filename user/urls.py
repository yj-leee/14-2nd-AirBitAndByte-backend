from django.urls     import path

from .views          import BookMarkView

urlpatterns= [
    path('/bookmark', BookMarkView.as_view()),
    path('/bookmark/<int:bookmark_id>', BookMarkView.as_view()),
]
