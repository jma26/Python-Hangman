# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

##################################################################

#Login/Registration

##################################################################
def index(request):
    return render(request, 'hangman_app/index.html')

def register(request):
    errors = User.objects.register_validation(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    
    else: 
        user = User.objects.new_user(request.POST)
        request.session['user_id'] = user.id
        return redirect('/user/reroute')

def login(request):
    result = User.objects.login_validation(request.POST)

    if type(result) is list:
        for error in result:
            messages.error(request, error)
        return redirect('/')
    
    else:
        request.session['user_id'] = result.id
        return redirect('/user/reroute')

def reroute(request):
    try:
        request.session['user_id']
        return redirect('/hangman')
    
    except:
        return redirect('/')


###################################################################

#End of Login/Registration

###################################################################

def hangman(request):
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'hangman_app/game.html', context)