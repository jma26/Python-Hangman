# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register_validation(self, postData):
        errors = []
        if len(postData['first_name']) <= 0:
            errors.append("First name field can't be blank")       
        elif not postData['first_name'].isalpha():
            errors.append("First name must contain letters only")
        
        if len(postData['last_name']) <= 0:
            errors.append("Last name field can't be blank")
        elif not postData['last_name'].isalpha():
            errors.append("Last name must contain letters only")
        
        if len(postData['alias']) <= 0:
            errors.append("Alias field can't be blank")
        
        if len(postData['password']) < 8:
            errors.append("Password must be 8 characters long")
        elif postData['password'] != postData['passwordcf']:
            errors.append("Password does not match")
        
        if not EMAIL_REGEX.match(postData['email'].lower()):
            errors.append("Email is not valid")
        elif not errors and User.objects.filter(email = postData['email'].lower()):
            errors.append('Email already registered')

        return errors

    def login_validation(self, postData):
        errors = []
        users = self.filter(email = postData['email'])
        if not users:
            errors.append("Email does not exist")
        
        else:
            user = users[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append("Wrong password")
        
        if not errors:
            return user
        
        return errors

    
    def new_user(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        print hash1

        return User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hash1, alias = postData['alias'])

class WordManager(models.Manager):

    def new_word_validation(self, postData):
        errors = []
        if len(postData['new_word']) <= 0:
            errors.append("New word can't be empty")
        
        if len(postData['hint']) <= 0:
            errors.append("Hint can't be empty")
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()

class Word(models.Model):
    word = models.CharField(max_length = 20)
    user = models.ForeignKey(User, related_name = 'submitted_by')
    hint = models.CharField(max_length = 255)
    objects = WordManager()