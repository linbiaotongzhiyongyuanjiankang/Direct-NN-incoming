import copy as copy

def skf(pan, root):
    index_record = []
    for i in range(0, len(root)):
        temp = []
        for j in range(0, len(pan)):  # append 带有广播性质
            if pan[j] == root[i]:
                temp.append(j)

            if j + 1 == len(pan):
                index_record = index_record + [temp]
                # 遍历到pan最后一个元才记录进index_record, 注意这个判断是独立的
                # #（若意外缩进该 /index if块/ 至 /比对if块/ 内，当 比对条件为False时 则会被视作 /比对if块/ 的执行块而被连带不执行导致出错）
    return index_record

def sep(sep, skf_record):
    sep_record = []
    for i in range(0,len(skf_record)):
        temp = skf_record[i]
        for j in range(0,len(temp)):
            temp[j] = list(divmod(temp[j], sep))
        sep_record = sep_record + [temp]
    return sep_record

def check( former_two, former_one, current):
    a = (former_one[0] - former_two[0])
    b = (former_one[1] - former_two[1])
    c = (current[0] - former_one[0])
    d = (current[1] - former_one[1])
    if a == 0 or b == 0:
        if c == 0 or d == 0:
            if (a * c) - (b * d) == 0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def possi_route(route_data, step):
    big_record = []
    if step + 1 == len(route_data):
        temp = route_data[step]
        for i in range(0, len(temp)):
            current = temp[i]
