import argparse

class Monopoles(object):
    def __init__(self, m, n):
        self.m = m 
        self.n = n
        self.rooms = [[] for i in range(n)]

    def compatible(self, mono, room):
        for i in self.rooms[room]:
            for j in self.rooms[room]:
                if (i + j) == mono:
                    if i != j:
                        return False 
        return True

    def dfs(self, mono, room):
        print(self.rooms)
        mono = mono + 1
        if mono > self.m:
            return True

        if not self.compatible(mono, room):
            return False

        for room in range(self.n):
            placement = self.dfs(mono, room)
            if placement:
                self.rooms[room].append(mono)

        return False

    def solve(self):
        if self.dfs(0, 0):
            return True

parser = argparse.ArgumentParser(description='Monopoles Sover.')
parser.add_argument('-m', type=int, help='monopoles')
parser.add_argument('-n', type=int, help='rooms')
args = parser.parse_args()

monopoles = Monopoles(args.m, args.n)
if monopoles.solve():
    print("solved")
