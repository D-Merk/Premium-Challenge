import sys
from pprint import pprint

def eprint(*args, **kwargs):
    print(*args,file=sys.stderr, **kwargs)

class Brain:
    def __init__(self,game):
        self.game = game
        self.middle_reach = False #This will be helpful late :)

    def update_game(self, game):
        self.game = game

    def test_move(self, move, pos):
        if move == 'n':
            new_position = [pos[0], pos[1]-1]
        elif move == 's':
            new_position = [pos[0], pos[1]+1]
        elif move == 'e':
            new_position = [pos[0]+1, pos[1]]
        elif move == 'w':
            new_position = [pos[0]-1, pos[1]]
        else:
            new_position = [pos[0], pos[1]]

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
        return False

    def is_visited(self,visited,pos,move):
        match move:
            case 'n':
                return not visited[pos[1]-1][pos[0]]
            case 's':
                return not visited[pos[1]+1][pos[0]]
            case 'e':
                return not visited[pos[1]][pos[0]+1]
            case 'w':
                return not visited[pos[1]][pos[0]-1]

    def middle_algorithm(self):
        queue = []
        moves = [str() for i in range(self.game.height)]
        distance = [0 for i in range(self.game.height)]
        visited = [False for i in range(self.game.height)]
        for i in range(len(distance)):
            distance[i] = [0 for i in range(self.game.width)]
            visited[i] = [False for i in range(self.game.width)]
            moves[i] = [str() for i in range(self.game.width)]
        
        queue.append([self.game.my_pos[0],self.game.my_pos[1]])
        while len(queue) > 0:
            curr_pos = [i for i in queue[0]]
            visited[curr_pos[1]][curr_pos[0]] = True

            if curr_pos[0] == self.game.middle_pos[0] and curr_pos[1] == self.game.middle_pos[1]:
                return moves[curr_pos[1]][curr_pos[0]], distance[curr_pos[1]][curr_pos[0]]
            
            queue = queue[1:]
            if self.game.matrix[curr_pos[1]][curr_pos[0]] < 0:
                continue
            for i in ['n','s','e','w']:
                if self.test_move(i,curr_pos) and self.is_visited(visited,curr_pos,i):
                    match i:
                        case 'n':
                            queue.append([curr_pos[0], curr_pos[1]-1])
                            distance[curr_pos[1]-1][curr_pos[0]] = distance[curr_pos[1]][curr_pos[0]] + 1
                            moves[curr_pos[1]-1][curr_pos[0]] = moves[curr_pos[1]][curr_pos[0]]+'n'

                        case 's':
                            queue.append([curr_pos[0], curr_pos[1]+1])
                            distance[curr_pos[1]+1][curr_pos[0]] = distance[curr_pos[1]][curr_pos[0]] + 1
                            moves[curr_pos[1]+1][curr_pos[0]] = moves[curr_pos[1]][curr_pos[0]]+'s'
                           
                        case 'e':
                            queue.append([curr_pos[0]+1, curr_pos[1]])
                            distance[curr_pos[1]][curr_pos[0]+1] = distance[curr_pos[1]][curr_pos[0]] + 1
                            moves[curr_pos[1]][curr_pos[0]+1] = moves[curr_pos[1]][curr_pos[0]]+ 'e'
                            
                        case 'w':
                            queue.append([curr_pos[0]-1, curr_pos[1]])
                            distance[curr_pos[1]][curr_pos[0]+1] = distance[curr_pos[1]][curr_pos[0]] + 1
                            moves[curr_pos[1]][curr_pos[0]+1] = moves[curr_pos[1]][curr_pos[0]]+'w'
        return -1
                        
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
        self.middle_pos = []
        #My variables
        self.priority = -1
        self.my_pos = []
        #Enemy variables
        self.n_enemies = -1
        self.enemy_pos = []

    def update_state(self, width, height, map, priority, pos, n_players, enemy_pos):
        self.width = width
        self.height = height
        self.map = map
        self.matrix = [ [0]*self.width for i in range(self.height)]
        self.priority = priority + 1
        self.n_enemies = n_players #Enemies plus worm
        self.my_pos = pos
        self.enemy_pos = enemy_pos

    def convert_map(self):
        for h in range(self.height):
            for w in range(self.width):
                match self.map[h][w]:
                    case '.':
                        self.matrix[h][w] = 0
                    case 'O':
                        self.matrix[h][w] = -1
                    case '#':
                        self.matrix[h][w] = 0
                    case '1':
                        self.matrix[h][w] = 1
                    case '2':
                        self.matrix[h][w] = 2
                    case '3':
                        self.matrix[h][w] = 3

    def __str__(self):
        return "map:% s priority:% s enemies:% s pos_x:% s pos_y:% s enemies:% s" % (self.map, self.priority, self.n_enemies, self.my_pos_x, self.my_pos_y, self.enemy_pos)
        



def main():
    game = Game()
    big_brain = Brain(game)
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
            game.middle_pos = [i for i in worm_position]

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
            minpath, min_dist = big_brain.middle_algorithm()
            #Do the play
            print(minpath[0])





        turn +=1

if __name__ == '__main__':
    main()


