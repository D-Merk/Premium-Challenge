# Sandbox

## Index

1. [ Overview ](#overview)
2. [ APIs ](#apis)
3. [ How to Run Sandbox ](#how-to-run-sandbox)
4. [ Rules ](#rules)
4. [ Examples ](#examples)

## Overview

The Sandbox is an auxiliary software of the **Spice Hunters** game used for testing before submiting.

You can use it to test your Bot vs pre-programmed bots with multiplie choosable difficulties and in different maps.

It can also be use to understand the rules by manually playing the game.

## APIs

Your bot's process is expected to run through the entire game, continuously reading new game states and outputting the movement it chooses to play.

### Input

In the begging of each round your bot will receive a string with the following format:

```
<map_width>
<map_height>
<line_1_Map>
<line_2_Map>
...
<line_<height>_Map>
<worm_X> <worm_Y>
<your_priority>
<number_of_alive_players>
<your_X> <your_Y>
(<other_player_id> <other_player_X> <other_player_Y>)*
```

Explanation for each line can be found at the end of the document, in the [rules section](#rules)

### Ouput

After receiving the, described above, input, your bot is expected to output a character corresponding to a possible movement.

A bot can only make a move per round. The available movements are **"nwse."**, *north*, *west*, *south*, *east* and *stay* respectively.

Another output will be considered as *stay*.

If your bot takes more then 10 seconds to answer, its move that round will be considered as *stay*.

## How to run Sandbox

Download it and extract

The command:

> `mkfifo /tmp/pipe` 

will create the pipe that will serve as the connection between the sandbox and your bot

Running the sandbox and your bot:

> `java -jar <path/to/sandbox.jar> [flags*] < /tmp/pipe | <compiled/code/of/your/bot> > /tmp/pipe`

This commands first create the pipe, then run the sandbox with the following flags:

- pretty map

- chooses the map 1

- two Bots with the 1 difficulty

- one Bot with the 2 difficulty

Then it runs the example bot

Available languages:
- Java
- Python
- C

**Warning:** If at the end of the game your bot sends an exception, its not a problem in the actual game. 

### Java

**WARNING:** If you are using java as your language of choice, your class and file **must** both be named *"Solution"*. Once again the Sandbox will not show error, but the actual game will.

#### Example

```
mkfifo /tmp/pipe

java -jar ./sandbox.jar -p -c1 -d1 -d1 -d2 < /tmp/pipe | java example_bots/Solution.java  > /tmp/pipe
```

### Python

#### Example

```
mkfifo /tmp/pipe

java -jar ./sandbox.jar -p -c1 -d1 -d2 -d1 < /tmp/pipe | python3 ./example_bots/exampleBot.py > /tmp/pipe
```

### C

#### Example

```
mkfifo /tmp/pipe

gcc -o exampleBot ./example_bots/exampleBot.c

java -jar ./sandbox.jar -p -c1 -d1 -d2 -d1 < /tmp/pipe | ./exampleBot > /tmp/pipe
```

### Manual Play

If you wish to test the game and don't worry about coding your bot you can use the flag: **"-m"**

Running the sandbox for manual play:

> `java -jar <path/to/sandbox.jar> -m`

In this mode the expected outputs are **"wasd"**, *north*, *west*, *south* and *east* respectively. Any other will be considered as *stay*.

### Available flags

| Flag (short form) | Flag (long form) | Arguments | Usage |
|:---:|:---:|:---:|:---|
| **-h** | --help | *None* | Help
| **-l** | --list | *None* | Lists all available maps (Will not run a game)
| **-b** | --bot-play | *None* | Run a game of only pre-programmed bots
| **-i** | --interval | Number of milliseconds *(Default: 0)* | The game will pause between each round
| **-c** | --choose-map | Number of the intended map *(Default: 0)* | The game will happen in the chosen map
| **-d** | --difficulty | Number of the intended difficulty *(Default: 0)* | Set the difficulty for each bot individually
| **-m** | --manual-play | *None* | [ manual play ](#manual-play)
| **-n** | --number-bots | Number of the intended players *(Default: 4)* | Set the number of players for the game *(between 3 and 4, inclusively)*
| **-p** | --pretty-map | *None* | A more readable version of the map will be printed to the stderr

## Rules

**Goal:** code a bot to win a tournament. Your bot should be concerned with surviving and catching the most spice possible **(not before reaching the center of the map)**.

Each game will be played in a 11 by 11 board between 4 bots in a *round-based* format.

### Priority

In the beginning of each round, each bot will receive the input, then the first to move will be the [ worm ](#worm) and, lastly, each bot will move depending on their priority (lower will move first). The priorities rotate between all bot.

### Victory Condition

First victory condition is to be the last one alive.

Then, the game will also end after 45 rounds.

Second victory condition is the most number of accumulated points (spice).

Third and last is the priority in the last round (lower is better)

**An Example:**

> Player 2 and 4 have both 10 points at the end of the 45º round. In this last round player 2 has priority one and player 4 has priority two. In this case player 2 is the winner.

### Board

Each line of the board/map

```
<line_1_Map>
<line_2_Map>
...
<line_<height>_Map>
```
Can contain 5 type of cells: empty, hole, spice or checkpoint and center.

- The position `0 0` corresponds to the top left corner of the board. 
- The position `11 11` corresponds to the bottom right corner of the board.
- All valid positions have positive values for their coordinates.
    - `-1 -1` is an invalid position.

#### Empty

**Character:** "."

#### Hole

**Character:** "O"

**Interaction with a bot:** If a bot ends up its movement in a hole, it loses.

#### Center

**Character:** "#"

**Interaction with a bot:** A bot needs to reach this cell before starting to collect spice (points). Apart from this its regarded as an empty cell.

The Worm starts the game in this cell.

#### Spice or Checkpoint

**Character:** (A number)

**Interaction with a bot:** When a bot enters one of this cells it receives the amount of points indicated in the cell. It will only gain points the first time it enters each checkpoint.

They can grant from 1 to 3 points.

A bot can only receive points if it has already been to the center at least once.

#### Edge

**Interaction with a bot:** If a bot moves out of the board, the effect is the same as if it fell into a hole (loses).

### Worm

```
<worm_X> <worm_Y>
```

The Worm starts the game in the [ center ](#center) of the board and its the first to move each round in a random fashion. It moves freely, not affecting or being affected by each cell.

**Interaction with a bot:** If a worm ends up in the same cell as a bot or vice-versa, the effect is the same as if it fell into a hole (loses).

### Interaction bot to bot

Two bots can't occupy the same cell. If a bot moves into an occupied cell it will "push" the other bot. The later will be moved a cell in the same direction as the one moving into the cell.

## Examples

### Example 1 (Initial State of the Game)

```
11
11
......2O...
.O..O.O3...
.O......O..
.....O.O...
O1O.....1O.
.....#.....
.OO1.O.O...
.....O.....
.......1...
.O.O..O..O.
...O.......
5 5
1
4
0 0
B 10 0
C 0 10
D 10 10
```