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
        return redirect('/hangman/home')
    
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
    return render(request, 'hangman_app/home.html', context)

def new_word(request, user_id):
    errors = Word.objects.new_word_validation(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect('/hangman/home')
    
    else:
        user = User.objects.get(id = user_id)
        Word.objects.create(word = request.POST['new_word'], user = user, hint = request.POST['hint'])
        messages.success(request, "New word successfully added")
        print "Hello World"
        return redirect('/hangman/home')

def user_info(request, user_id):
    user = User.objects.get(id = user_id)
    word_count = User.objects.get(id = user_id).submitted_by.count()
    words = Word.objects.filter(user = user)
    
    context = {
        'user': user,
        'word_count': word_count,
        'words': words
    }
    return render(request, 'hangman_app/user_info.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')