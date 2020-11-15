#!/usr/bin/python3
# An encoder that takes as arguments the number of monopoles m and number of rooms n 
# and produces an encoding of the m, n Monopoles problem as a propositional SAT formula 
# in Conjunctive Normal form (CNF) using DIMACS format on its standard output.
# Problem: part one of Monopoles found at https://www.drdobbs.com/monopoles/184411053
# Referenced Bart Massey's sudoku-sat-py/sudoku-gen.py for boilerplate
# Bruh Beyene
# CS441 Artificial Intelligence HW2

from sys import argv

M = int(argv[1]) # number of monopoles
N = int(argv[2]) # number of rooms

# Given M monopoles and N rooms, return the atom
# corresponding to L[m][n]
def L(m, n):
        return M * n + m + 1

# Adds variables to list of CNF
# Borrowed from Bart Massey's sudokugen.py
def clause(c):
    clauses.append(c)

clauses = []

# Each monopole is placed in a room
for m in range(M):
    clause([L(m, n) for n in range(N)])

# No monopole is in two rooms
# Taken from Bart Massey's class demo - previous version had an edge case I had neglected
for m in range(M):
    for n1 in range(N):
        for n2 in range(n1+1, N):
                clause([-L(m, n1), -L(m, n2)])

# No sum of two monopoles is in a room with both of its summands
for n in range(N):
    for m1 in range(M):
        for m2 in range(m1):
            if m1 != m2 and m1 + m2 + 2 <= M:
                x = m1 + 1
                y = m2 + 1
                z = x + y
                clause([-L(x-1, n), -L(y-1, n), -L(z-1, n)])

# Emit the problem description
# Taken from Bart Massey's sudokugen.py
print("c", "generated by monosat")
print("p", "cnf", M*N, len(clauses))
for c in clauses:
    for l in c:
        print(l, "", end="")
    print("0") 
