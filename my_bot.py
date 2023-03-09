import sys

def eprint(*args, **kwargs):
    print(*args,file=sys.stderr, **kwargs)

class Brain:
    def __init__(self,game):
        self.game = game
        self.middle_reach = False #This will be helpful late :)

    def update_game(self, game):
        self.game = game

    def test_move(self, move):
        if move == 'n':
            new_position = [self.game.my_pos_x, self.game.my_pos_y-1]
        elif move == 's':
            new_position = [self.game.my_pos_x, self.game.my_pos_y+1]
        elif move == 'e':
            new_position = [self.game.my_pos_x+1, self.game.my_pos_y]
        elif move == 'w':
            new_position = [self.game.my_pos_x-1, self.game.my_pos_y]
        else:
            new_position = [self.game.my_pos_x, self.game.my_pos_y]

        # check borders
        if new_position[0]<0 or new_position[1]<0 or new_position[0]>self.game.width or new_position[1]>self.game.height:
            return False

        map_symbol = self.game.map[new_position[1]][new_position[0]]
        # check holes
        if map_symbol == 'O':
            return False

        # check worm position
        for i in self.game.enemy_pos:
            if new_position == i[1]:
                self.stranger_danger(i)
        return True
    
    def stranger_danger(self,enemy_pos):
        if enemy_pos[0] == 'W':
            #TODO: FUCKING RUN
            pass
        #TODO: ANALYZE BULLSHIT
        pass

    #------------------- PARTE QUE O RUI METEU ---------------------------#
    class Point:
        def __init__(self,x: int, y: int):
            self.x = x
            self.y = y
 
    # A data structure for queue used in BFS
    class queueNode:
        def __init__(self,pt: Point, dist: int):
            self.pt = pt  # The coordinates of the cell
            self.dist = dist  # Cell's distance from the source
    
    # Check whether given cell(row,col)
    # is a valid cell or not
    def isValid(row: int, col: int):
        return (row >= 0) and (row < 11) and (col >= 0) and (col < 11)
    
    # These arrays are used to get row and column
    # numbers of 4 neighbours of a given cell
    rowNum = [-1, 0, 0, 1]
    colNum = [0, -1, 1, 0]

    def middle_algorithm(mat, src: Point, dest: Point):
        # check source and destination cell
        # of the matrix have value 1
        if mat[src.x][src.y]!=1 or mat[dest.x][dest.y]!=1:
            return -1
        
        visited = [[False for i in range(11)]
                        for j in range(11)]
        
        # Mark the source cell as visited
        visited[src.x][src.y] = True
        
        # Create a queue for BFS
        q = deque()
        
        # Distance of source cell is 0
        s = queueNode(src,0)
        q.append(s) #  Enqueue source cell
        
        # Do a BFS starting from source cell
        while q:
    
            curr = q.popleft() # Dequeue the front cell
            
            # If we have reached the destination cell,
            # we are done
            pt = curr.pt
            if pt.x == dest.x and pt.y == dest.y:
                return curr.dist
            
            # Otherwise enqueue its adjacent cells
            for i in range(4):
                row = pt.x + rowNum[i]
                col = pt.y + colNum[i]
                
                # if adjacent cell is valid, has path 
                # and not visited yet, enqueue it.
                if (isValid(row,col) and
                mat[row][col] == 1 and
                    not visited[row][col]):
                    visited[row][col] = True
                    Adjcell = queueNode(Point(row,col),
                                        curr.dist+1)
                    q.append(Adjcell)
        
        # Return -1 if destination cannot be reached
        return -1
    #-------------------FIM DA PARTE QUE O RUI METEU ---------------------#
    
    
    #Counterbalance between safety and points
    #Ou alphabeta etc...
    def min_max(self):
        pass

class Game:
    #TODO: Turn Board into matrix

    def __init__(self):
        #Map variables
        self.width = -1
        self.height = -1
        self.map = []
        self.moves = ['n', 's', 'e', 'w', '.']
        #My variables
        self.priority = -1
        self.my_pos_x = -1
        self.my_pos_y = -1
        #Enemy variables
        self.n_enemies = -1
        self.enemy_pos = []

    def update_state(self, width, height, map, priority, pos, n_players, enemy_pos):
        self.width = width
        self.height = height
        self.map = map
        self.priority = priority + 1
        self.n_enemies = n_players #Enemies plus worm
        self.my_pos_x, self.my_pos_y = pos
        self.enemy_pos = enemy_pos

    def __str__(self):
        return "map:% s priority:% s enemies:% s pos_x:% s pos_y:% s enemies:% s" % (self.map, self.priority, self.n_enemies, self.my_pos_x, self.my_pos_y, self.enemy_pos)
        



def main():
    game = Game()
    big_brain = Brain()
    turn = 0
    for i in range(1):
        width, height = int(input()), int(input())
        map = [ [0]*width for i in range(height)]
        for h in range(int(height)):
            l = input()
            for w in range(width):
                map[h][w] = l[w]

        worm_position = [int(i) for i in input().split(' ')]
        if turn == 0:
            #TODO: Put middle postion
            pass

        priority, number_players = int(input()), int(input())
        my_position = [int (i) for i in input().split(' ')]
        enemy_pos = list()
        enemy_pos.append(('W', worm_position))

        for j in range(int(number_players) - 1):
            s = input().split(' ')
            enemy_pos.append((s[0], [int (i) for i in s[1:]]))

        game.update_state(width, height, map, 
                          priority, my_position, number_players, 
                          enemy_pos)
        big_brain.update_game(game)
        if(big_brain.middle_reach == False):
            big_brain.middle_algorithm()





        turn +=1

if __name__ == '__main__':
    main()


