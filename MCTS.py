import math
import numpy as np
import logging

log=logging.getLogger(__name__)

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
            depth=0
            self.search(canonicalBoard,depth)

        s=self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(self.game.getActionSize())]
        
        if temp==0:
            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)
            probs[bestA] = 1
            return probs
        
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        probs = [x / counts_sum for x in counts]
        return probs
        

    def search(self, canonicalBoard, depth):
        depth+=1
        if(depth>self.args.depth):
            return -1

        s = self.game.stringRepresentation(canonicalBoard)
        
        if s not in self.Es:
            #print(self.game.getGameEnded(canonicalBoard,1))
            self.Es[s]=self.game.getGameEnded(canonicalBoard,1)
        
        if self.Es[s] != 0: # game not ended
            return -self.Es[s]
        
        if s not in self.Ps: # no Policy for current state
            self.Ps[s],v = self.self_net.predict(canonicalBoard)
            valid_moves=self.game.getValidMoves(canonicalBoard, 1)
            self.Ps[s] = self.Ps[s] * valid_moves

            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s
            else:
                log.error("All valid moves were masked. Try other way")
                self.Ps[s]=self.Ps[s]+valid_moves
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s]=valid_moves
            self.Ns[s]=0
            return -v
        
        valid_moves = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        for a in range(self.game.getActionSize()):
            if valid_moves[a]:
                if (s,a) in self.Qsa:
                    u=self.Qsa[(s,a)] +self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    u=self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s])

                if u>cur_best:
                    cur_best=u
                    best_act=a
        
        a=best_act
        next_s, next_player=self.game.getNextState(canonicalBoard,1,a)
        next_s = self.game.getCanonicalForm(next_s, next_player)

        v = self.search(next_s,depth)

        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)] * self.Qsa[(s,a)] +v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s,a)] += 1

        else:
            self.Qsa[(s,a)]=v
            self.Nsa[(s,a)]=1

        self.Ns[s] += 1
        return -v
