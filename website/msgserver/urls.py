from django.urls import path 
from . import views 


#our current list of pages that exist under the directory of msgserver. 
urlpatterns = [
        path('', views.show_all_messages, name='allmessages'),
        path('get/<slug:key>/', views.get_message, name='get'),
        path('create/', views.MessageCreate.as_view(), name='message_create'),
        path('update/<slug:pk>', views.MessageUpdate.as_view(),name='message_update')
        ]
