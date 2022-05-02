import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

torch.manual_seed(1)
np.random.seed(1)

epoch_max = 20000
sample_batch = 128
sample_size = 16
sample_pts = 21
goal_batch = sample_pts
judge_batch = 1
hid1 = 256
hid2 = 128
hid3 = 128

dorate_G1 = 0.0001
dorate_G2 = 0.0001
dorate_D = 0.0001

ptspos = np.vstack([np.linspace(-3, 3, sample_pts) for _ in range(sample_batch)])       # (sample-batch,sample_pts)


def pro_art():
    a = np.random.uniform(1, 2, size=sample_batch)[:, np.newaxis] # (sample_barch,1)
    paints = a * np.power(ptspos, 2) - a
    paints = torch.from_numpy(paints).float()
    return paints  # 定义专家数据集


'''
    nn是对张量操作的封装
'''

G1 = nn.Sequential(
    nn.Linear(sample_size, hid1),
    nn.Linear(hid1, hid2)
)

G2 = nn.Sequential(
    nn.Linear(hid2, hid1),
    nn.ReLU(),
    nn.Linear(hid1,goal_batch)
)

D = nn.Sequential(
    nn.Linear(goal_batch, hid3),
    nn.ReLU(),
    nn.Linear(hid3, judge_batch),
    nn.Sigmoid()
)

optimizer_G1 = torch.optim.Adam(G1.parameters(), lr=dorate_G1)
optimizer_G2 = torch.optim.Adam(G2.parameters(), lr=dorate_G2)
optimizer_D = torch.optim.Adam(D.parameters(), lr=dorate_D)

plt.ion()

for epoch in range(0, epoch_max):
    sample_trigger = torch.randn(sample_batch, sample_size)
    G_work = G1(sample_trigger)
    G_work = G2(G_work)# GNN genarator

    pro = pro_art()
    D_pro = D(pro)  # DNN judgement
    D_gwork = D(G_work)

    G_loss = torch.mean(torch.log(1 - D_gwork))
    G_loss = torch.reciprocal(G_loss)   # 逐元素取负一次方
    G_loss = torch.mul(G_loss, -1)
    D_loss = -torch.mean(torch.log(D_pro) + torch.log(1 - D_gwork))
    vD_loss = torch.mean(D_loss)

    optimizer_G2.zero_grad()
    optimizer_G1.zero_grad()
    G_loss.backward(retain_graph=True)
    optimizer_G1.step()
    optimizer_G2.step()

    optimizer_D.zero_grad()
    D_loss.backward()
    optimizer_D.step()

    print("Eopch:{}, Loss:{:.3f}".format(epoch + 1, vD_loss))


    if epoch %200 == 0:    #plt
        plt.cla()
        plt.plot(ptspos[0], G_work.data.numpy()[0], c='#4AD631', lw=3, label='Generated painting', )
        plt.plot(ptspos[0], 2.5 * np.power(ptspos[0], 2) - 2, c='#74BCFF', lw=3, label='upper bound')
        plt.plot(ptspos[0], 0.5 * np.power(ptspos[0], 2) - 1 , c='#FF9359', lw=3, label='lower bound')
        plt.text(-.5, 2.3, 'D accuracy=%.2f (0.5 for D to converge)' % D_pro.data.numpy().mean(),fontdict={'size': 13})
        # plt.text(-.5, 2, 'G_loss= %.2f ' % G_loss.data.numpy(), fontdict={'size': 13})

        plt.ylim((-3, 3))
        plt.legend(loc='upper right', fontsize=10)
        plt.draw()
        plt.pause(0.1)


plt.ioff()
plt.show()