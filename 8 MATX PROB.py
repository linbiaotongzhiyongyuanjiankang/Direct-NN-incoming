import torch
import numpy as np

bigpod = np.vstack(np.linspace(0, 7, 8))
pod = np.vstack(np.linspace(0, 7, 8))


for epoch in range(7):
    pod = torch.from_numpy(pod).int()
    pod = torch.add(pod, 8)
    bigpod = np.column_stack((bigpod, pod))
    pod = pod.numpy()

bigpod = torch.from_numpy(bigpod).int().transpose(0, 1)

print(bigpod)

print(bigpod.shape)

