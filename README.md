## HW 2 - Monopoles via SAT
### Bruh Beyene

### encoder:
`./monosat m n > encoded_prob`

### minisat:
`minisat encoded_prob encoded_soln`

### decoder:
`./unmonosat m n < encoded_soln`

The formal encoding of Monopoles had three parts:

- (A) `forall i in {1..m} . exists j in {1..n} . i in S[j]`
- (B) `forall i in {1..m} . forall j, k in {1..n} . j ≠ k → i not in S[j] or i not in S[k]`
- (C) `forall i in {1..n} . forall j, k in {1..m} . j ≠ k → j not in S[i] or k not in S[i] or j + k not in S[i]`

I started by studying and using Bart Massey's sudoku-sat-py and its boilerplate then following the hints, I ground out the problem with SAT atoms for `M = 4` and `N = 2`, and found boolean assignments that satisfy if and only if true for monopoles being located in room n: `L[m][n])`:

- L(1,1) = 1; L(2,1) = 2; L(3,1) = 3; L(4,1) = 4;
- L(1,2) = 5; L(2,2) = 6; L(3,2) = 7; L(4,2) = 8;

... where,
- (1 v 5) ^ (2 v 6) ^ (3 v 7) ^ (4 v 8) satisfies (A)
- (~1 v ~5) ^ (~2 v ~6) ^ (~3 v ~7) ^ (~4 v ~8) satisfies (B)
- (~1 v ~2 v ~2) ^ (~1 v ~3 v ~4) ^ (~5 v ~6 v ~7) ^ (~5 v ~7 v ~8) satisfies (C)

(C) was the most difficult to program as I was doubling up on clauses or getting off-by-one bugs but I eventually found a way by looping on a subset instead of all of M in the inner loop and by calculating the sums with the offset before using the 'location' function.

Minisat's output for this instance was `1 2 -3 -4 -5 -6 7 8`. 

To decode it, I keep the `true` (positive) values `1 2 7 8` then reverse the L function for `(m,n)` pairs: `(1, 0) (2, 0) (3, 1) (4, 1)` giving monopoles 1 and 2 are in the first, and 3 and 4 are in the second.

When M = 53 and N = 4, dfs took several minutes whereas minisat takes 10's of milliseconds. Awesome!


