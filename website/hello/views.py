from django.shortcuts import render
from django.http import HttpResponse 

def hello(request):
    return HttpResponse('<table><tr><td>hi</td><td>there</td></table>')


# Create your views here.
