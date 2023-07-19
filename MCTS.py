import math
import numpy as np

class MCTS():
    def __init__(self, game, self_net, args):
        self.game=game
        self.self_net=self_net
        self.args=args
        
        self.Qsa = {}  # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}  # stores #times edge s,a was visited
        self.Ns = {}  # stores #times board s was visited
        self.Ps = {}  # stores initial policy (returned by neural net)

        self.Es = {}  # stores game.getGameEnded ended for board s
        self.Vs = {}  # stores game.getValidMoves for board s

    def getActionProb(self, canonicalBoard, temp=1):
        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)

        s=self.game.stringRepresentation(canonicalBoard)
        probs = [0.11] * 9
        return probs

    def search(self, canonicalBoard):

        s = self.game.stringRepresentation(canonicalBoard)
        
        if s not in self.Es:
            print(self.game.getGameEnded(canonicalBoard,1))
            self.Es[s]=self.game.getGameEnded(canonicalBoard,1)