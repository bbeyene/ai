## CS441 - HW3 - Author Identification by Machine Learning 
This module builds booleanized instances for identifying novels written by different authors such that its output is an arg for Bart Massey's machine learner modules: nbayes.py, knn.py and id3.py. The output is lines of comma-separated feature vectors including a paragraph identifier and author class.

### to run it

`./features.py [ novels ... ] > instances`

where novels might be any/all ...
> ../hw-authors/austen-northanger-abbey.txt, 
> ../hw-authors/austen-pride-and-prejudice.txt, 
> ../hw-authors/shelley-frankenstein.txt, 
> ../hw-authors/shelley-the-last-man.txt

I followed the steps in the assignment description. First, I read the words of each paragraph from the four novels into memory as a list of lists of paragraphs per author. I used the cleaned up novels in Bart's `hw-authors/` corpus which discards names, headers and front/back matter. From those, features.py keeps or removes words based on some criteria, converts each paragraph to be the set of unique words present in the paragraph, then labels it with a unique paragraph identifier and the author class (1 = Shelley, 0 = Austen). It constructs a dictionary of words and maps each word to a gain by calculating the entropy of splitting paragraphs on the word. I the sort and select the 300 highest-gain words to use as features of a paragraph.

I fed my output CSV file of booleanized instances as input to Bart's three machine learners at `http://github.com/pdx-cs-ai/psamlearn`. With my first configuration of omitting words less than 2, 3 and 4 letters, the `ID3` learner with 10 way cross validation had accuracies in the mid-high 70's but when I kept them it had `81 percent` accuracy. The other learners weren't great with `k-nearest-neighbor` and `naive-bayes` in the mid-60's. The instructions and hints from the assignment description were easy to follow but the entropy equations were not so until I understood them - I used word count or a random number for the gains to check my data-structures were working properly. I then replaced it with the gain calculations.

It took me a while to realize I could be using a matrix to count how many times a word is/isn't used by author 0/1 because entropy is calculated by splitting the instances on a word then calculating the probabilities of each authors' usage. I didn't calculate the initial entropy of the instances so the word gains are (-1 < G < 0) where 0 is least entropy. There are 17,014 filtered unique words and all have G < -0.877. The highest gain word was "my". In an unfiltered example, the word "mr" had the best with 0.87 but I think titles would make it too easy for the learner so they were omitted.

Bart's corpus already had cleaned up the novels and this module cleans up a bit more. I experimented with different counts `nfeatures`, word filtering `construct()` as well as Bart's other learners and had the best accuracy when titles were kept, and increasing the feature count had deminishing returns. It was several days of work, lots of fun and practice. It takes about half a minute to get the instances output - I could have done these steps with fewer passes over the lists but this worked better for testing. What is left is to import more novels by Austen, Shelley and others to test different filters and learners, and experiment with the learners' code.

## CS441 - HW 2 - Monopoles via SAT

### encoder:
`./monosat.py m n > encoded_prob`

### minisat:
`minisat encoded_prob encoded_soln`

### decoder:
`./unmonosat.py m n < encoded_soln`

The formal encoding of Monopoles had three parts:

(A) `forall i in {1..m} . exists j in {1..n} . i in S[j]`
(B) `forall i in {1..m} . forall j, k in {1..n} . j ≠ k → i not in S[j] or i not in S[k]`
(C) `forall i in {1..n} . forall j, k in {1..m} . j ≠ k → j not in S[i] or k not in S[i] or j + k not in S[i]`

I started by studying and using Bart Massey's sudoku-sat-py and its boilerplate then following the hints, I ground out the problem with SAT atoms for `M = 4` and `N = 2`, and found boolean assignments that satisfy if and only if true for monopoles being located in room n: `L[m][n])`:

- L(1,1) = 1; L(2,1) = 2; L(3,1) = 3; L(4,1) = 4;
- L(1,2) = 5; L(2,2) = 6; L(3,2) = 7; L(4,2) = 8;

... where,
(A) is satisfied by (1 v 5) ^ (2 v 6) ^ (3 v 7) ^ (4 v 8)
(B) is satisfied by (~1 v ~5) ^ (~2 v ~6) ^ (~3 v ~7) ^ (~4 v ~8)
(C) is satisfied by - (~1 v ~2 v ~3) ^ (~1 v ~3 v ~4) ^ (~5 v ~6 v ~7) ^ (~5 v ~7 v ~8)

(C) was the most difficult to program as I was doubling up on clauses or getting off-by-one bugs but I eventually found a way by looping on a subset instead of all of M in the inner loop and by calculating the sums with the offset before using the 'location' function.

Minisat's output for this instance was `1 2 -3 -4 -5 -6 7 8`. 

To decode it, I keep the `true` (positive) values `1 2 7 8` then reverse the L function for `(m,n)` pairs: `(1, 0) (2, 0) (3, 1) (4, 1)` giving monopoles 1 and 2 are in the first, and 3 and 4 are in the second.

When M = 53 and N = 4, dfs took several minutes whereas minisat takes 10's of milliseconds. Awesome!

Update: new (B) clauses generator fixed edge case bug where M = 2, N = 1 was UNSAT thanks to peeking at Bart's code during class.

## CS441 - HW1 - Monopoles

Run:
`./monodfs m n`


A complete depth-first search that attempts to place m monopoles (1…m) into n rooms, where no pairs add to equal another in the same room, e.g. if (1, 2) were in room 1, then (3) must be in another room.

I started by studying Bart Massey's 'Sliding Tile Puzzle Solver' which has a dfs solver. But here, no stop list because no state can be revisited while traversing possibilites. The following was scribbled on paper before I understood the problem ...

> while current != m
>	depth = 0
>	room = 0
>	if compatible
>>		place current
>>		current++
>>		depth++
>>		room++

... which isn't correct at all but it showed me that I should be tracking and traversing the state of the room configuration and not the rooms themselves. As I drew out the tree, I saw that the depth was the monopole count. Then, if n = 2 and m = 3, the first, second and fourth of the possible configurations are compatible ...

- at depth 1: [ 1 ][ - ] , [ - ][ 1 ]
- at depth 2: [ 1,2 ][ - ] , [ - ][ 1,2 ] , [ 1 ][ 2 ]
- at depth 3: [ 1,3 ][ 2 ] , [ 1 ][ 2,3 ] , [ 1,2,3 ][ - ] , [ 1,2 ][ 3 ]

... so, the dfs stack became the rooms selected while the depth was the current monopole count. When all of the rooms were exhausted with no branch having a solution, it removes the room from the stack and tries the next rooms of the branch above.

What is left is seeing how to increase performance especially for m > 52 (and n = 4).