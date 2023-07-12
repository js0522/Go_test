from GoGame import GoGame
from utils import *
from Net import Net
args = dotdict({'numIter':100,'numGame':100,})

def main():
    g=GoGame(3)
    
    RLnet=Net(g)
    
    


if __name__ =="__main__":
    main()