import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from database import SessionLocal
from models import User


db = SessionLocal()

users = db.query(User).all()


def parse_address(address):
    parts = address.split()

    zip_code = parts[-1]
    state = parts[-2]

    return zip_code, state


states = [parse_address(user.address)[1] for user in users]
unique_states = sorted(set(states))

state_to_index = {
    state: i
    for i, state in enumerate(unique_states)
}

index_to_state = {
    i: state
    for i, state in enumerate(unique_states)
}

num_classes = len(unique_states)
print("Number of classes:", num_classes)


X = []
y = []

for user in users:
    zip_code, state = parse_address(user.address)

    X.append(float(zip_code) / 100000)
    y.append(state_to_index[state])

db.close()


class PetDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, index):
        return self.X[index].unsqueeze(0), self.y[index]


dataset = PetDataset(X, y)


train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size

train_dataset, test_dataset = random_split(
    dataset,
    [train_size, test_size]
)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


class StateModel(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.linear = nn.Linear(1, num_classes)

    def forward(self, x):
        return self.linear(x)


model = StateModel(num_classes)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)


for epoch in range(10):
    total_loss = 0.0
    num_batches = 0

    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        output = model(X_batch)
        loss = loss_fn(output, y_batch)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        num_batches += 1

    avg_loss = total_loss / num_batches
    print("Epoch:", epoch + 1, "Avg loss:", round(avg_loss, 3))



def evaluate(model, loader):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for X_batch, y_batch in loader:
            output = model(X_batch)
            predicted = output.argmax(dim=1)

            correct += (predicted == y_batch).sum().item()
            total += y_batch.size(0)

    model.train()
    return correct / total



train_accuracy = evaluate(model, train_loader)
test_accuracy = evaluate(model, test_loader)

print("Train accuracy:", round(train_accuracy, 5))
print("Test accuracy:", round(test_accuracy, 5))
print("Random-guess baseline:", round(1 / num_classes, 3), f"(1 / {num_classes} classes)")


def predict_state(zip_code):
    x = torch.tensor([[float(zip_code) / 100000]])

    model.eval()
    with torch.no_grad():
        output = model(x)
    model.train()

    predicted_class = output.argmax(dim=1).item()
    return index_to_state[predicted_class]


new_zip = 34627
predicted_state = predict_state(new_zip)
print("ZIP", new_zip, "-> predicted state:", predicted_state)