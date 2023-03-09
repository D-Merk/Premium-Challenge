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

    def middle_algorithm():
        pass
    
    
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


