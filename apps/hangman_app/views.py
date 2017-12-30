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
    request.session['hint'] = word.hint
    request.session['counter'] = 0
    request.session['guess_container'] = []
    blanks = '_' * len(request.session['word'])
    
    request.session['blanks'] = ' '.join(blanks) ##Creates the spacing between each underscore

    context = {
        'word': word,
    }
    return render(request, 'hangman_app/game.html', context)

def guess(request):
    blanks = request.session['blanks']
    guess = request.POST['user_guess']

    blanks = "".join(str(word) for word in blanks)

    print blanks

    blanks = list(blanks) ## list to make the contents iterable 
    print blanks
    blanks = map(str, blanks) ##removes 'u unicode from list(blanks)
    print blanks


    if guess in request.session['word']: #If the guess is in the word

        if guess not in request.session['guess_container']: ## Check if the guessed letter is already used, if not proceed
            request.session['guess_container'].append(guess)
            for index, letter in enumerate(request.session['word']): # Split it into a tuple

                if guess == letter: # if the guess is the letter of the tuple
                    blanks[index] = str(letter) ## index to location position of blanks
                    request.session['blanks'] = ''.join(blanks)
                    print request.session['blanks']
                    return render(request, 'hangman_app/game.html') 
    
        else:
            messages.error(request, "You've already guessed that letter, please try again")
            return render(request, 'hangman_app/game.html')
    
    else:
        request.session['counter'] += 1
        request.session['guess_container'].append(guess)
        messages.error(request, "NOT FOUND! Ouch, one step closer to X_X")
        return render(request, 'hangman_app/game.html')
        
        
    return render(request, 'hangman_app/game.html')

###################################################################

#Game Functionality

###################################################################