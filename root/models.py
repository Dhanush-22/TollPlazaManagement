from django.db import models
import datetime
from django.contrib.auth.models import User
from django import forms

date = datetime.date.today()

# Create your models here.

class Vehicle(models.Model):
    owner_name = models.CharField(max_length=50)
    veh_no = models.CharField(max_length=50)
    balance = models.IntegerField(default=0)
    def __str__(self):
        return self.owner_name
        

class LicenseHolder(models.Model):
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_num = models.CharField(max_length=20)
    License_num = models.CharField(max_length=20) 
    Vehicle_Number = models.CharField(max_length=10)
    Vehicle_Name = models.CharField(max_length=20)
    validity = models.DateField( default=date)
    def __str__(self):
        return self.First_Name + " " + self.Last_Name


class User_Extra(models.Model):
    First_Name = models.CharField(max_length=100,default="")
    Last_Name = models.CharField(max_length=100,default="")
    License_num = models.CharField(max_length=20, default="") 
    License_img = models.ImageField(upload_to='', default="tempo.png")  # -- added 13/04/22
    Vehicle_Number = models.CharField(max_length=10, default="")
    Vehicle_Name = models.CharField(max_length=20, default="")
    is_verified = models.IntegerField(default=0)

    def __str__(self):
        return self.First_Name + " " + self.Last_Name
