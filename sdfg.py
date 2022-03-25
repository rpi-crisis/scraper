from itertools import permutations

perms = permutations("BOOKKEEPER")

words10 = set([ ''.join(p) for p in perms ])
words9 = set([ p[:-1] for p in words10 ])
words8 = set([ p[:-1] for p in words9 ])
words7 = set([ p[:-1] for p in words8 ])

print(len(words10), len(words9), len(words8), len(words7))
