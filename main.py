from GoGame import GoGame
from utils import *
from Net import Net
from Coach import Coach
import logging
args = dotdict({'numIters':10,
                'numGame':100,
                'maxlenOfQueue':100000,
                'numEps':100,
                'tempThreshold':4,
                'numMCTSSims':25,
                'cpuct': 1,
                'depth':19
                })
log=logging.getLogger(__name__)
log.setLevel(logging.INFO)
def main():
    g=GoGame(3)
    
    RLnet=Net(g)
    
    c=Coach(g,RLnet,args)

    c.learn()

if __name__ =="__main__":
    main()