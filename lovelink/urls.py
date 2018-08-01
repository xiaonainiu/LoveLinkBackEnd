from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('textIn', views.textIn, name='textIn'),
    path('postRequest', views.postRequest, name='postRequest'),
]