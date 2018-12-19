a = 1
b = 0
c = 0
d = 0
f = 0

# line 17
f = f + 2
f = f * f
f = 19 * f
f = f * 11
c = c + 1
c = c * 22
c = c + 6
f = f + c

if a != 0:
    c = 27
    c = c * 28
    c = c + 29
    c = c * 30
    c = c * 14
    c = c * 32
    f = f + c
    a = 0

# sum all divisors of f
a = 0
for b in range(1, f+1):
    if f % b == 0:
        a += b
print(a)
