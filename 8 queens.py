def queen(col_record, col_current): # record（）是按row记录的，record[行索引值]是该行棋子的col值 ''' 当前行列下子的判断'''
    row_current = len(col_record)  # col表的长度是（表末行索引值+1），正好等于当前行的索引值
    for row in range(row_current):  # range是右开区间，从0到（当前行索引值-1）等于0到前一行索引值
        if abs(col_record[row] - col_current) in (abs(row - row_current), 0):
            return False    # 该语句是一旦有冲突就返回false值，如果再建立一个else分支让某个行列没有冲突就返回true，那么这个函数的返回值就会变来变去直到返回最后一组判断条件对应的布尔值，那就失去了判断意义
    return True


def process(queen_nums, queen_step, col_record):
    res = []
    if queen_step == (queen_nums - 1):
        for col_current in range(queen_nums):
            if queen(col_record, col_current):
                res.append([col_current])  # 又更新了一行col值
    else:
        for col_current in range(queen_nums):
            if queen(col_record, col_current):
                for beyond in process(queen_nums, queen_step + 1, col_record + [col_current]):
                    res.append(beyond + [col_current])
    return res


a = process(8, 0, [])

print(len(a))
