def gen_pnext(p):
    i, k, m = 0, -1, len(p)  # 顺序指针，其集合为自然数；逆序指针，其集合为负数
    pnext = [-1] * m  # -1是初始化值，代表针前串为空集时的pnext值，并要求指针i后移一位;
    while i < m - 1:  # 生成下一个pnext元素，对于长度len(p)的模式串，其最大检测位置是顺序索引为len(p)-1时，此时匹配真子集,也就是现有针前串非全子集的最大索引是(len(p)-1)-1
        if k == -1 or p[i] == p[k]:  # 假设主串主指针在p[i]处失配,模式串副指针在p[k]且k!=-1，此时认为模式串中的 p[0]~p[k-1]== p[i-k]~p[i-1]
            i, k = i + 1, k + 1
            if p[i] == p[k]:
                pnext[i] = pnext[k]  # 若p[i]=p[k],意味着p[0]~p[k-1]+p[k]== p[j-k]~p[j-1]+p[i],指针在p[i+1]处的k[i+1]值是k[i]+1
            else:              # 若k=-1,代表此时p[i]之前p[0]~p[k-1]!= p[i-k]~p[i-1],p[i]和p[k]是否相等都导致
                pnext[i] = k  # 若p[i]!=p[k]且k=-1,此时默认的是p[0]~p[k-1]!= p[i-k]~p[i-1]成立，在p[i+1]处的k[i+1]值是k[i]+1=0
        else:   # k!=-1且p[i]!=p[k],p[0]~p[k-1]== p[j-k]~p[j-1]，k[k]=k
            k = pnext[k]
    return pnext


def matching_KMP(t, p, pnext):  # p为模式串，t为目标串
    j, i = 0, 0
    n, m = len(t), len(p)
    while j < n and i < m:
        if i == -1 or t[j] == p[i]:
            j, i = j + 1, i + 1
        else:
            i = pnext[i]
    if i == m:
        return j - i
    return -1


# 测试
t = "abbcabcaabbaabaafcaa"  # 目标串
p = "abaabcac"  # 模式串
pnext = gen_pnext(p)
print(matching_KMP(t, p, pnext), pnext)
