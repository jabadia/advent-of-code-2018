seen = set()
prev = None
with open('results.txt', 'r') as f:
    for i, line in enumerate(f):
        n = int(line)
        if n in seen:
            print(i, prev)
            exit()
        seen.add(n)
        prev = n
print('no dups')

