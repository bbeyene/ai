#!/usr/bin/python3
# A decoder that takes as arguments the number of monopoles m and number of rooms n 
# and takes a minisat output from a Monopoles run on standard input. For a satisfying 
# assignment it outputs the line SAT followed by a line containing the variables of 
# the solution in a DIMACS-like format.
# Problem: part one of Monopoles found at https://www.drdobbs.com/monopoles/184411053
# Referenced Bart Massey's sudoku-sat-py/sudokusolve.py
# Bruh Beyene
# CS441 Artificial Intelligence HW2

from sys import argv, stdin

M = int(argv[1]) # number of monopoles
N = int(argv[2]) # number of rooms

# Extract monopole and room number
def locate(s):
    s -= 1
    m = s % M + 1
    n = s // M
    return (m, n)

header = next(stdin).strip()

print()
if header == "SAT":
    # Borrowed from Bart Massey's sudoku-sat-py/sudokusolve.py
    # Discard negatives
    solution = [int(b) for b in next(stdin).split() if int(b) > 0]
    
    rooms = [[] for n in range(N)]

    # Place satisfied monopoles into rooms
    for s in solution:
        (m, n) = locate(s)
        rooms[n].append(m)

    # Print rooms
    for i in range(N):
        row = ""
        for j in range(len(rooms[i])):
            row += str(rooms[i][j]) + " "
        print(row)

elif header == "UNSAT":
    print(header)
else:
    print("invalid solution: not minisat format")
print()

