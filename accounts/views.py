from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Create your views here.


def register(request):
    return HttpResponse("Hello")


