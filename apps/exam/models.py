from django.db import models
import bcrypt 
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def registerValidator(self, form):
        errors = {}

        if len(form['name']) < 1:
            errors['email'] = "Name cannot be blank!"
        elif len(form['name']) < 3:
            errors['name'] = "Name must be 3+ characters"

    
        if len(form['username']) < 1:
            errors['username'] = "Username cannot be blank!"
        elif len(form['username']) < 3:
            errors['username'] = "Username must be 3+ characters"
        elif User.objects.filter(username=form['username']):
            errors['username'] = "Username is already in database"
    
        if len(form['password']) < 1:
            errors['password'] = "Password cannot be blank!"
        elif len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"

        if form['repeat'] != form['password']:
            errors['password'] = "Passwords must match!"
    
        return errors
    
    def loginValidator(self, form):
        errors = {}

        if len(form['logpassword']) < 1:
            errors['password'] = "Password cannot be blank!"

        print(form['loguser'])
        if len(form['loguser']) < 1:
            errors['logemail'] = "Username cannot be blank!"
        elif not User.objects.filter(username=form['loguser']):
            errors['loguser'] = "Username is not in database"
        
        else:
            print('form', form)
            user = User.objects.filter(username=form['loguser'])
            if not bcrypt.checkpw(form['logpassword'].encode(), user[0].password.encode()):
                errors['logpassword'] = "Passwords don't match"
        return errors

class TripManager(models.Manager):
    def tripValidator(self, form):
        errors = {}
        if len(form['name']) < 1:
            errors['name'] = "Destination cannot be left blank!"
        
        if len(form['description']) < 1:
            errors['description'] = "Description cannot be left blank!"

        if not form['date_from']:
            errors['date_from'] = "Travel Date From cannot be left blank!"
        elif form['date_from'] < str(datetime.now()):
            errors['date_from'] = "Travel Date From must be a future date"
        
        if not form['date_to']:
            errors['date_to'] = "Travel Date To cannot be left blank!"
        elif form['date_to'] < form['date_from']:
            errors['date_to'] = "Travel Date To cannot be before Travel Date From"

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Trip(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_from = models.DateField()
    date_to = models.DateField()
    uploader = models.ForeignKey(User, related_name="uploaded_trips")
    travel_users = models.ManyToManyField(User, related_name="travel_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = TripManager()