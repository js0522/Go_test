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
                    count += self.check_surround((x,y))
            return count
        
    def check_surround(self, position):
        x,y=position
        up=(x,y+1)
        down=(x,y-1)
        left=(x-1,y)
        right=(x+1,y)
        if(x==0):
            a,b=right
            return self[a][b]
        if(x==self.n-1):
            a,b=left
            return self[a][b]
        

    def get_legal_moves(self, color):
        
        moves=set()
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    check=self.is_move_legal(color,(x,y))
                    if (check==True):
                        move=[(x,y)]
                        moves.update(move)
        return list(moves)

    def has_legal_moves(self, color):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    check=self.is_move_legal(color,(x,y))
                    if (check==True):
                        return True
        return False

    def is_move_legal(self, color, position):
        self.qi=[]
        self.qi.append(position)
        self.history=[]
        self.check_qi(color,position)
        if(len(self.qi)>1):
            return True
        else:
            if(self.is_chi(color,position)):
                return True
            return False




    def is_chi(self, color, position):
        
        
        x,y=position
        if((x<0 or x>=self.n) or (y<0 or y>=self.n)):
            return False
        up=(x,y+1)
        down=(x,y-1)
        left=(x-1,y)
        right=(x+1,y)

        self.qi=[]
        self.history=[]
        self.check_qi(-color,up)
        if (position not in self.qi):
            self.qi.append(position)
        if(len(self.qi)==1):
            return True
        self.qi=[]
        self.history=[]
        self.check_qi(-color,down)
        if (position not in self.qi):
            self.qi.append(position)
        if(len(self.qi)==1):
            return True
        self.qi=[]
        self.history=[]
        self.check_qi(-color,left)
        if (position not in self.qi):
            self.qi.append(position)
        if(len(self.qi)==1):
            return True
        self.qi=[]
        self.history=[]
        self.check_qi(-color,right)
        if (position not in self.qi):
            self.qi.append(position)
        if(len(self.qi)==1):
            return True
        
        return False

    
    def check_qi(self,color,position):
        x,y=position
        
        if((x<0 or x>=self.n) or (y<0 or y>=self.n)):
            return
        if(position in self.history):
            return
        if(self[x][y]==-color):
            return
        if(self[x][y]==0):
            if(position not in self.qi):
                self.qi.append(position)
                return
        
        up=(x,y+1)
        down=(x,y-1)
        left=(x-1,y)
        right=(x+1,y)

        self.history.append(position)
        self.check_qi(color,up)
        self.check_qi(color,down)
        self.check_qi(color,left)
        self.check_qi(color,right)
        
    def execute_move(self, move, color):
        x,y=move
        up=(x,y+1)
        down=(x,y-1)
        left=(x-1,y)
        right=(x+1,y)

        if (self.is_chi(color,up)):
            for a,b in self.history:
                self.pieces[a][b]=0
        if (self.is_chi(color,down)):
            for a,b in self.history:
                self.pieces[a][b]=0
        if (self.is_chi(color,left)):
            for a,b in self.history:
                self.pieces[a][b]=0
        if (self.is_chi(color,right)):
            for a,b in self.history:
                self.pieces[a][b]=0
        
        self.pieces[x][y]=color

