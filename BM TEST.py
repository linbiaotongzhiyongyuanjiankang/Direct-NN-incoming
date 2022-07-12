def gen_pnext(p):
    i, k, m = 0, -1, len(p)
    pnext = [-1] * m    # 初始化为-1的值
    while i < m-1:  # 指针从0号位开始直到(m-2)号位，因为生成的序列对应的是指针的后一位，所以最大的指针号是(m-2)
        if k == -1 or p[i] == p[k]: #
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
t = "abbcabcaaaaaaacaa"  # 目标串
p = "aadsrgaabaa"  # 模式串
pnext = gen_pnext(p)
print(matching_KMP(t, p, pnext), pnext)

#