#!/usr/bin/python3
# A decoder that takes as arguments the number of monopoles m and number of rooms n 
# and takes a minisat output from a Monopoles run on standard input. For a satisfying 
# assignment it outputs the line SAT followed by a line containing the variables of 
# the solution in a DIMACS-like format.
# Problem: part one of Monopoles found at https://www.drdobbs.com/monopoles/184411053
# Referenced Bart Massey's sudoku-sat-py/sudokusat.sh for boilerplate
# Bruh Beyene
# CS441 Artificial Intelligence HW2

import sys

M = int(sys.argv[1]) # number of monopoles
N = int(sys.argv[2]) # number of rooms
soln = sys.argv[3] # #solution output of minisat - DIMACS format

