from django.urls import path

from .views import login, signup, logout


app_name = "users"


urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("signup/", signup, name="signup"),
    
]