# 
# Board class for server
# infinite size of board
#     |y-       ----------->
#   2 | 3       |
# ----|----     |
#   1 | 0       |
#     |y+       |
# 0,3 includes x=0
# 0,1 includes y=0
# 


class Board():
    def __init__(self, bomb_rate:float=0.4):
        self.bomb_rate=bomb_rate
        self.clear()
    
    def clear(self):
        self.flag_count=0
        self.bomb_list=[[[0xff for i in range(1)]for j in range(1)]for k in range(4)]          # shape(1,1,4)
        self.display_list=[[[False for i in range(1)]for j in range(1)]for k in range(4)]
        self.flag_list=[[[False for i in range(1)]for j in range(1)]for k in range(4)]
    
    def read(self,start_coord:tuple[int,int],end_coord:tuple[int,int]) -> list[list[int]]:
        if start_coord[0]>end_coord[0] and start_coord[1]>end_coord[1]:
            return [[]]
        return [[self.bomb_list[0][x][y] if x>=0 and y>=0 else (self.bomb_list[1][-x-1][y] if x<0 and y>=0 else(self.bomb_list[2][-x-1][-y-1] if x<0 and y<0 else self.bomb_list[3][x][-y-1])) for x in range(start_coord[0],end_coord[0]+1)]for y in range(start_coord[1],end_coord[1]+1)]
    
    def write(self,start_coord:tuple[int,int],end_coord:tuple[int,int],write_list:list[list[int]]) -> int:
        for (x_list,x) in zip(write_list,range(min(start_coord[0],end_coord[0]),max(start_coord[0],end_coord[0])+1)):
            for (elem,y) in zip(x_list,range(min(start_coord[1],end_coord[1]),max(start_coord[1],end_coord[1])+1)):
                if x>=0 and y>=0: #0
                    if len(self.bomb_list[0])>x and len(self.bomb_list[0][x])>y:
                        self.bomb_list[0][x][y]=elem
                    elif len(self.bomb_list[0])<=x and len(self.bomb_list[0][0])>y:
                        for x_ in range(x+1-len(self.bomb_list[0])):
                            self.bomb_list[0].append([0xff])
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list)
                    elif len(self.bomb_list[0])>x and len(self.bomb_list[0][x])<=y:
                        for y_ in range(y+1-len(self.bomb_list[0][x])):
                            self.bomb_list[0][x].append(0xff)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list)
                    else:
                        for x_ in range(x+1-len(self.bomb_list[0])):
                            self.bomb_list[0].append([0xff])
                        for y_ in range(y+1-len(self.bomb_list[0][x])):
                            self.bomb_list[0][x].append(0xff)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list)
                elif x<0 and y>=0: #1
                    if len(self.bomb_list[1])>-x-1 and len(self.bomb_list[1][-x-1])>y:
                        self.bomb_list[1][-x-1][y]=elem
                    elif len(self.bomb_list[1])<=-x-1 and len(self.bomb_list[1][0])>y:
                        for x_ in range(-x-1+1-len(self.bomb_list[1])):
                            self.bomb_list[1].append([0xff])
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)

                    elif len(self.bomb_list[1])>-x-1 and len(self.bomb_list[1][-x-1])<=y:
                        for y_ in range(y+1-len(self.bomb_list[1][-x-1])):
                            self.bomb_list[1][-x-1].append(0xff)
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)
                    else:
                        for x_ in range(-x-1+1-len(self.bomb_list[1])):
                            self.bomb_list[1].append([0xff])
                        for y_ in range(y+1-len(self.bomb_list[1][-x-1])):
                            self.bomb_list[1][-x-1].append(0xff)
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)
                elif x<0 and y<0: #2
                    if len(self.bomb_list[2])>-x-1 and len(self.bomb_list[2][-x-1])>-y-1:
                        self.bomb_list[2][-x-1][-y-1]=elem
                    elif len(self.bomb_list[2])<=-x-1 and len(self.bomb_list[2][0])>-y-1:
                        for x_ in range(-x-1+1-len(self.bomb_list[2])):
                            self.bomb_list[2].append([0xff])
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)

                    elif len(self.bomb_list[2])>-x-1 and len(self.bomb_list[2][-x-1])<=-y-1:
                        for y_ in range(-y-1+1-len(self.bomb_list[2][-x-1])):
                            self.bomb_list[2][-x-1].append(0xff)
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)
                    else:
                        for x_ in range(-x-1+1-len(self.bomb_list[2])):
                            self.bomb_list[2].append([0xff])
                        for y_ in range(-y-1+1-len(self.bomb_list[2][-x-1])):
                            self.bomb_list[2][-x-1].append(0xff)
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)
                else: #3
                    if len(self.bomb_list[3])>x and len(self.bomb_list[3][x])>-y-1:
                        self.bomb_list[3][x][-y-1]=elem
                    elif len(self.bomb_list[3])<=x and len(self.bomb_list[3][0])>-y-1:
                        for x_ in range(x+1-len(self.bomb_list[3])):
                            self.bomb_list[3].append([0xff])
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)

                    elif len(self.bomb_list[3])>x and len(self.bomb_list[3][x])<=-y-1:
                        for y_ in range(-y-1+1-len(self.bomb_list[3][x])):
                            self.bomb_list[3][x].append(0xff)
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)
                    else:
                        for x_ in range(x+1-len(self.bomb_list[3])):
                            self.bomb_list[3].append([0xff])
                        for y_ in range(-y-1+1-len(self.bomb_list[3][x])):
                            self.bomb_list[3][x].append(0xff)
                        self.write(start_coord=start_coord, end_coord=end_coord, write_list=write_list)
        return 0
    
    def prepare(self,start_coord:tuple[int,int],end_coord:tuple[int,int]):
        try: 
            self.write(start_coord=start_coord,end_coord=end_coord,write_list=[[0xff for y in range(abs(end_coord[1]-start_coord[1])+1)]for x in range(abs(end_coord[0]-start_coord[0])+1)])
            return 0
        except:
            return -1
    
    def generate(self,start_coord:tuple[int,int],end_coord:tuple[int,int]):
        pass