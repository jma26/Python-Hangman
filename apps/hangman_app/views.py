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

###################################################################

#Game Functionality

###################################################################

def game(request):
    word = Word.objects.random_word(request.POST)
    request.session['word'] = word.word.lower()
    request.session['hint'] = word.hint
    request.session['word_length'] = len(word.word)
    request.session['counter'] = 6

    ## Resets guess_container each time new game is generated ##
    request.session['guess_container'] = []
    ## ' '.join() to remove the square brackets in beginning of game, redundant- yes
    request.session['guess_container'] = ' '.join(request.session['guess_container'])
    blanks = '_' * len(request.session['word'])
    
    request.session['blanks'] = blanks

    hangman_art = [
        ''' 
        +---+
        |   |
            |
            |
            |
    ========== ''',
        '''
        +---+
        |   |
        O   |
            |
            |
    ========== ''',

        '''
        +---+
        |   |
        O   |
        |   |
            |
    ========== ''',

        '''
        +---+
        |   |
        O   |
       /|   |
            |
    ========== ''',

        '''
        +---+
        |   |
        O   |
       /|\  |
        |
    ========== ''',

        '''
        +---+
        |   |
        O   |
       /|\  |
       /    |
    ========== ''',

        '''
        +---+
        |   |
        O   |      You're dead :(
       /|\  |
       / \  |
    ========== '''
    ]

    request.session['art'] = hangman_art[0]
        
    context = {
        'word': word,
    }

    return render(request, 'hangman_app/game.html', context)

def guess(request):
    blanks = request.session['blanks']
    guess = request.POST['user_guess'].lower()
    hidden_word = request.session['word'].lower()

    ## Convert guess_container to list to iterate 
    request.session['guess_container'] = list(request.session['guess_container'])

    hangman_art = [
        ''' 
        +---+ <br>
        |   |
            |
            |
            | 
    ========== ''',
        '''
        +---+
        |   |
        O   |
            |
            |
    ========== ''',
        '''
        +---+
        |   |
        O   |
        |   |
            |
    ========== ''',
        '''
        +---+
        |   |
        O   |
       /|   |
            |
    ========== ''',
        '''
        +---+
        |   |
        O   |
       /|\  |
        |
    ========== ''',
        '''
        +---+
        |   |
        O   |
       /|\  |
       /    |
    ========== ''',
        '''
        +---+
        |   |
        O   |      You're dead :(
       /|\  |
       / \  |
    ========== '''
    ]

    blanks = list(blanks) ## list to make the contents iterable

    if len(guess) <= 0:  ## CONDITION: returns an error message if no input given
        request.session['guess_container'] = ' '.join(request.session['guess_container'])
        messages.error(request, "No guess given, please take a guess")
        return render(request, 'hangman_app/game.html')
    
    if len(guess) > 1: ## CONDITION: returns an error message if user inputs more than 1
        request.session['guess_container'] = ' '.join(request.session['guess_container'])
        messages.error(request, "Only one character at a time, guess again")
        return render(request, 'hangman_app/game.html')
    
    if not guess.isalpha():
        request.session['guess_container'] = ' '.join(request.session['guess_container'])
        messages.error(request, "Alphabetical letters only!")
        return render(request, 'hangman_app/game.html')

    if guess in hidden_word and guess not in request.session['guess_container']: #If the guess is in the word and check if the guessed letter is already used - if not proceed
        request.session['guess_container'].extend(guess)
        request.session['guess_container'] = ' '.join(request.session['guess_container']) # update guess container so it can not be guessed again

        for index, letter in enumerate(hidden_word): # Split it into a tuple

            if hidden_word[index] == guess: # if the guess is the letter of the tuple
                blanks[index] = str(guess) ## index to location position of blanks
                request.session['blanks'] = ''.join(blanks)  # removes 'u unicode for display purposes

        if request.session['blanks'] == request.session['word']:
            messages.success(request, "Congratulations, you've won!")

        return render(request, 'hangman_app/game.html')

    elif guess in request.session['guess_container']:
        messages.error(request, "You've already guessed that letter, please try again")
        request.session['guess_container'] = ' '.join(request.session['guess_container']) # removes 'u unicode for display purposes
        return render(request, 'hangman_app/game.html')
    
    else:
        request.session['counter'] -= 1
        request.session['guess_container'].extend(guess)
        request.session['guess_container'] = ' '.join(request.session['guess_container'])

        if request.session['counter'] == 5:
            request.session['art'] = hangman_art[1]
        elif request.session['counter'] == 4:
            request.session['art'] = hangman_art[2]
        elif request.session['counter'] == 3:
            request.session['art'] = hangman_art[3]
        elif request.session['counter'] == 2:
            request.session['art'] = hangman_art[4]
        elif request.session['counter'] == 1:
            request.session['art'] = hangman_art[5]
        elif request.session['counter'] == 0:
            request.session['art'] = hangman_art[6]

        messages.error(request, "NOT FOUND! Ouch, one step closer to X_X")
        return render(request, 'hangman_app/game.html')

###################################################################

# End of Game Functionality

###################################################################