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

    def dfs(self, mono):
        mono = mono + 1
        if mono > self.m:
            print("solved")
            return []

        possible = [i for i in range(self.n) if self.compatible(mono, i)]

        for i in possible:
            self.rooms[i].append(mono)
            soln = self.dfs(mono)
            if soln != None:
                return [i] + soln
            self.rooms[i].pop()

        return None

    def solve(self):
        soln = self.dfs(0)
        if soln != None:
            print(soln)

parser = argparse.ArgumentParser(description='Monopoles Sover.')
parser.add_argument('-m', type=int, help='monopoles')
parser.add_argument('-n', type=int, help='rooms')
args = parser.parse_args()

monopoles = Monopoles(args.m, args.n)
monopoles.solve()
