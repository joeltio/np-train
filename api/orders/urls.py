from django.urls import path

from . import views

urlpatterns = [
    path("uncompleted/", views.uncompleted_order),
    path("new/", views.new_order),
]
