import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt


def intext(pan, root, index_record):
    for i in range(0, len(root)):
        temp = []
        for j in range(0, len(pan)):  # append 带有广播性质
            if pan[j] == root[i]:
                temp.append(j)

            if j + 1 == len(pan):    # 遍历到pan最后一个元才记录进index_record, 注意这个判断是独立的（若意外缩进该 /index if块/ 至 /比对if块/ 内，当 比对条件为False时 则会被视作 /比对if块/ 的执行块而被连带不执行导致出错）
                index_record = index_record + [temp]

    return index_record


pan = '111AAAB111'
root = 'ABA'
index_record = []
print(intext(pan, root, index_record))
