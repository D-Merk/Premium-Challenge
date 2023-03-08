import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.Scanner;

public class Solution {
    static record Position(int x, int y){}

    private static char[][] map;

    private static Position wormPosition;

    private static Position myPosition;

    private static int width, height;
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        List<Character> possibleMoves = Arrays.asList('n', 's', 'e', 'w');
        while(true){
            try {
                width = scanner.nextInt();
            } catch(NoSuchElementException e) {
                // reached end of game
                break;
            }
            height = scanner.nextInt();

            scanner.nextLine(); // Flush
            map = new char[height][width];
            for (int y = 0; y < height; y++) {
                map[y] = scanner.nextLine().toCharArray();
            }
            wormPosition = readPosition(scanner);
            int priority = scanner.nextInt();
            int nrPlayers = scanner.nextInt();

            scanner.nextLine(); // Flush

            myPosition = readPosition(scanner);
            List<Position> otherPlayersPositions = new LinkedList<>();
            for (int i = 0; i < nrPlayers - 1; i++){
                scanner.next();
                otherPlayersPositions.add(readPosition(scanner));
            }

            Collections.shuffle(possibleMoves);
            for (Character move : possibleMoves) {
                if (testMove(move)) {
                    System.out.println(move);
                    break;
                }
            }
        }
    }

    private static boolean testMove(char move) {
        int x = myPosition.x, y = myPosition.y;
        Position newPosition = switch (move) {
            case 'n' -> new Position(myPosition.x, myPosition.y-1);
            case 's' -> new Position(myPosition.x, myPosition.y+1);
            case 'e' -> new Position(myPosition.x+1, myPosition.y);
            case 'w' -> new Position(myPosition.x-1, myPosition.y);
            default -> myPosition;
        };

        // check borders
        if (newPosition.x<0 || newPosition.y<0 || newPosition.x>width || newPosition.y>height) {
            return false;
        }

        // check holes
        char mapSymbol = map[newPosition.y][newPosition.x];
        if (mapSymbol == 'O') {
            return false;
        }

        // check worm
        if (wormPosition.equals(newPosition)) {
            return false;
        }

        return true;
    }

    private static Position readPosition(Scanner scanner) {
        Position p = new Position(scanner.nextInt(), scanner.nextInt());
        scanner.nextLine();
        return p;
    }
}