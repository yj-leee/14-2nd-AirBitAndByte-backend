from django.urls import path, include

from .views import LogInView, SocialLoginView, SignUpView, BookmarkView

urlpatterns = [
    path('socialLogin', SocialLoginView.as_view()),
    path('signup', SignUpView.as_view()),
    path('login', LogInView.as_view()),
    path('bookmark', BookmarkView.as_view()),

]
