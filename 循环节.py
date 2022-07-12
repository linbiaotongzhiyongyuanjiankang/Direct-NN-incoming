def looptail_gen(a):
    looptail = a-int(a)
    loop = str(looptail)
    tail = loop.split('.')[1]
    count = len(tail)
    int_0 = int(a)
    up = (10**count - 1)*int_0 + int(tail)
    under = (10**count - 1)
    print(up,'/', under)



a = 0.36
looptail_gen(a)



