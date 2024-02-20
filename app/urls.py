from django.urls import path
from . import views


urlpatterns = [
    path('<str:url_path>', views.index_path),
    path('', views.index),
]
