from random import gammavariate
import re
from turtle import forward
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def __str__(self):
        return 'Linear_QNet'

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='linear_model', score=0):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        file_name = file_name + ('_' + str(score) + '.pth')
        torch.save(self.state_dict(), file_name)

    def load(self, file_name=None):
        model_folder_path = './model'
        if file_name is not None:
            file = os.path.join(model_folder_path, file_name)
            if os.path.exists(file):
                torch.load(file)      

class NonLinear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(NonLinear_QNet, self).__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size),
        )
        
    def __str__(self):
        return 'NonLinear_QNet'

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits
    
    def save(self, file_name='nonlinear_model', score=0):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        file_name = file_name + ('_' + str(score) + '.pth')
        torch.save(self.state_dict(), file_name)
    
    def load(self, file_name=None):
        model_folder_path = './model'
        if file_name is not None:
            file = os.path.join(model_folder_path, file_name)
            if os.path.exists(file):
                torch.load(file) 

class QTrainer:
    def __init__(self, model, lr, gamma, device):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.device = device
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float).to(self.device)
        next_state = torch.tensor(next_state, dtype=torch.float).to(self.device)
        action = torch.tensor(action, dtype=torch.long).to(self.device)
        reward = torch.tensor(reward, dtype=torch.float).to(self.device)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0).to(self.device)
            next_state = torch.unsqueeze(next_state, 0).to(self.device)
            action = torch.unsqueeze(action, 0).to(self.device)
            reward = torch.unsqueeze(reward, 0).to(self.device)
            done = (done, )
        
        # 1: predicted Q values with current state
        pred = self.model(state)

        # 2: Q_new = r + gamma * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action).item()] = Q_new

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()

