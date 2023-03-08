#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0
#define eprintf(...) fprintf (stderr, __VA_ARGS__)

struct position {
    int x;
    int y;
    char id;
} typedef Position;

char moves[] = {'n', 's', 'e', 'w'};

char **map; // map coordinates are y, x
int width, height;

int test_move(char move, Position *my_position, Position *worm){
    int move_x = my_position->x, move_y = my_position->y;
    switch(move) {
        case 'n':
            move_y-=1;
            break;
        case 's':
            move_y+=1;
            break;
        case 'e':
            move_x+=1;
            break;
        case 'w':
            move_x-=1;
            break;
    }

    // check borders
    if (move_x<0 || move_y<0 || move_x>width || move_y>height){
        return FALSE;
    }

    char map_symbol = map[move_y][move_x];
    // check holes
    if (map_symbol == 'O'){
        return FALSE;
    }
    // check worm position
    if (move_x == worm->x && move_y == worm->y){
        return FALSE;
    }

    // good move
    return TRUE;
}

// shuffle moves array
void shuffleMoves() {
    for (int i = 0; i < 3; i++) 
    {
        int j = i + rand() / (RAND_MAX / (4 - i) + 1);
        char t = moves[j];
        moves[j] = moves[i];
        moves[i] = t;
    }
}

int main() {
    int priority;
    int num_players;
    Position worm_position;
    Position my_position;
    Position *players_positions;

    scanf("%d\n", &width);
    scanf("%d\n", &height);

    map = (char **) malloc(sizeof(char *) * height);
    for (int i = 0; i < height; i++) {
        map[i] = (char *)malloc(sizeof(char) * (width + 1));
        scanf("%s\n", map[i]);
    }
    scanf("%d %d\n", &worm_position.x, &worm_position.y);
    
    scanf("%d\n", &priority);
    scanf("%d\n", &num_players);
    players_positions = (Position *) malloc(sizeof(Position) * num_players);

    while (TRUE)
    {
        scanf("%d %d", &my_position.x, &my_position.y);
        for (int i = 0; i < num_players - 1; i++) {
            getchar();
            scanf("%c %d %d", &players_positions[i].id ,&players_positions[i].x, &players_positions[i].y);
        }

        shuffleMoves();
        char move = '.';
        for (int i=0; i<4; i++) {
            move = moves[i];
            if (test_move(move, &my_position, &worm_position)) {
                printf("%c\n", move);
                break;
            }
        }
        fflush(stdout);

        int ans = scanf("%d", &width);
        if (ans == EOF){
            break;
        }
        scanf("%d", &height);
        
        for (int i = 0; i < height; i++) {
            scanf("%s", map[i]);
        }
        scanf("%d %d", &worm_position.x, &worm_position.y);
        scanf("%d", &priority);
        scanf("%d", &num_players);

    }

    return 0;
}
