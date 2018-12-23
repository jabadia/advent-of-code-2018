seen = set()
prev = None
with open('results.txt', 'r') as f:
    for line in f:
        n = int(line)
        if n in seen:
            print(prev)
            exit()
        seen.add(n)
        prev = n
print('no dups')

