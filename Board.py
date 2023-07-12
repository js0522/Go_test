class Board():
    def __init__(self,n):
        self.n=n
        self.pieces=[None]*self.n
        for i in range(self.n):
            self.pieces[i]=[0]*self.n

    def __getitem__(self, index):
        return self.pieces[index]
    
    