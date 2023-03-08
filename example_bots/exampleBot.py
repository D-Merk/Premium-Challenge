import random
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

while(True):
    width, height = int(input()), int(input())
    map = [ [0]*width for i in range(height)]
    x = str()
    for h in range(int(height)):
        l = input()
        for w in range(width):
            map[h][w] = l[w]

    worm_position = [int(i) for i in input().split(' ')]
    priority, number_players = int(input()), int(input())
    my_position = [int (i) for i in input().split(' ')]
    other_players_positions = list()
    for j in range(int(number_players) - 1):
        s = input().split(' ')
        other_players_positions.append((s[0], [int (i) for i in s[1:]]))
    
    def test_move(move):
        if move == 'n':
            new_position = [my_position[0], my_position[1]-1]
        elif move == 's':
            new_position = [my_position[0], my_position[1]+1]
        elif move == 'e':
            new_position = [my_position[0]+1, my_position[1]]
        elif move == 'w':
            new_position = [my_position[0]-1, my_position[1]]
        else:
            new_position = my_position
        
        # check borders
        if new_position[0]<0 or new_position[1]<0 or new_position[0]>width or new_position[1]>height:
            return False
        
        map_symbol = map[new_position[1]][new_position[0]]
        # check holes
        if map_symbol == 'O':
            return False
        # check worm position
        if new_position==worm_position:
            return False
        
        return True
    
    moves = ['n', 's', 'e', 'w', '.']
    random.shuffle(moves)
    for m in moves:
        if test_move(m):
            print(m)
            break