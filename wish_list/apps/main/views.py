# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from .models import *
from django.shortcuts import render, redirect
from datetime import date, datetime
from django.contrib import messages


# Create your views here.
#-----------------------------------------------------------------------------------------------------------

def index(request):
    return render(request, 'main/index.html')

#-----------------------------------------------------------------------------------------------------------    

#-----------------------------------------------------------------------------------------------------------

def register(request):
    
    full_name = request.POST['full_name']
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']

    valid = True
    if len(full_name) < 3:
        messages.error(request, '*Name must be at least 3 characters')
        valid = False

    if len(username) < 3:
        messages.error(request, '*Username must be at least 3 characters')
        valid = False
    
    if len(password)< 8:
        messages.error(request, '*Password must be at least 8 characters long.')
        valid = False

    if password != confirm_password:
        messages.error(request, '*Passwords do not match.')
        valid = False

    if valid:
        try: 
            User.objects.create(full_name = full_name, username = username, password = password)
            messages.success(request, '*You have successfully registered. Please sign in.')
            return redirect('/')
        except:
            messages.error(request, '*User exists')
            return redirect('/')
    else:
        return redirect('/')


#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def login(request):

    valid = True

    username = request.POST['username']
    password = request.POST['password']
    user_id = ''

    if len(username) < 3:
        messages.error(request, '*Username must be at least 3 characters')
        valid = False
    
    if len(password)< 8:
        messages.error(request, '*Password must be at least 8 characters long.')
        valid = False

    if valid:
        try:
            user_id = User.objects.get(username=username)
        
        except:
            messages.error(request, '*Invalid User')
            return redirect('/')
    
        if password == user_id.password:
            # print "first name is: ", user_id.first_name
            # print "email is: ", user_email
            request.session['full_name'] = user_id.full_name
            request.session['username'] = username
            request.session['user_id'] = user_id.id
            return redirect('/home')
        else:
            messages.error(request, '*Invalid Password')
        return redirect('/')
    
    return redirect('/')
    

#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def home_page(request):
    
    data = Item.objects.all()
    items ={
        "items": data,
        'wished_items': Item.objects.filter(wishers__id=request.session['user_id'])
    }
    return render(request, 'main/home.html', items)
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def new_item(request):
    return render(request, 'main/new_item.html')
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def add(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":

        completed_form = True

        item = request.POST['item']
        if len(item) < 1:
            completed_form = False
            messages.error(request, "Item is required")

        if completed_form:
            user = User.objects.get(pk=request.session['user_id'])

            Item.objects.create(item=request.POST['item'], seller=User.objects.get(id=request.session['user_id']))


        else:
            messages.error(request, "please try again")
            return redirect('/item_form')

    return redirect('/home')
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def view_item(request, item_id):
    
    item = Item.objects.get(id=item_id)
    wishers = item.wishers.all()

    data = {
        'item': item,
        'wishers': wishers
    }
    
    return render(request, 'main/view_item.html', data)
    
#-----------------------------------------------------------------------------------------------------------
def join(request, item_id):
    
    itemInQuestion = Item.objects.get(id=item_id)
    userThatWantsToAdd = User.objects.get(id=request.session['user_id'])
    itemInQuestion.wishers.add(userThatWantsToAdd)
    itemInQuestion.save()
    # wishedItemUserId = Item.wishers
    # print wishedItemUserId_user_id
    # if wishedItemUserId == userThatWantsToAdd:
    #     messages.error(request, "Item already in wishlist")

    return redirect('/home')

#-----------------------------------------------------------------------------------------------------------
def unjoin(request, item_id):
    
    itemInQuestion = Item.objects.get(id=item_id)
    userThatWantsToRemove = User.objects.get(id=request.session['user_id'])
    itemInQuestion.wishers.remove(userThatWantsToRemove)
    itemInQuestion.save()

    return redirect('/home')
#-----------------------------------------------------------------------------------------------------------
def logout(request):
    request.session.clear()
    return redirect('/')
#-----------------------------------------------------------------------------------------------------------

def remove(request, id):
    Item.objects.get(id=id).delete()
    return redirect('/home')