import utils
import random

# All possible words
word_file = 'wordle-words.txt'
word_list = utils.listify(word_file)


def run_game(diff):
    
    total_list = utils.listify(word_file, diff)
    
    actual = generate_word(total_list[:])
    guesses = 0
    guess = ''
    guess_list = ''
    
    while guesses < 6:
        guess = input("Guess a 5-letter word: ").lower()
        while len(guess) != 5 or guess not in word_list:
            guess = input("Not a valid word. Guess a 5-letter word: ").lower()
            
        guesses += 1
        match_list = get_match(guess, actual)
        emoji_list = return_squares(match_list)
        print(emoji_list)
        print('Guesses used: ', guesses)
        guess_list += emoji_list + '\r\n'
        if guess == actual:
            break
    
    if guess == actual:
        print()
        print()
        print('Wordle X ' + str(guesses) + '/6')
        print()
        print(guess_list)
        print()
        print('Word was: ', actual)
        print('Good job!')
        
    else:
        print()
        print()
        print('Wordle X/6')
        print()
        print(guess_list)
        print()
        print('Word was: ', actual)
        print('Try again!')
    
    return

        

def generate_word(word_list):
    s_list = []
    for word in enumerate(word_list):
        if word[1][-1] == 's':
            out = word_list.pop(word[0])
            s_list.append(out)
            
    rand_normal = random.choices(word_list, k=95)
    rand_s = random.choices(s_list, k=5)
    
    word = random.choice(rand_normal + rand_s)
    return word


# ACTUAL: shell
# GUESS: sleep
# limits: [('s', 'y'), ('l', 'm'), ('e', 'y'), ('e', 'n'), ('p', 'n')]
# return match list
def get_match(guess, actual):
    if len(guess) != 5 and len(actual) != 5:
        return -1
    
    res = []
    
    actual_dict = {}
    for letter in actual:
        if letter not in actual_dict:
            actual_dict[letter] = 1
        else:
            actual_dict[letter] += 1
    
    for i in range(5):
        if guess[i] == actual[i] and actual_dict[guess[i]] > 0:
            res.append((actual[i], 'y'))
            actual_dict[guess[i]] -= 1
        elif guess[i] != actual[i] and guess[i] not in actual:
            res.append((guess[i], 'n'))
        elif guess[i] != actual[i] and guess[i] in actual:
            # case: if actual = RESET and guess = ERASE
            if actual_dict[guess[i]] > 0:
                res.append((guess[i], 'm'))
                actual_dict[guess[i]] -= 1
            else:
                res.append((guess[i], 'n'))
        else:
            res.append((guess[i], 'n'))
    print(res)
    return res


def return_squares(match_list):
    res = ""
    for letter in match_list:
        if letter[1] == 'y':
            res += '🟩'
        elif letter[1] == 'm':
            res += '🟨'
        elif letter[1] == 'n':
            res += '⬛️'
    return res


def rule_from_squares(string, icons):
    return list(zip(list(string), list(icons)))


