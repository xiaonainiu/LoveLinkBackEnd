from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('textIn', views.textIn, name='textIn'),
    path('personInfoIn', views.personInfoIn, name='personInfoIn'),
    path('personInfoOut', views.personInfoOut, name='personInfoOut'),
    path('personId', views.personId, name='personId'),
    path('prepayId',views.prepayId, name='prepayId'),
    path('getKey',views.getKey, name='getKey'),
]