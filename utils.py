import enums
import math
import copy
import csv
import pandas as pd
from collections import Counter
from heapq import nlargest
from wordfreq import word_frequency

# Makes a list of all the possible Wordle words
def listify(filename, diff='H'):
    with open(filename) as f:
        lines = f.readlines()
        
    if diff == 'H':
        return [line.strip() for line in lines]
        
    word_list = [(line.strip(), word_frequency(line.strip(), 'en')) for line in lines]
    word_list.sort(key=lambda x:x[1], reverse=True)

    if diff == 'M':
        cutoff = int(enums.M_CUTOFF * len(word_list))
    elif diff == 'E':
        cutoff = int(enums.E_CUTOFF * len(word_list))
    return [term[0] for term in word_list[:cutoff]]


# Makes a list of all the possible Wordle words WITH UNIQUE LETTERS
def unique_listify(filename):
    final = []
    with open(filename) as f:
        lines = f.readlines()
    return [word.strip() for word in lines if len(Counter(word.strip())) == len(word.strip())]        


# Returns a list of words with only unique letters
def unique_only(word_list):
    return [word for word in word_list if len(set(list(word))) == 5]


def stable_sigmoid(a, x):
    x -= 2.88e-6
    if x >= 0:
        z = math.exp(-a*x)
        sig = 1 / (1 + z)
        return sig
    else:
        z = math.exp(a*x)
        sig = z / (1 + z)
        return sig


# Writes a sorted csv of the frequency of each word
def freq_file(word_list):
    with open('word_freqs.csv', 'w', newline='') as csvfile:
        fields = ['word', 'freq']
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        
        for word in word_list:
            csvwriter.writerow([word, word_frequency(word, 'en')])
            
    df = pd.read_csv('word_freqs.csv')
    df.sort_values(['freq'], axis=0, ascending=False, inplace=True)
    df.to_csv('word_freqs.csv', index=False)
    
    return df
        

# Calculates freq of each letter BY TOTAL FREQUENCY AND BY POSITION
def letter_dists(filename):
    word_list = listify(filename)
    dists = {}
    dists_pos = {}
    
    for letter in enums.ALPHABET:
        dists[letter] = 0
        dists_pos[letter] = {0:0, 1:0, 2:0, 3:0, 4:0}
    
    for word in word_list:
        for letter in enumerate(word):
            dists[letter[1]] += 1
            dists_pos[letter[1]][letter[0]] += 1
            
    return dists, dists_pos

    
# Calculates percent occurrence of each letter BY FREQUENCY
def freq_dists_percent(dists, num_words):
    for letter in dists:
        dists[letter] = round(dists[letter] / (num_words * 5), 6)
    return dists
    

# Calculates percent occurrence of each letter BY POSITION
def pos_dists_percent(dists, num_words):
    for letter in dists:
        dists[letter] = {ind: round(dists[letter][ind] / num_words, 6) for ind in dists[letter]}
    return dists


# Calculates score based on letter probabilities for a word BY POSITION
def pos_score(word, dists_percent):
    score = 0
    for letter in enumerate(word):
        score += dists_percent[letter[1]][letter[0]]
    return round(score, 6)


# Calculates score based on letter probabilities for a word BY FREQUENCY
def freq_score(word, dists_percent):
    score = 0
    for letter in enumerate(word):
        score += dists_percent[letter[1]]
    return round(score, 6)


# Calculates score for all possible words BY POSITION
def pos_score_all_words(word_list, dists_percent):
    scores = {word: pos_score(word, dists_percent) for word in word_list}
    return scores


# Calculates score for all possible words BY FREQUENCY
def freq_score_all_words(word_list, dists_percent):
    scores = {word: freq_score(word, dists_percent) for word in word_list}
    return scores   
    
    
# Looks up the score of a specific word
def lookup_score(word, all_words):
    try:
        return all_words[word]
    except:
        # If word doesn't exist in possibilities
        return -1
    

# Returns the N highest words based on scores from list (can be unique or non-unique)
def n_best(word_list, N):
    res = nlargest(N, word_list, key=word_list.get)
    return {word: word_list[word] for word in res} 