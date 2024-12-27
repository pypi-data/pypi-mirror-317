from django.urls import path

from . import views

urlpatterns = [
    path("switch-user/", views.switch_user, name="switch-user"),
]
