
import os, sys

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

def clean(novel):
    # Strip away leading and trailing punctuation and remove internal punctuation
    # Words of one letter should probably be ignored
    # The set of unique words present in the paragraph
    discard = {'—', 'a', 'i', '', 'lady', 'lord', 'madam', 'madame', 'miss' 'mr', 'mrs', 'sir', 'the'}
    pars = list()
    for paragraph in novel:
        allwords = set()
        for sentence in paragraph:
            words = sentence.replace('--', ' ').split()
            justwords = {alphas(w) for w in words}
            allwords |= justwords
            allwords -= discard
        if allwords is not None and len(allwords) > 0:
            pars.append(allwords)

    return pars

# Labeled with a unique paragraph identifier and the author class (1 = Shelley, 0 = Austen).
def label(fname, novel):
    labeled = list()
    split_fname = fname.split()
    identifier = label.join('-')[0:-1]
    if split_fname[0] == 'shelley':
        label = 1
    if split_fname[0] == 'austin':
        label = 0
    
    for i, paragraph in enumerate(novel):
        par = list()
        par.append(f'{identifier}.{i}, {label}') 
            
                

# Calculate the information gain of splitting the paragraphs on w using the equations above. 
def calc_gain(word, paragraphs):
    pass

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
words = set() # all words in novels (unique)
word_gain = {} # calculated "word":gain
nfeatures = 300
features = [] # the nfeatures highest-gain words to use as features of the paragraph
labeled_paragraphs = [] # a comma-separated line consisting of the paragraph identifier, the paragraph class, and the values of the 300 features

for fname in sys.argv[1:]:
    original = read_novel(fname)
    novels.append(original)
    cleaned = clean(original)
    cleaned_novels.append(cleaned)
    labeled = label(cleaned)
    labeled_paragraphs.append(labeled)

    # label(clean(read_novel(fname)))

"""
for novel in novels_paragraphs
    for paragraph in novel
        words |= novels_paragraphs[novel][paragraph]

for w in words
    for novel in novels_paragraphs
        for paragraph in novel
            gain = calc_gain(word, paragraph)
            word_gain[word] = gain

features = best_nfeatures(nfeatures, word_gain)

for novel in novels_paragraps
    for paragraph in novel
        paragraph_id = paragraph[0]
        paragraph_class = paragraph[1]
        labeled_feature_vectors.append(paragraph_id, paragraph_class)
        for word in word_gain.keys()
            if word not in paragraph
                labeled_feature_vectors.append(0)
            else
                labeled_feature_vectors.append(1)
                
output(labeled_feature_vectors)
"""
