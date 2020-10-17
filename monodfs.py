#!/usr/bin/python3
# Solution for part one of Monopoles found at https://www.drdobbs.com/monopoles/184411053
# Bruh Beyene
# CS441 Artificial Intelligence HW1
import sys

# A list of lists (rooms of monopoles) with dfs solver
class Monopoles(object):
    def __init__(self, m, n):
        self.m = m 
        self.n = n
        self.rooms = [[] for i in range(n)]

    # Checks if a number can belong in a room
    # True if X + Y doesn't equal candidate
    def compatible(self, mono, room):
        for i in self.rooms[room]:
            for j in self.rooms[room]:
                if (i + j) == mono:
                    if i != j:
                        return False 
        return True

    # With help from Bart Massey's code at https://github.com/pdx-cs-ai/slider
    # Difference being no state saving because a state cannot be reached more than once
    # A monopole is placed at each turn therefore mono == depth
    def dfs(self, mono):
        mono = mono + 1
        if mono > self.m:
            # The last monopole was placed compatibly -> done
            return []

        # List of rooms a monople is allowed in given a room's current monopoles
        possible = [i for i in range(self.n) if self.compatible(mono, i)]

        # Try the monopole in each room
        for i in possible:
            self.rooms[i].append(mono)
            # Add to room and keep deepening until the last monopole is sat
            soln = self.dfs(mono)
            if soln != None:
                return [i] + soln
            # Not sat so remove from room to try another
            self.rooms[i].pop()

        # not satisfied in any rooms
        return None

    # The soln is a list of rooms picked in order (e.g. [0,2,1] means that
    # monopole 1 is in first room, 2 is in third room and 3 is in second room)
    def show(self, soln):
        print("")
        if soln == None:
            print("unsat")
        else:
            for i in range(self.n):
                row = ""
                for j in range(len(self.rooms[i])):
                    row += str(self.rooms[i][j]) + " "
                print(row)
        print("")

    # solve using dfs starting with monopole 0
    def solve(self):
        soln = self.dfs(0)
        self.show(soln)

# m: number of monopoles
# n: number of rooms
m = int(sys.argv[1])
n = int(sys.argv[2])

monopoles = Monopoles(int(m), int(n))
monopoles.solve()
