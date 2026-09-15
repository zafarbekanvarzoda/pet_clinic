import torch
from torch.utils.data import Dataset, random_split


class MyDataset(Dataset):
    def __init__(self):
        self.x = torch.tensor([1, 2, 3, 4, 5])
        self.y = torch.tensor([2, 4, 6, 8, 10])

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return len(self.x)


dataset = MyDataset()

train_dataset, test_dataset = random_split(
    dataset,
    [4, 1]
)

print("Train size:", len(train_dataset))
print("Test size:", len(test_dataset))

print("Train:")
for item in train_dataset:
    print(item)

print("Test:")
for item in test_dataset:
    print(item)