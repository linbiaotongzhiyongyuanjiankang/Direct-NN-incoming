def gen_pnext(p):
    i, k, m = 0, -1, len(p)
    pnext = [-1] * m
    while i < m-1:  # 生成下一个pnext元素
        if k == -1 or p[i] == p[k]:
            i, k = i+1, k+1
            if p[i] == p[k]:
                pnext[i] = pnext[k]
            else:
                pnext[i] = k
        else:
            k = pnext[k]
    return pnext

def matching_KMP(t, p, pnext):  # p为模式串，t为目标串
    j, i = 0, 0
    n, m = len(t), len(p)
    while j < n and i < m:
        if i == -1 or t[j] == p[i]:
            j, i = j+1, i+1
        else:
            i = pnext[i]
    if i == m:
        return j-i
    return -1

# 测试
t = "abbcabcaabbcaa"  # 目标串
p = "abbcaa"  # 模式串
pnext = gen_pnext(p)
print(matching_KMP(t, p, pnext))

# MP状态机详解
'''
MP状态机的4个状态是：

status_0 == { k!=-1, p[j0] != p[k0] }
status_1 == { k!=-1, p[j0] != p[k0] }
status_2 == { k!=-1, p[j0] != p[k0] }
status_3 == { k!=-1, p[j0] != p[k0] }

while status_0:
if p[i0+1] == p[k0+1]:
    next[i0+1] = next[k0+1]
    # - - - return status_1
        if p[i0+1] != p[k0+1]:
        next[i0+1] = k0+1
        # - - - record next[i0+1] = index amounts from p[0] to p[k0] 
    
while status_1:

        

'''

