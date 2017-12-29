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

###################################################################

#Beginning of hangman home page 

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

###################################################################

#End of hangman home page

###################################################################

def game(request):
    word = Word.objects.random_word(request.POST)
    request.session['word'] = word.word
    request.session['blanks'] = []
    request.session['blanks_index'] = []
    request.session['hint'] = word.hint
    unicode_blanks = '_' * len(request.session['word'])

    blanks = str(" ".join(unicode_blanks)) # str() removes 'u unicode
    
    request.session['blanks'].append(blanks)

    print request.session['blanks']
    context = {
        'word': word
    }
    return render(request, 'hangman_app/game.html', context)

def guess(request):
    unicode_blanks = '_' * len(request.session['word'])
    guess = request.POST['user_guess']
    blanks = str("".join(unicode_blanks))
    index = str("".join(request.session['word']))

    blanks1 = list(blanks)
    index1 = list(index) ## list allows us to iterate

    if guess in request.session['word']: #If the guess is in the word
        for index, letter in enumerate(index1): # Split it into a tuple

            if guess == letter: # if the guess is the letter of the tuple
                blanks1[index] = guess # we assign the guess letter to the index
            print blanks1
        
    return render(request, 'hangman_app/game.html')

###################################################################

#Game Functionality

###################################################################