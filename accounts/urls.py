from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    ResendOTPView,
    LoginView,
    GoogleAuthInitView,
    GoogleAuthCallbackView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("resend-otp/", ResendOTPView.as_view()),
    path("login/", LoginView.as_view()),
    path("google/", GoogleAuthInitView.as_view()),
    path("google/callback/", GoogleAuthCallbackView.as_view()),
]