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
        return self.n*self.n+1
   
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
    
    def EndArea(self, board, player):
        b = Board(self.n)
        b.pieces=np.copy(board)
        if b.countArea(player) > 0:
            return 1
        return -1

    def getNextState(self, board, player, action):
        if action == self.n*self.n:
            return (board, -player)
        
        b=Board(self.n)
        b.pieces = np.copy(board)
        move=(int(action/self.n), action%self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)
    
    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        
        valids[-1]=1
        if len(legalMoves)!=0:   
            for x, y in legalMoves:
                valids[self.n*x+y]=1
        return np.array(valids)
    
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l