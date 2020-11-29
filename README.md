### CS441 - Bruh Beyene - HW3 - Author Identification by Machine Learning 
This module builds booleanized instances for identifying novels written by different authors such that its output is an arg for Bart Massey's machine learner modules: nbayes.py, knn.py and id3.py. The output is lines of comma-separated feature vectors including a paragraph identifier and author class.

### to run it

`./features.py [ novels ... ] > instances

where novels might be any/all ...
> `../hw-authors/austen-northanger-abbey.txt,`
> `../hw-authors/austen-pride-and-prejudice.txt,`
> `../hw-authors/shelley-frankenstein.txt,`
> `../hw-authors/shelley-the-last-man.txt`

I followed the steps in the assignment description. First, I read the words of each paragraph from the four novels into memory as a list of lists of paragraphs per author. I used the cleaned up novels in Bart's `hw-authors/` corpus which discards names, headers and front/back matter. From those, features.py keeps or removes words based on some criteria, converts each paragraph to be the set of unique words present in the paragraph, then labels it with a unique paragraph identifier and the author class (1 = Shelley, 0 = Austen). It constructs a dictionary of words and maps each word to a gain by calculating the entropy of splitting paragraphs on the word. I the sort and select the 300 highest-gain words to use as features of a paragraph.

I fed my output CSV file of booleanized instances as input to Bart's three machine learners at `http://github.com/pdx-cs-ai/psamlearn`. With my first configuration of keeping/omitting certain types of words, the `ID3` learner had a `76 percent` accuracy and now `81 percent` with 10-way cross-validation. The other learners weren't great with `k-nearest-neighbor` and 'naive-bayes` in the mid-60's. The instructions and hints from the assignment description were easy to follow but the entropy equations were not so until I understood them - I used word count or a random number for the gains to check my data-structures were working properly. I then replaced it with the gain calculations.

It took me a while to realize I could be using a matrix to count how many times a word is/isn't used by author 0/1 because entropy is calculated by splitting the instances on a word then calculating the probabilities of each authors' usage. I didn't calculate the initial entropy of the instances so the word gains are (-1 < G < 0) where 0 is least entropy. There are 16,995 filtered unique words and all have G < -0.9. With 300 features selected, the most used words were "could" and "would"; the highest gain word was "our". In an unfiltered example, the word "mr" had the best with 0.87 but I think titles would make it too easy for the learner so they were omitted.

Bart's `hw-authors/` already had cleaned up the novels and this module cleans up a bit more. I experimented with different counts `nfeatures`, word filtering `construct()` as well as Bart's other learners and had the best accuracy when titles were kept, and increasing the feature count had deminishing returns. It was several days of work, lots of fun and practice. It takes a couple of minutes to get the instances output - I could have done these steps with fewer passes over the lists but this worked better for testing. What is left is to import more novels by Austen, Shelley and others to test different filters and learners, and experiment with the learners' code.
