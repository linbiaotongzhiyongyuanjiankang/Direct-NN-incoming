import sys as sys

sys.setrecursionlimit(1000)

def skf(pan, root):
    index_record = []
    for i in range(0, len(root)):
        temp = []
        for j in range(0, len(pan)):
            if pan[j] == root[i]:
                temp.append(j)
            if j + 1 == len(pan):
                index_record = index_record + [temp]
    return index_record


def sep(sep, skf_record):
    sep_record = []
    for i in range(0,len(skf_record)):
        temp = skf_record[i]
        for j in range(0,len(temp)):
            temp[j] = list(divmod(temp[j], sep))
        sep_record = sep_record + [temp]
    return sep_record


def check(forward_two, forward_one, current):
    a = (forward_one[0] - forward_two[0])
    b = (forward_one[1] - forward_two[1])
    c = (current[0] - forward_one[0])
    d = (current[1] - forward_one[1])
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


def possi_route(data, step, record):

    big_record = []

    if len(data) < 3:
        return False

    if step + 3 < len(data) or step + 3 == len(data):
        step_plus_one = data[step + 1]
        step_plus_two = data[step + 2]
        step_temp = data[step]

        if step + 1 > len(data):
            return big_record

        elif step + 3 == len(data) and step != 0 and step != 1:
            forward_set = record[-1]
            forward_two = forward_set[-2]
            forward_one = forward_set[-1]
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                if check(forward_two, forward_one, current):
                    for j in range(0, len(step_plus_one)):
                        next_one = step_plus_one[j]
                        if check(forward_one, next_one, current):
                            for k in range(0, len(step_plus_two)):
                                next_two = step_plus_two[k]
                                if check(next_two, next_one, current):
                                    big_record.append([current]+[next_one]+[next_two])

        elif step + 2 == len(data) and step != 0 and step != 1:
            forward_set = record[-1]
            forward_two = forward_set[-2]
            forward_one = forward_set[-1]
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                if check(forward_two, forward_one, current):
                    for j in range(0, len(step_plus_one)):
                        next_one = step_plus_one[j]
                        if check(forward_one, next_one, current):
                            big_record.append([current] + [next_one])

        elif step + 1 == len(data) and step != 0 and step != 1:
            forward_set = record[-1]
            forward_two = forward_set[-2]
            forward_one = forward_set[-1]
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                if check(forward_two, forward_one, current):
                    big_record.append([current])

        elif step == 0:
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                for forward in possi_route(data, step + 3, record + [current]):
                    big_record.append(forward + [current])

        elif step == 1:
            forward_set = record[-1]
            forward_one = forward_set[-1]
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                for j in range(0, len(step_plus_one)):
                    next_one = step_plus_one[j]
                    if check(forward_one, next_one, current):
                        for forward in possi_route(data, step + 3, record + [current]):
                            big_record.append(forward + [current])

        else:
            forward_set = record[-1]
            forward_two = forward_set[-2]
            forward_one = forward_set[-1]
            for i in range(0, len(step_temp)):
                current = step_temp[i]
                if check(forward_two, forward_one, current):
                    for j in range(0, len(step_plus_one)):
                        next_one = step_plus_one[j]
                        if check(forward_one, next_one, current):
                            for k in range(0, len(step_plus_two)):
                                next_two = step_plus_two[k]
                                if check(next_two, next_one, current):
                                    for forward in possi_route(data, step + 3, record + [current] + [next_one] + [next_two]):
                                        big_record.append(forward + [current] + [next_one] + [next_two])
    return big_record



'''
  for r in range(0, len(next_two)):
                forward_two = temp[r]
                current_set = big_record[-1]
                current = current_set[-2]
                forward_one = current_set[-1]
'''

'''
             for r in range(0, len(next_two)):
                current = next_two[r]
                for s in range(0, len(next_one)):
                    forward_one = next_one[s]
                    for t in range(0, len(temp)):
                        forward_two = temp[t]
'''

'''
[current] + [forward_one] + [forward_two]
big_record.append([current] + [next_one] + [next_two])
'''