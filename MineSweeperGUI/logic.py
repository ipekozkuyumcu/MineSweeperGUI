class Cell():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = 0
        self.f = False
        
    def make_bomb(self):
        self.val = -1

    def calculate_val(self, board):
        # try catch for every if is needeed
        if self.val == 0:
            try:
                if len(board) > self.x+1 and board[self.x+1][self.y].val == -1:
                    self.val +=1
            except:
                pass        
            try:
                if self.x-1 >= 0 and board[self.x-1][self.y].val == -1:
                    self.val +=1
            except:
                pass 
            try:
                if len(board) > self.y+1 and board[self.x][self.y+1].val== -1:
                    self.val +=1
            except:
                pass
            try:
                if self.y-1 >= 0 and board[self.x][self.y-1].val== -1:
                    self.val +=1
            except:
                pass        
            try:
                if self.x-1 >= 0 and self.y-1 >= 0 and board[self.x-1][self.y-1].val==-1:
                    self.val +=1
            except:
                pass
            try:
                if self.y-1 >= 0 and len(board) > self.y+1 and board[self.x+1][self.y-1].val==-1:
                    self.val +=1 
            except:
                pass
            try:
                if len(board) > self.x+1 and len(board) > self.y+1 and board[self.x+1][self.y+1].val==-1:
                    self.val +=1  
            except:
                pass
            try:
                if self.x-1 >= 0 and len(board) > self.y+1 and board[self.x-1][self.y+1].val==-1:
                    self.val +=1
            except:
                pass
        
        
    def __str__(self):
        return ""+str(self.x)+",  "+str(self.y)+", val:"+str(self.val)
