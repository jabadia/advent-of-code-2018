a = 0
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

# line 1
b = 1
while b <= f:
    d = 1
    while d <= f:
        if b * d == f:  # if b * d == f goto 7 else goto 8
            a = b + a
        print(a, b, c, d, f)
        d = d + 1
        # if d <= f: # if d > f goto 12 else goto 11
    b = b + 1

print(a, b, c, d, f)
