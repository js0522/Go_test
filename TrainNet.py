import torch
import argparse
from utils import *
class TrainNet(torch.nn.Module):
    def __init__(self, game, args):
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        super(TrainNet, self).__init__()
        self.conv1= torch.nn.Conv2d(1, args.num_channels, 3, stride=1, padding=1)
        self.conv2= torch.nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1, padding=1)
        self.conv3= torch.nn.Conv2d(args.num_channels, args.num_channels, 3, stride=1)

        self.bn1 = torch.nn.BatchNorm2d(args.num_channels)
        self.bn2 = torch.nn.BatchNorm2d(args.num_channels)
        self.bn3 = torch.nn.BatchNorm2d(args.num_channels)

        self.fc1=torch.nn.Linear(args.num_channels*(self.board_x-2)*(self.board_y-2), 1024)
        self.fc_bn1 = torch.nn.BatchNorm1d(1024)

        self.fc2 = torch.nn.Linear(1024, 512)
        self.fc_bn2 = torch.nn.BatchNorm1d(512)

        self.fc3 = torch.nn.Linear(512, self.action_size)

        self.fc4 = torch.nn.Linear(512, 1)

    def forward(self, s):

        s = s.view(-1, 1, self.board_x, self.board_y)               
        s = torch.nn.functional.relu(self.bn1(self.conv1(s)))                          
        s = torch.nn.functional.relu(self.bn2(self.conv2(s)))                          
        s = torch.nn.functional.relu(self.bn3(self.conv3(s)))                          
                        
        s = s.view(-1, self.args.num_channels*(self.board_x-2)*(self.board_y-2))

        s = torch.nn.functional.dropout(torch.nn.functional.relu(self.fc_bn1(self.fc1(s))), p=self.args.dropout, training=self.training)  
        s = torch.nn.functional.dropout(torch.nn.functional.relu(self.fc_bn2(self.fc2(s))), p=self.args.dropout, training=self.training)  

        pi = self.fc3(s)                                                                         
        v = self.fc4(s)                                                                          

        return torch.nn.functional.log_softmax(pi, dim=1), torch.tanh(v)