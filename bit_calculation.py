import csv
import math
import utils
import enums
import random
import numpy as np
import pandas as pd
import itertools
import recommender
from wordfreq import word_frequency


# takes in word and creates all possible combinations of patterns
# should be len 243 = 3 ** 5
def create_rules_possibilities(word):
    total_rules = []
    combos = []
    ymn_list = ['y', 'm', 'n']
    
    p = itertools.product(ymn_list, repeat=5)
    
    for subset in p:
        temp = list(zip(list(word), subset))
        combos.append(temp)
    return combos
        

# simulates all possible pattern matches for a word
def entropy(word, word_list, rules_list):
    entropy = 0
    
    for rule in rules_list:
        _, matches = recommender.filter_words(word_list, rule)
        p = matches / len(word_list)
        if p == 0:
            bit_val = 0
        else:
            bit_val = math.log(1 / p, 2)
        entropy += p * bit_val
        
    return round(entropy, 6)


# sorted CSV list of all words and their expected STARTING entropy (at 0 guesses)
# this takes a long time to run
def starting_entropy_csv(word_list):
    
    with open('starting_entropy.csv', 'w', newline='') as csvfile:
        fields = ['word', 'entropy']
        
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        counter = 0
        for word in word_list:
            rules_list = create_rules_possibilities(word)
            E = entropy(word, word_list, rules_list)
            csvwriter.writerow([word, E])
            counter += 1
            if counter % 100 == 0:
                print('Terms calculated: ', counter)
        print('Done.')

    return


# sorted CSV list of all words and their expected STARTING entropy UNIQUE LETTERS ONLY (at 0 guesses)
# this takes a long time to run
def starting_entropy_unique_csv(word_list):
    
    with open('starting_entropy_unique.csv', 'w', newline='') as csvfile:
        fields = ['word', 'entropy']
        
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        counter = 0
        for word in word_list:
            rules_list = create_rules_possibilities(word)
            E = entropy(word, word_list, rules_list)
            csvwriter.writerow([word, E])
            counter += 1
            if counter % 100 == 0:
                print('Terms calculated: ', counter)
        print('Done.')
    
    return


# adds frequency and sum of both entropy and frequency
def freq_calc(filename):
    
    new_col = []
    sum_both = []
    df = pd.read_csv(filename)
    for i in df.index:
        freq_score = utils.stable_sigmoid(1.0e6, word_frequency(df['word'][i], 'en')) * 1.2
        sum_score = round(df['entropy'][i] + freq_score, 6)
        
        if df['word'][i][-1] == 's':
            freq_score -= 0.3
        
        new_col.append(freq_score)
        sum_both.append(sum_score)
        
    df['frequency'] = new_col
    df['sum'] = sum_both
    
    df.sort_values(['sum'], axis=0, ascending=False, inplace=True)
    df.to_csv(filename, index=False)
    
    return df


# randomly choose a starting word from a list of best choices
def choose_first_word(filename):
    df = pd.read_csv(filename)
    df.sort_values(['sum'], axis=0, ascending=False, inplace=True)
    first_10 = df.iloc[:, 0].tolist()[:10]
    first_word = random.choice(first_10)
    print(first_10)
    return first_word
    
    
def recommend(word_list, hits=3):
    entries = []
    f = open('past_words.txt', 'r')
    past_words = [line.strip() for line in f.readlines()]
    for word in word_list:
        E = entropy(word, word_list, create_rules_possibilities(word))
        freq = utils.stable_sigmoid(1.7e6, word_frequency(word, 'en')) * 1.2
        
        if word[-1] == 's':
            freq -= 0.3
        
        sum_score = E + freq
        # dissuade suggesting non-unique words with small number of hits
        if hits < 3 and len(set(list(word))) < 5:
            sum_score *= 0.5
        
        # dissuade recommending a word that has been picked before
        if word in past_words:
            sum_score *= 0.1
            
        entries.append((word, E, freq, sum_score))
    return sorted(entries, key=lambda x: x[3], reverse=True)[:10]
