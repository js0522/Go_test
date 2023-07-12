import numpy as np
from NeuralNet import NeuralNet
from TrainNet import TrainNet
import torch
from utils import *

args=dotdict({'cuda':torch.cuda.is_available(),
              'num_channels':512,
              })


class Net(NeuralNet):
    def __init__(self,game):
        self.nnet=TrainNet(game,args)
        self.board_x,self.board_y=game.getBoardSize()
        self.action_size=game.getActionSize()

        if args.cuda:
            self.nnet.cuda()