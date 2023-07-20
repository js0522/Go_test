class Board():
    def __init__(self,n):
        self.n=n
        self.pieces=[None]*self.n
        for i in range(self.n):
            self.pieces[i]=[0]*self.n

    def __getitem__(self, index):
        return self.pieces[index]
    
    def countArea(self, color):

        count=0
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==color:
                    count += 1
                if self[x][y]==-color:
                    count -= 1
                if self[x][y]==0:
                    num = self.check_surround((x,y),color)
                    if num>0:
                        count +=1
                    if num<0:
                        count -=1
            return count
        
    def check_surround(self, position, color):
        x,y=position
        right=(x,y+1)
        left=(x,y-1)
        up=(x-1,y)
        down=(x+1,y)
        num=0
        num+=self.check_surround_piece(up,color)
        num+=self.check_surround_piece(down,color)
        num+=self.check_surround_piece(left,color)
        num+=self.check_surround_piece(right,color)
        return num

    def check_surround_piece(self, position, color):
        x,y=position
        if(x<0 or x>=self.n):
            return 0
        if(y<0 or y>=self.n):
            return 0
        if(self[x][y]==-color):
            return -1
        if(self[x][y]==0):
            return 0
        if(self[x][y]==color):
            return 1

    def get_legal_moves(self, color):
        
        moves=set()
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    move=[(x,y)]
                    moves.update(move)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    return True
        return False
        
    def execute_move(self, move, color):
        
        x,y=move
        self.pieces[x][y]=color
        right=(x,y+1)
        left=(x,y-1)
        up=(x-1,y)
        down=(x+1,y)

        self.update_opponent(move,color)
        #self.update_self(move,color)

    def update_opponent(self,move,color):

        x,y=move
        right=(x,y+1)
        left=(x,y-1)
        up=(x-1,y)
        down=(x+1,y)
        
        self.history=[]
        qi=self.check_qi_oppo(right,-color)
        if(qi==0):
            self.chi_history()

        self.history=[]
        qi=self.check_qi_oppo(left,-color)
        if(qi==0):
            self.chi_history()

        self.history=[]
        qi=self.check_qi_oppo(up,-color)
        if(qi==0):
            self.chi_history()

        self.history=[]
        qi=self.check_qi_oppo(down,-color)
        if(qi==0):
            self.chi_history()

        self.history=[]
        self.history.append(move)
        qi=0
        qi+=self.check_qi_self(right,color)
        qi+=self.check_qi_self(left,color)
        qi+=self.check_qi_self(up,color)
        qi+=self.check_qi_self(down,color)

        if(qi==0):
            self.chi_history()

        

    def check_qi_self(self,position,player):
        x,y=position
        if(x<0 or x>=self.n):
            return 0
        if(y<0 or y>=self.n):
            return 0
        if(self[x][y]==-player):
            return 0
        if(self[x][y]==0):
            return 1
        if(self[x][y]==player):
            if(position not in self.history):
                self.history.append(position)
                right=(x,y+1)
                left=(x,y-1)
                up=(x-1,y)
                down=(x+1,y)
                qi=0
                qi+=self.check_qi_oppo(right,player)
                qi+=self.check_qi_oppo(left,player)
                qi+=self.check_qi_oppo(up,player)
                qi+=self.check_qi_oppo(down,player)
                return qi
            else:
                return 0

    def check_qi_oppo(self,position,player):
        x,y=position
        if(x<0 or x>=self.n):
            return 0
        if(y<0 or y>=self.n):
            return 0
        if(self[x][y]==-player):
            return 0
        if(self[x][y]==0):
            return 1
        if(self[x][y]==player):
            if(position not in self.history):
                self.history.append(position)
                right=(x,y+1)
                left=(x,y-1)
                up=(x-1,y)
                down=(x+1,y)
                qi=0
                qi+=self.check_qi_oppo(right,player)
                qi+=self.check_qi_oppo(left,player)
                qi+=self.check_qi_oppo(up,player)
                qi+=self.check_qi_oppo(down,player)
                return qi
            else:
                return 0
        
    def chi_history(self):
        for position in self.history:
            x,y=position
            self[x][y]=0
        self.history=[]    
        



