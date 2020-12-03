from django.urls import path, include

from .views import LoginView, SocialLoginView, RegisterView, BookmarkView

urlpatterns = [
    path('socialLogin', SocialLoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('bookmark', BookmarkView.as_view()),

]
