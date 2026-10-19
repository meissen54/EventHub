from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
       path(
        "manage/events/create/",
        views.create_event,
        name="create_event"
    ),
]