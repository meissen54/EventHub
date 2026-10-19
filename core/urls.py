
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("accounts/signup/", views.signup_view, name="signup"),
    path("events/", views.events, name="events"),
    path("event-detail/", views.event_detail, name="event_detail"),
]
