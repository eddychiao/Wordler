import re
import utils
from wordfreq import word_frequency


# RULE CONVENTION:
# 
# [y] = exact spot, [n] = not in word, [m] = wrong spot, in word 1+ times
#
# input: limits
# ACTUAL: shell
# GUESS: sleep
#
# limits: [('s', 'y'), ('l', 'm'), ('e', 'y'), ('e', 'n'), ('p', 'n')]

# Interestingly, words that end in 's' are rarely chosen as the word, meaning plurals and present tenses are not picked
    
    
word_file = 'wordle-words.txt'
freq, pos = utils.letter_dists(word_file)
num_words = len(utils.listify(word_file))

freq_percent = utils.freq_dists_percent(freq, num_words)
pos_percent = utils.pos_dists_percent(pos, num_words)
    
    
# Performs hard filter based on words with letters in the correct placement
def filter_words(word_list, limits):
    re_string = ""
    matches = []
    rule_occurrences = {letter[0]: 0 for letter in limits}

    for rule in limits:
        if rule[1] == 'y':
            re_string += rule[0]
            rule_occurrences[rule[0]] += 1
        elif rule[1] == 'm':
            re_string += '[^' + rule[0] + ']'
            rule_occurrences[rule[0]] += 1
        else:        
            re_string += '[^' + rule[0] + ']'             
    
    for word in word_list:
        if re.match(re_string, word):
            occurrence_match = True
            for letter in rule_occurrences:
                if rule_occurrences[letter] == 0 and word.count(letter) > 0:
                    occurrence_match = False
                    break
                elif rule_occurrences[letter] > word.count(letter):
                    occurrence_match = False
                    break
            if occurrence_match:
                matches.append(word)
    return matches, len(matches)


# Performs soft filter (only removes N words)
def filter_words_nonstrict(word_list, limits):
    re_string = ""
    matches = []
    rule_occurrences = {letter[0]: 0 for letter in limits}

    for rule in limits:
        if rule[1] == 'y':
#             re_string += rule[0]
            rule_occurrences[rule[0]] += 1
        elif rule[1] == 'm':
#             re_string += '[^' + rule[0] + ']'
            rule_occurrences[rule[0]] += 1
        else:        
            re_string += '[^' + rule[0] + ']'             
    
    for word in word_list:
        if re.match(re_string, word):
            occurrence_match = True
            for letter in rule_occurrences:
                if rule_occurrences[letter] == 0 and word.count(letter) > 0:
                    occurrence_match = False
                    break
                elif rule_occurrences[letter] > word.count(letter):
                    occurrence_match = False
                    break
            if occurrence_match:
                matches.append(word)
    return matches, len(matches)


# Scores and suggests list of N best word to pick
def rank(word_list, N=20, metric='freq'):
    if metric == 'freq':
        scored = utils.freq_score_all_words(word_list, freq_percent)
    elif metric == 'pos':
        scored = utils.pos_score_all_words(word_list, pos_percent)
    else:
        print('Incorrect metric')
        return -1
        
    scored = {entry: round(scored[entry] * (1 * word_frequency(entry, 'en')), 6) for entry in scored} 
    nbest = utils.n_best(scored, N)
    return nbest
    
    

def heuristic(word, scored):
    return
    
    
