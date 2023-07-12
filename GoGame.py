from Game import Game
from Board import Board
import numpy as np

class GoGame(Game):
    square_content={
        -1:"X",
        +0:"-",
        +1:"O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return GoGame.square_content[piece]
    
    def __init__(self, n):
        self.n=n

    def InitBoard(self):
        self.b=Board(self.n)
        self.board=np.array(self.b.pieces)

    def getBoardSize(self):
        return(self.n, self.n)