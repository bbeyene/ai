
import os, random, sys

# Read the words of each paragraph from the four novels into memory
def read_novel(fname):
    with open(fname, "r") as f:
        pars = list()
        par = list()
        for line in f:
            words = line.split()
            if not words or words[0] in { "CHAPTER","VOL.","VOLUME","Letter","Chapter",}:
                if par and len(par) > 1:
                    pars.append(par)
                par = list()
                continue
            par.append(line)
        if par and len(par) > 1:
            pars.append(par)

        return pars


def alphas(w): 
        return ''.join([c for c in w if c.lower() >= 'a' and c.lower() <= 'z']).lower()


def clean_construct(novel, corpus_words):
    # Strip away leading and trailing punctuation and remove internal punctuation
    # Words of one letter should probably be ignored
    # The set of unique words present in the paragraph
    discard = {'—', 'a', 'i', 's', '', 'lady', 'lord', 'madam', 'madame', 'miss' 'mr', 'mrs', 'sir', 'the'}
    pars = list()
    for paragraph in novel:
        allwords = set()
        for sentence in paragraph:
            words = sentence.replace('--', ' ').split()
            justwords = {alphas(w) for w in words}
            allwords |= justwords
            allwords -= discard
        if allwords is not None and len(allwords) > 0:
            corpus_words |= allwords
            pars.append(allwords)

    return pars


# Label with a unique paragraph identifier and the author class (1 = Shelley, 0 = Austen).
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


# Calculate the information gain of splitting the paragraphs on w using the equations above. 
def calc_gain(word, paragraphs):
    """
    prNpos = # of paragraphs w is in / number of paragraphs
    prNneg = 1 - prNpos

    U = -(prN * math.log(prN) + (1 - prN) * math.log(1 - prN))
    """
    return random.randint(1, 100)


# Return best
def best_nfeatures(nfeatures, word_gain):
    pass
    # sort_on_gains = word_gain sort on gain
    # top = sort_on_gains[:300]


# For each paragraph p in the corpus, emit on standard output a comma-separated line 
# paragraph identifier, paragraph class, and the values of the 300 features
def output(vectors):
    pass


novels = [] # list of lists: each novel has hundreds of paragraphs
cleaned_novels = [] # list of lists: cleaned paragraphs
corpus_words = set() # all words in novels (unique)
word_gain = dict() # calculated "word":gain
nfeatures = 300
features = [] # the nfeatures highest-gain words to use as features of the paragraph
labeled_paragraphs = [] # a list of lists of comma-separated: paragraph identifier, the paragraph class, and the unique words per paragraph

for fname in sys.argv[1:]:
    novel = read_novel(fname)
    cleaned = clean_construct(novel, corpus_words)
    cleaned_novels.append(cleaned)
    labeled = label(fname, cleaned)
    labeled_paragraphs.append(labeled)

for w in corpus_words:
    for nov in labeled_paragraphs:
        for par in nov:
            word_gain[w] = calc_gain(w, par)

#for w, g in word_gain.items():
#    print(f'{w} = {g}')

sorted_wg = sorted(word_gain.items(), key=lambda item: item[1])
features.append(sorted_wg[0:nfeatures])
print(features)
"""
for nov in labeled_paragraphs:
    for par in nov:
        print(par)
for w in corpus_words:
    print(w)


output(labeled_feature_vectors)
"""
