def check(col_record, col_now):
    row_now = len(col_record)
    for rows in range(row_now):
        if abs(col_record[rows] - col_now) in (abs(rows - row_now), 0):
            return False
    return True


def queen(queens, step, col_record):
    bigrecord = []
    rowcolmax = queens
    if step == queens - 1:
        for col_now in range(rowcolmax):
            if check(col_record, col_now) == True:
                bigrecord.append([col_now])
    else:
        for col_now in range(rowcolmax):
            if check(col_record, col_now) == True:
                for forward in queen(queens, step + 1, col_record + [col_now]):
                    bigrecord.append(forward + [col_now])
    return bigrecord


queens = 12
alpha = queen(queens, 0, [])

print(len(alpha))
