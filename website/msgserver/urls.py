from django.urls import path 
from . import views 

urlpatterns = [
        path('', views.message, name='allmessages'),
        path('get/<int:key>/', views.get_message, name='get'),
        path('create/', views.MessageCreate.as_view(), name='message_create'),
        path('update/<int:pk>', views.MessageUpdate.as_view(),name='message_update')
        ]
