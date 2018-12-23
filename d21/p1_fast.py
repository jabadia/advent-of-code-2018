a = 0
ip = 0
e = 123                 #   0
while True:
    e = e & 456             #   1
    if e == 72:
        break

e = 0                   #   5
while True:
    f = e | 65536           #   6
    e = 10704114            #   7
    while True:
        c = f & 255             #   8
        e = e + c               #   9
        e = e & 16777215        #  10
        e = e * 65899           #  11
        e = e & 16777215        #  12

        if 256 > f:
            print(e)
            exit()
        else:
            c = 0                   #  17
            while True:
                d = c + 1               #  18
                d = d * 256             #  19
                if d > f:
                    d = 1
                    f = c  # 26
                    # ip = 7  # 27
                    break
                else:
                    d = 0
                    c = c + 1
