import numpy as np
import copy

m = []


def pailie(arr, posnow, end):  # posnow是当前下标指针指向的位置，是当前待敲定的元
    if posnow == end:
        global m
        m.append(arr[:])
    else:
        for index in range(posnow, end):  # posnow可用的元的下标范围是[posnow， indexfinal]，已经被敲定的元不参与敲定
            arr[index], arr[posnow] = arr[posnow], arr[index]  # 当前的敲定分支
            pailie(arr, posnow + 1, end)  # 下一位的敲定分支，循环引用敲定函数
            arr[index], arr[posnow] = arr[posnow], arr[index]  # 从最后一层向上逐级逆序操作，还原到交换前的状态


def card(a, b, c, d):
    res = [a, b, c, d]
    vlu = copy.copy(res)
    vlu.sort()
    arr = vlu
    pailie(arr, 0, len(arr))
    su = a + b + c + d
    p = divmod(su, 5)
    p = p[1]

    cord = []
    for t in res:
        cord.append(vlu.index(t))

    tok = []
    for i in range(5):  # 最终余数 0,1,2,3,4 对应的 k 列表，最终余数 i =（k+p） mod 5
        if i - p > 0 or i - p == 0:
            tok = tok + [(i - p)]
        else:
            tok = tok + [(5 + i - p)]

    for tk in tok:
        fs = tok.index(tk)
        idv = m.index(res)
        goal = tk + 5 * idv
        if goal < vlu[0] and fs == 0:
            return goal, m, vlu
        else:
            if vlu[0] < goal < vlu[1] and fs == 1:
                return goal, m, idv
            else:
                if vlu[1] < goal < vlu[2] and fs == 2:
                    return goal, m, idv
                else:
                    if vlu[2] < goal < vlu[3] and fs == 3:
                        return goal, m, idv
                    else:
                        if vlu[3] < goal and fs == 4:
                            return goal, m, idv


toke = card(18, 19, 24, 8)
print(toke)
