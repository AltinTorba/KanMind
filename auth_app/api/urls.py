from django.urls import path
from .views import RegisterView, LoginView, EmailCheckView

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("email-check/", EmailCheckView.as_view())
]