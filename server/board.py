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
    
    def toggle_flag(self, change_coord:tuple[int,int]):
        self.write(change_coord,change_coord,self.read(change_coord,change_coord,self.flag_list),self.flag_list,filler=False)
    
    def click(self, click_coord:tuple[int,int]) -> int:
        if not self.read(click_coord,click_coord,self.display_list)[0][0] and not self.read(click_coord,click_coord,self.flag_list)[0][0]:
            self.write(click_coord,click_coord,[[True]],self.display_list,filler=False)
            if self.read(click_coord,click_coord,self.bomb_list)[0][0]==1:
                return -1
            else:
                if self.get_cell_num(click_coord)==0:
                    surround=((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
                    for rel_coord in surround:
                        self.click((click_coord[0]+rel_coord[0],click_coord[1]+rel_coord[1]))
                return 0
        return 1
    
    def get_cell_num(self, get_coord:tuple[int,int]) -> int:
        if self.read(get_coord,get_coord,self.bomb_list)==1:
            return -1
        surround=((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1))
        num=0
        for rel_coord in surround:
            a=(get_coord[0]+rel_coord[0],get_coord[1]+rel_coord[1])
            if self.read((a[0],a[1]),(a[0],a[1]),self.bomb_list)[0][0]==1:
                num+=1
        return num
    
    def read(self,start_coord:tuple[int,int],end_coord:tuple[int,int],origin_list:list[list[list[None]]]) -> list[list[int]]:
        if start_coord[0]>end_coord[0] and start_coord[1]>end_coord[1]:
            return [[]]
        print("x:{} y:{}".format(list(range(start_coord[0],end_coord[0]+1)),list(range(start_coord[1],end_coord[1]+1))))
        for i in range(start_coord[0],end_coord[0]+1):
            print("x:{} list:{}".format(i,origin_list[0][i]))
        return [[origin_list[0][x][y] if x>=0 and y>=0 else (origin_list[1][-x-1][y] if x<0 and y>=0 else(origin_list[2][-x-1][-y-1] if x<0 and y<0 else origin_list[3][x][-y-1])) for x in range(start_coord[0],end_coord[0]+1)]for y in range(start_coord[1],end_coord[1]+1)]
    
    def write(self,start_coord:tuple[int,int],end_coord:tuple[int,int],write_list:list[list[int]],dest_list:list[list[list[None]]],filler=0xff) -> int:
        for (x_list,x) in zip(write_list,range(min(start_coord[0],end_coord[0]),max(start_coord[0],end_coord[0])+1)):
            for (elem,y) in zip(x_list,range(min(start_coord[1],end_coord[1]),max(start_coord[1],end_coord[1])+1)):
                if x>=0 and y>=0: #0
                    if len(dest_list[0])>x and len(dest_list[0][x])>y:
                        dest_list[0][x][y]=elem
                    elif len(dest_list[0])<=x and len(dest_list[0][0])>y:
                        for x_ in range(x+1-len(dest_list[0])):
                            dest_list[0].append([filler])
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                    elif len(dest_list[0])>x and len(dest_list[0][x])<=y:
                        for y_ in range(y+1-len(dest_list[0][x])):
                            dest_list[0][x].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                    else:
                        for x_ in range(x+1-len(dest_list[0])):
                            dest_list[0].append([filler])
                        for y_ in range(y+1-len(dest_list[0][x])):
                            dest_list[0][x].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                elif x<0 and y>=0: #1
                    if len(dest_list[1])>-x-1 and len(dest_list[1][-x-1])>y:
                        dest_list[1][-x-1][y]=elem
                    elif len(dest_list[1])<=-x-1 and len(dest_list[1][0])>y:
                        for x_ in range(-x-1+1-len(dest_list[1])):
                            dest_list[1].append([filler])
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)

                    elif len(dest_list[1])>-x-1 and len(dest_list[1][-x-1])<=y:
                        for y_ in range(y+1-len(dest_list[1][-x-1])):
                            dest_list[1][-x-1].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                    else:
                        for x_ in range(-x-1+1-len(dest_list[1])):
                            dest_list[1].append([filler])
                        for y_ in range(y+1-len(dest_list[1][-x-1])):
                            dest_list[1][-x-1].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                elif x<0 and y<0: #2
                    if len(dest_list[2])>-x-1 and len(dest_list[2][-x-1])>-y-1:
                        dest_list[2][-x-1][-y-1]=elem
                    elif len(dest_list[2])<=-x-1 and len(dest_list[2][0])>-y-1:
                        for x_ in range(-x-1+1-len(dest_list[2])):
                            dest_list[2].append([filler])
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)

                    elif len(dest_list[2])>-x-1 and len(dest_list[2][-x-1])<=-y-1:
                        for y_ in range(-y-1+1-len(dest_list[2][-x-1])):
                            dest_list[2][-x-1].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                    else:
                        for x_ in range(-x-1+1-len(dest_list[2])):
                            dest_list[2].append([filler])
                        for y_ in range(-y-1+1-len(dest_list[2][-x-1])):
                            dest_list[2][-x-1].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                else: #3
                    if len(dest_list[3])>x and len(dest_list[3][x])>-y-1:
                        dest_list[3][x][-y-1]=elem
                    elif len(dest_list[3])<=x and len(dest_list[3][0])>-y-1:
                        for x_ in range(x+1-len(dest_list[3])):
                            dest_list[3].append([filler])
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)

                    elif len(dest_list[3])>x and len(dest_list[3][x])<=-y-1:
                        for y_ in range(-y-1+1-len(dest_list[3][x])):
                            dest_list[3][x].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
                    else:
                        for x_ in range(x+1-len(dest_list[3])):
                            dest_list[3].append([filler])
                        for y_ in range(-y-1+1-len(dest_list[3][x])):
                            dest_list[3][x].append(filler)
                        self.write(start_coord=start_coord,end_coord=end_coord,write_list=write_list,dest_list=dest_list,filler=filler)
        return 0
    
    def prepare(self,start_coord:tuple[int,int],end_coord:tuple[int,int]):
        try: 
            self.write(start_coord=start_coord,end_coord=end_coord,write_list=[[0xff for y in range(abs(end_coord[1]-start_coord[1])+1)]for x in range(abs(end_coord[0]-start_coord[0])+1)], dest_list=self.bomb_list)
            self.write(start_coord=start_coord,end_coord=end_coord,write_list=[[False for y in range(abs(end_coord[1]-start_coord[1])+1)]for x in range(abs(end_coord[0]-start_coord[0])+1)], dest_list=self.display_list, filler=False)
            self.write(start_coord=start_coord,end_coord=end_coord,write_list=[[False for y in range(abs(end_coord[1]-start_coord[1])+1)]for x in range(abs(end_coord[0]-start_coord[0])+1)], dest_list=self.flag_list, filler=False)
            return 0
        except:
            return -1
    
    def generate(self,start_coord:tuple[int,int],end_coord:tuple[int,int]):
        pass
