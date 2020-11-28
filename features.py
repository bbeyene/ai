# CS441 Bruh Beyene
# HW3 - Author Identification by Machine Learning 
# This module builds booleanized instances for use in Bart Massey's ID3 machine learning code
# to discriminate between paragraphs written by two quite different authors.

import os, math, sys

# Read the words of each paragraph from the four novels into memory
# Strip away leading and trailing punctuation 
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
# Ignore words less than 4 letters, discard titles
# Reduce to set of unique words in paragraph
def construct(novel, corpus_words):

    def alphas(w): 
        return ''.join([c for c in w if (c.lower() >= 'a' and c.lower() <= 'z') or c == '-']).lower()

    discard = {'—', 'a', 'i', 's', '', 'lady', 'lord', 'madam', 'madame', 'miss' 'mr', 'mrs', 'sir', 'the'}
    pars = list()
    for paragraph in novel:
        allwords = set()
        for sentence in paragraph:
            words = sentence.replace('--', ' ').split()
            justwords = {alphas(w) for w in words if len(w) > 4}
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
def calc_gains(words, paragraphs):

    word_gains = dict()
    total_pars = 0
    for nov in paragraphs:
        total_pars += len(nov)

    def calc_entropy(matrix, total_pars):
        # split word ununsed/used
        nNeg = matrix[0][0] + matrix[0][1] # the feature = 0 split
        nPos = matrix[1][0] + matrix[1][1] # the feature = 1 split

        # word unused class entropy: feature = 0, author 0/1
        prNeg_0 = matrix[0][0] / nNeg
        prNeg_1 = matrix[0][1] / nNeg
        try: lg_0 = math.log(prNeg_0, 2)
        except: lg_0 = 0
        try: lg_1 = math.log(prNeg_1, 2)
        except: lg_1 = 0
        uNeg = -prNeg_0 * lg_0 - prNeg_1 * lg_1

        # word used class entropy: feature = 1, author 0/1
        prPos_0 = matrix[1][0] / nNeg
        prPos_1 = matrix[1][1] / nNeg
        try: lg_0 = math.log(prPos_0, 2)
        except: lg_0 = 0
        try: lg_1 = math.log(prPos_1, 2)
        except: lg_1 = 0
        uPos = -prPos_0 * lg_0 - prPos_1 * lg_1

        # weight each entropy by prob of being in that set
        uPrime = (nNeg / total_pars * uNeg) + (nPos / total_pars * uPos)

        # G = U - uPrime
        G = -uPrime

        return G

    for word in words:
        matrix = [[0] * 2 for i in range(2)]
        for nov in paragraphs:
            for par in nov:
                author = int(par[1])
                if word not in par:
                    if author == 0:
                        matrix[0][0] += 1
                    else:
                        matrix[0][1] += 1
                else:
                    matrix[1][author] += 1

        # The matrix represents:
        """
        print(f'{word} is not used by author 0 {matrix[0][0]} times')
        print(f'{word} is not used by author 1 {matrix[0][1]} times')
        print(f'{word} is used by author 0 {matrix[1][0]} times')
        print(f'{word} is used by author 1 {matrix[1][1]} times')
        """
        G = calc_entropy(matrix, total_pars) 
        word_gains[word] = G

    return word_gains


# For each paragraph p in the corpus, emit on standard output a comma-separated line:
# paragraph identifier, paragraph class, and the values of the 300 features
def output(words, paragraphs):

    nfeatures = len(words)
    for nov in paragraphs:
        for par in nov:
            vector = list()
            vector.append(par[0])
            vector.append(int(par[1]))
            for w in words:
                if w in par:
                    vector.append(1)
                else:
                    vector.append(0)
            for i, v in enumerate(vector):
                if i <= nfeatures:
                    print(v, end=', ')
                else:
                    print(v, end='\n')


nfeatures = 300
paragraphs = [] # lists of comma-separated: identifier, class and unique words
corpus_words = set() # unique words of novels
word_gains = dict() # calculated 'word':gain of corpus words
features = [] # nfeatures highest-gain words to use as features of paragraphs

# Read novels, label the paragraphs and create dictionary of unique words
for fname in sys.argv[1:]:
    paragraphs.append(label(fname, construct(novel(fname), corpus_words)))

# Calculate and pick best spliting words based on gain
word_gains = calc_gains(corpus_words, paragraphs)
sorted_wg = sorted(word_gains.items(), key=lambda item: item[1], reverse=True)[0:nfeatures]
for w, g in sorted_wg:
    features.append(w)

# Print comma-separated feature vectors with paragraph identifier and class
output(features, paragraphs)
