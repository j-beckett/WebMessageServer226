from django.shortcuts import render
from django.http import HttpResponse 
from msgserver.models import Message
from django.core import serializers
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView


#allows a user to create a new message. Validation checked in 'models' class.
class MessageCreate(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('allmessages')

#allows a user to update a message. Validation checked in 'models' class.
class MessageUpdate(UpdateView):
    model = Message
    fields = ['message']
    success_url = reverse_lazy('allmessages')

#this function returns all current message/key pairs in a JSON format and displays them to the /msgserver page.
#after a new message is created, or an existing message is updated, users are also redirected to this page.     
def show_all_messages(request):
    mess = Message.objects.all()
    toReturn = serializers.serialize("json", mess)
    return HttpResponse(toReturn)

#this function gets the specific message associated with the key
#the user writes the key in the url of message Server
#if no message, return the key that was entered
def get_message(request, key):
    mess = Message.objects.filter(key = key)
    if (len(mess) == 1):                     
        return HttpResponse("%(key)s:%(message)s " %{'key':mess[0].key, 'message':mess[0].message})
    else:
        return HttpResponse("No message at key" + str(key))


