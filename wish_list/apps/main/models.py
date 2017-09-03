# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt, re
from datetime import date, datetime

# Create your models here.

class ItemManager(models.Manager):
    def add(self, request):
        
        user = User.objects.get(id=request.session['user']['user_id'])

        Item.objects.create(item=request.POST['item'], seller=user)
#-----------------------------------------------------------------------------------------------------------

    def join(self, request, id):
        user = User.objects.get(id=request.session['user_id'])

        item = Item.objects.get(id=id)

        item.wishers.add(user)
#-----------------------------------------------------------------------------------------------------------




class User(models.Model):
    full_name = models.CharField(max_length=65)
    username = models.CharField(max_length=65)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    item = models.CharField(max_length=255)
    seller = models.ForeignKey(User, related_name='item')
    wishers = models.ManyToManyField(User, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)