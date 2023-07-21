from Board import Board
import numpy as np
b=Board(3)
board=np.array([[1,-1,0],[0,-1,0],[0,0,0]])
b.pieces=np.copy(board)
a=b.countArea(1)
a= 1
a -1