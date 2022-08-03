import numpy as np
import pandas as pd
import torch
import os

def preprocess_input(data):
    features = ["Pclass", "Sex", "Age", "SibSp", "Parch"]
    X = pd.get_dummies(data[features])
    return torch.tensor(np.array(X, dtype=int), dtype=torch.float)

def preprocess_output(data):
    features = ["Survived"]
    X = pd.get_dummies(data[features])
    return torch.tensor(np.array(X, dtype=int), dtype=torch.float)

#for dirname, _, filenames in os.walk('.'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

train_data = pd.read_csv('.\\train.csv')
processed_train_data = preprocess_input(train_data)
y = preprocess_output(train_data)

test_data = pd.read_csv('.\\test.csv')
processed_test_data = preprocess_input(test_data)

xx = torch.unsqueeze(processed_train_data, 0)

print(len(processed_train_data))

# Use the nn package to define our model and loss function.
model = torch.nn.Sequential(
    torch.nn.Linear(5, 1),
    torch.nn.Flatten(0, 1)
)
loss_fn = torch.nn.MSELoss(reduction='sum')

learning_rate = 1e-3

optimizer = torch.optim.RMSprop(model.parameters(), lr=learning_rate)
for t in range(len(processed_train_data)):
    # Forward pass: compute predicted y by passing x to the model.
    y_pred = model(xx)

    # Compute and print loss.
    loss = loss_fn(y_pred, y)
    if t % 100 == 99:
        print(t, loss.item())

    # Before the backward pass, use the optimizer object to zero all of the
    # gradients for the variables it will update (which are the learnable
    # weights of the model). This is because by default, gradients are
    # accumulated in buffers( i.e, not overwritten) whenever .backward()
    # is called. Checkout docs of torch.autograd.backward for more details.
    optimizer.zero_grad()

    # Backward pass: compute gradient of the loss with respect to model
    # parameters
    loss.backward()

    # Calling the step function on an Optimizer makes an update to its
    # parameters
    optimizer.step()













y = train_data["Survived"]

features = ["Pclass", "Sex", "SibSp", "Parch"]
X = pd.get_dummies(train_data[features])
X_test = pd.get_dummies(test_data[features])

model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X, y)
predictions = model.predict(X_test)

output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
output.to_csv('submission.csv', index=False)
print("Your submission was successfully saved!")
