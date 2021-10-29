from django.shortcuts import render
from django.http import HttpResponse 
from msgserver.models import Message

def message(request):
    return HttpResponse("Hello World this is MESSAGE!!")


def get_message(request, key):
    mess = Message.objects.filter(key = key)
    if (len(mess) > 0):
        #return HttpResponse(mess )
        return HttpResponse("Key is  %(key)s and message is %(message)s " %{'key':mess[0].key, 'message':mess[0].message})
        # %{'message':mess.message, 'key':mess.key})
    else:
        return HttpResponse("No such message " + str(id))

# Create your views here.