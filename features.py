#!/usr/bin/python3
# CS441 - Bruh Beyene
# HW3 - Author Identification by Machine Learning 
# This module builds booleanized instances for use in Bart Massey's machine learners
# to discriminate between paragraphs written by two quite different authors.

import math, os, sys

# Read words of each paragraph from the four novels 
# Strip away leading and trailing punctuation 
# Inspired by Bart Massey's paragraph.py
def novel(fname):

    with open(fname, "r") as f:
        pars = list()
        par = list()
        for line in f:
            words = line.split()
            if not words:
                if par and len(par) > 1:
                    pars.append(par)
                par = list()
                continue
            par.append(line)
        if par and len(par) > 1:
            pars.append(par)

        return pars


# Remove internal punctuation, keep hyphenated, convert to lowercase
# Ignore words less than 2 letters, discard titles, remove dashes
# Reduce to set of unique words in paragraph, create unique word dictionary
# Inspired by Bart Massey's vocab.py
def construct(novel, corpus_words):

    def alphas(w): 
        return ''.join([c for c in w if (c.lower() >= 'a' and c.lower() <= 'z') or c == '-']).lower()

    discard = {  'the', 'lady', 'lord', 'madam', 'madame', 'miss', 'mr', 'mrs', 'sir' }
    pars = list()
    for paragraph in novel:
        allwords = set()
        for sentence in paragraph:
            words = sentence.replace('--', ' ').split()
            justwords = {alphas(w) for w in words if len(w) > 2} # removes titles and '', '-', '—', 's', 'i', 'a', etc
            allwords |= justwords
            allwords -= discard
            corpus_words |= allwords
        if allwords is not None:
            pars.append(allwords)

    return pars


# Label with unique paragraph identifier and author class (1 = Shelley, 0 = Austen).
def label(fname, novel):

    label = None
    labeled = list()
    split_fname = fname.split()
    identifier = '-'.join(split_fname)[0:-4]
    if 'shelley' in fname:
        label = 1
    if 'austen' in fname:
        label = 0
    
    for i, paragraph in enumerate(novel):
        par = list()
        par.append(f'{identifier}.{i}')
        par.append(f'{label}') 
        for word in paragraph:
            par.append(word)
        labeled.append(par)

    return labeled


# Calculate information gain of splitting paragraphs on words using entropy equations
# G = initial_entropy - split_entropy
def entropy(matrix, total_pars):

    # calculate class entropy: feature = 0
    nNeg = matrix[0][0] + matrix[0][1] # times word not used

    # author = 0
    prNeg_0 = matrix[0][0] / nNeg 
    try: lg_0 = math.log(prNeg_0, 2)
    except: lg_0 = 0
    # author = 1
    prNeg_1 = matrix[0][1] / nNeg 
    try: lg_1 = math.log(prNeg_1, 2)
    except: lg_1 = 0

    Uneg = -prNeg_0 * lg_0 - prNeg_1 * lg_1

    # calculate class entropy: feature = 1
    nPos = matrix[1][0] + matrix[1][1] # times word used

    # author = 0
    prPos_0 = matrix[1][0] / nPos
    try: lg_0 = math.log(prPos_0, 2)
    except: lg_0 = 0
    # author = 1
    prPos_1 = matrix[1][1] / nPos 
    try: lg_1 = math.log(prPos_1, 2)
    except: lg_1 = 0

    Upos = -prPos_0 * lg_0 - prPos_1 * lg_1

    # entropies weighted by prob of being in that set
    Usplit = (nNeg / total_pars * Uneg) + (nPos / total_pars * Upos)
    return Usplit


# Get a sorted word:gain mapping
def gains(words, paragraphs):

    word_gains = dict()
    total_pars = 0
    for nov in paragraphs:
        total_pars += len(nov)

    for word in words:
        matrix = [[0] * 2 for i in range(2)]
        for nov in paragraphs:
            for par in nov:
                author = int(par[1])
                if word in par:
                    matrix[1][author] += 1
                else:
                    matrix[0][author] += 1

        # {word} appears: {Boolean(i)}, by author: {j} {matrix[i][j]} times

        G = entropy(matrix, total_pars) 
        word_gains[word] = G

    sorted_wg = sorted(word_gains.items(), key=lambda item: item[1])
    return sorted_wg


# For each paragraph output a comma-separated line:
# identifier, class, and the values of the 300 features
def output(words, paragraphs):

    nfeatures = len(words)
    for nov in paragraphs:
        for par in nov:
            instances = list()
            instances.append(par[0])
            instances.append(int(par[1]))
            for w in words:
                if w in par:
                    instances.append(1)
                else:
                    instances.append(0)
            for i, v in enumerate(instances):
                if i <= nfeatures:
                    print(v, end=', ')
                else:
                    print(v, end='\n')


nfeatures = 300
paragraphs = [] # [ 'identifier', 'class', unique-words ] per novel
corpus_words = set() # unique words of novels
word_gains = dict() # calculated 'word':gain of corpus words
features = [] # nfeatures highest-gain words to use for splits

# Read novels, label paragraphs, create dictionary of unique words
for fname in sys.argv[1:]:
    paragraphs.append(label(fname, construct(novel(fname), corpus_words)))

# Calculate, sort, pick best words to split based on (-1 < G < 0)
word_gains = gains(corpus_words, paragraphs)
for w, g in word_gains[0:nfeatures]:
    features.append(w)

# Print instances
output(features, paragraphs)
