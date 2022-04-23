from django.urls import path, include
from django.conf import settings #add this
from django.conf.urls.static import static #add this
from . import views



urlpatterns = [
    path('register',views.register,name='register'),
] 
