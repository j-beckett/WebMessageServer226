from django.shortcuts import render
from django.http import HttpResponse 
from msgserver.models import Message
from django.core import serializers
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView



class MessageCreate(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('allmessages')

class MessageUpdate(UpdateView):
    model = Message
    fields = ['key', 'message']
    success_url = reverse_lazy('allmessages')
     
def message(request):
    mess = Message.objects.all()
    toReturn = serializers.serialize("json", mess)
    return HttpResponse(toReturn)

def get_message(request, key):
    mess = Message.objects.filter(key = key)
    if (len(mess) == 1):                     
        #return HttpResponse(mess )
        return HttpResponse("Key is  %(key)s and message is %(message)s " %{'key':mess[0].key, 'message':mess[0].message})
        # %{'message':mess.message, 'key':mess.key})
    else:
        return HttpResponse("No such message " + str(id))

def create_message(request):
    return HttpResponse("hey")


