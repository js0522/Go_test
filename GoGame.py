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

    def getInitBoard(self):
        self.b=Board(self.n)
        return np.array(self.b.pieces)

    def getBoardSize(self):
        return(self.n, self.n)
    
    def getActionSize(self):
        return self.n*self.n
   
    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        return player*board
    
    def stringRepresentation(self, board):
        return board.tostring()
    
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces=np.copy(board)
        if b.has_legal_moves(player):
            return 0
        if b.has_legal_moves(-player):
            return 0
        if b.countArea(player) > 0:
            return 1
        return -1