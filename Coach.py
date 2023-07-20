import numpy as np
from MCTS import MCTS
import logging
from collections import deque
from tqdm import tqdm
import os
from pickle import Pickler, Unpickler


log=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
class Coach():

    def __init__(self,game,self_net,args):
        self.game=game
        self.self_net=self_net
        self.oppo_net=self.self_net.__class__(self.game)
        self.args=args
        self.mcts = MCTS(self.game, self.self_net, self.args)
        self.trainExampleHistory=[]
        self.skipFirstSelfPlay=False
        
    def learn(self):

        for i in range(1,self.args.numIters+1):
            log.info(f'Starting Iter #{i}...')
            if not self.skipFirstSelfPlay or i>1:
                iterationTrainExamples = deque([],maxlen=self.args.maxlenOfQueue)

                for _ in tqdm(range(self.args.numEps), desc="Self Play"):
                    self.mcts = MCTS(self.game, self.self_net, self.args)
                    iterationTrainExamples+=self.executeEpisode()

                self.trainExampleHistory.append(iterationTrainExamples)

            if len(self.trainExampleHistory) > self.args.numItersForTrainExamplesHistory:
                log.warning(f"remove oldest entry")
                self.trainExampleHistory.pop(0)

            self.saveTranExamples(i-1)    
    
    
    def executeEpisode(self):
        trainExamples=[]
        board=self.game.getInitBoard()
        self.curPlayer=1
        episodeStep=0

        while True:
            episodeStep+=1
            canonicalBoard=self.game.getCanonicalForm(board,self.curPlayer)
            temp=int(episodeStep<self.args.tempThreshold)

            pi = self.mcts.getActionProb(canonicalBoard, temp=temp)
            
            sym = self.game.getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, self.curPlayer, p, None])

            action = np.random.choice(len(pi),p=pi)

            board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)

            r = self.game.getGameEnded(board, self.curPlayer)


            if r != 0:
                return [(x[0], x[2], r * ((-1) ** (x[1] != self.curPlayer))) for x in trainExamples]
            if episodeStep > self.args.depth:
                winner=self.game.EndArea(board,1)
                return [(x[0], x[2], winner * ((-1) ** (x[1] != self.curPlayer))) for x in trainExamples]
            


    def saveTrainExamples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.getCheckpointFile(iteration) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        f.closed