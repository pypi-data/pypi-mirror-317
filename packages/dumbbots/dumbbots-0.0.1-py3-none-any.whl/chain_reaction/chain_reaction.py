
class Dot():
    def init(self,y,x,player_no, atoms_no):
        self.x = x
        self.y = y
        self.atoms = atoms_no
        self.owner = player_no

    def set_type(self,length, width):
        self.type = 0
        self.neighbour_coords = []
        if (self.x >= 1 and self.y < (length -1)): # bottom left
            self.type += 1
            self.neighbour_coords.append([self.y+1,self.x-1])

        if (self.x < (width -1) and self.y < (length -1)): # bottom right
            self.type += 1
            self.neighbour_coords.append([self.y+1,self.x+1])

        if (self.x < (width -1) and self.y>=1): # top right
            self.type += 1
            self.neighbour_coords.append([self.y-1,self.x+1])

        if (self.y >= 1 and self.x >=1): # top left
            self.type += 1
            self.neighbour_coords.append([self.y-1,self.x-1]) 


class ChainReaction():
    def __init__(self, length, width):
        self.grid_length = length
        self.grid_width = width 
        self.__grid = []  # Made private with double underscore

        # initialize grid
        for j in range(length):
            row = []
            for i in range(width):
                dot = Dot(j,i,0,0)
                dot.set_type(length,width)
                row.append(dot)

            self.__grid.append(row)

    def get_grid(self):
        """Returns the current game state grid"""
        return self.__grid

    def add_dot(self,y,x, player_no):
        if (x >= self.grid_width or y >= self.grid_length): # should not be out of grid
            return
        
        if (self.__grid[y][x].owner != 0 and self.__grid[y][x].owner != player_no): # should not be on other players territory
            return
        
        self.__grid[y][x].atoms += 1
        self.__grid[y][x].owner = player_no

        if(self.__grid[y][x].type == self.__grid[y][x].atoms):
            self.explode(y,x,player_no)
        
    def explode(self,y,x, player_no):
        self.__grid[y][x].atoms = 0
        self.__grid[y][x].owner = 0
        for y1,x1 in self.__grid[y][x].neighbour_coords:
            self.__grid[y1][x1].owner = player_no
            self.__grid[y1][x1].atoms += 1
            if(self.__grid[y1][x1].type == self.__grid[y1][x1].atoms):
                self.explode(y1,x1,player_no)

    def check_game_over(self):
        owner = -1
        for row in self.__grid:
            for dot in row:
                if dot.owner != 0:  # Ignore unoccupied cells
                    if owner == -1:
                        owner = dot.owner
                    elif owner != dot.owner:
                        return -1  # More than one player owns cells
                    
        return owner