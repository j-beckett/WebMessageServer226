from django.urls import path 
from . import views 

urlpatterns = [
        path('', views.message, name='mess'),
        path('get/<int:key>/', views.get_message, name='messag'),

        ]
