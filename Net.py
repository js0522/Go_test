import numpy as np
from NeuralNet import NeuralNet
from TrainNet import TrainNet
import torch
from utils import *
import time

args=dotdict({'cuda':torch.cuda.is_available(),
              'num_channels':512,
              'dropout':0.3,
              })


class Net(NeuralNet):
    def __init__(self,game):
        self.self_net=TrainNet(game,args)
        self.board_x,self.board_y=game.getBoardSize()
        self.action_size=game.getActionSize()

        if args.cuda:
            self.self_net.cuda()

    def predict(self, board):
        start= time.time()

        board = torch.FloatTensor(board.astype(np.float64))
        if args.cuda: board = board.contiguous().cuda()
        board = board.view(1, self.board_x, self.board_y)
        self.self_net.eval()
        with torch.no_grad():
            pi, v = self.self_net(board)

        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]