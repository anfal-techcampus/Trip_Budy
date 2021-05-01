from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("register",views.register),
    path("login",views.login),
    path("dashboard",views.dashboard),
    path("trips/new",views.new),
    path("trips/create",views.create),
    path("cancel",views.cancel),
    path("trips/edit/<int:id>",views.edit),
    path("trips/update/<int:id>",views.update),
    path("trips/remove/<int:id>",views.remove),
    path("trips/<int:id>",views.view),
    path("trips/join/<int:id>",views.join),
    path("trips/notjoin/<int:id>",views.notjoin),
    path("logout",views.logout)
]