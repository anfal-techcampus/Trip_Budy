from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def validator(self,postData):
        errors={}
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name']='First name should be at lesat 2 charictors'
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name']='First name should only be letters'
        if len(postData['last_name'])<2:
            errors['last_name']='Last name should be at lesat 2 charictors'   
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name']='Last name should only be letters'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = "Invalid email address!"

        if len(postData['password'])<8:
            errors['password']='Password should be at lesat 8 charictors'
        elif postData['password'] != postData['confirm_pw']:
                errors['password'] = 'Confirm PW does not match the password!'

        user=User.objects.filter(email=postData['email'])
        if user:
            errors['email']='Email is already exist'
        return errors

class TripManager(models.Manager):
    def validator(self,postData):
        errors={} 
        today=datetime.today().date()
        if len(postData['destination'])<1:
            errors['destination']='Destination must be provided'    
        elif len(postData['destination'])<3:
            errors['destination']='A trip destination must consist of 3 characters' 
        if postData['start_date'] < str(today):
            errors['start_date']='Start date must be in future'
        if postData['end_date'] < postData['start_date']:
            errors['end_date']='End date must be after start date'          
        if len(postData['plan'])<1:
            errors['plan']='Plan must be provided'         
        elif len(postData['plan'])<3:
            errors['plan']='A trip plan must consist of 3 characters'
        return errors      

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=100)
    created_by = models.ForeignKey(User , related_name="trip_creator", on_delete=models.CASCADE,default='')
    user_in_trip = models.ManyToManyField (User , related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()



