def permutations(arr, position, end):
    if position == end:
        print(arr)
    else:
        for index in range(position, end):
            arr[index], arr[position] = arr[position], arr[index]
            permutations(arr, position + 1, end)
            arr[index], arr[position] = arr[position], arr[index]
            # 还原到交换前的状态，为了进行下一次交换


arr = [0, 1, 6]
permutations(arr, 0, len(arr))

'''
def pailie(arr, posnow, end):   # posnow是当前下标指针指向的位置，是当前待敲定的元
    if position == end:
        print(arr)
    else:
        for index in range(posnow, end):    # posnow可用的元的下标范围是[posnow， indexfinal]，已经被敲定的元不参与敲定
            arr[index], arr[posnow] = arr[posnow], arr[index]   # 当前的敲定分支
            pailie(arr, posnow + 1, end)                        # 下一位的敲定分支，循环引用敲定函数
            arr[index], arr[posnow] = arr[posnow], arr[index]   # 从最后一层向上逐级逆序操作，还原到交换前的状态


arr = [1, 2, 3, 4]
pailie(arr, 0, len(arr))

'''