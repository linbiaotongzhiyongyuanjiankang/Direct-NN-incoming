import numpy as np
import torch
import torch.nn as nn

torch.manual_seed(1)
np.random.seed(5)

epoch_max = 64
sample_batch = 64
sample_size = 16
sample_pts = 16
goal_batch = sample_pts
judge_batch = 1
hid1 = 128
hid2 = 64
hid3 = 32
dorate_G = 0.000025
dorate_D = 0.000025

ptspos = np.vstack([np.linspace(-5, 5, sample_pts) for _ in range(sample_batch)])       # (sample-batch,sample_pts)


def pro_art():
    a = np.random.uniform(1, 3, size=sample_batch)[:, np.newaxis]
    paints = a * np.power(ptspos, 2) - a
    paints = torch.from_numpy(paints).float()
    return paints  # 定义专家数据集


'''
    nn是对张量操作的封装
'''

G = nn.Sequential(
    nn.Linear(sample_size, hid1),
    nn.ReLU(),
    nn.Linear(hid1, goal_batch)
)

D = nn.Sequential(
    nn.Linear(goal_batch, hid3),
    nn.ReLU(),
    nn.Linear(hid3, judge_batch),
    nn.Sigmoid()
)

optimizer_G = torch.optim.Adam(G.parameters(), lr=dorate_G)
optimizer_D = torch.optim.Adam(D.parameters(), lr=dorate_D)

for epoch in range(0, epoch_max):
    sample_trigger = torch.randn(sample_batch, sample_size)
    G_work = G(sample_trigger)  # GNN genarator

    pro = pro_art()
    D_pro = D(pro)  # DNN judgement
    D_gwork = D(G_work)

    G_loss = torch.mean(torch.log(1. - D_gwork)).pow(-1)
    D_loss = -torch.mean(torch.log(D_pro) + torch.log(1 - D_gwork))
    vD_loss = torch.mean(D_loss)

    optimizer_G.zero_grad()
    G_loss.backward(retain_graph=True)
    optimizer_G.step()

    optimizer_D.zero_grad()
    D_loss.backward()
    optimizer_D.step()

    print("Eopch:{}, Loss:{:.3f}".format(epoch + 1, vD_loss))
