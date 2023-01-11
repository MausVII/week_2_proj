import os
from more_itertools import all_equal

class OutOfRangeY(Exception): pass
class TooManyCharacters(Exception): pass
class InvalidXCharacter(Exception): pass
class InitialCharNumber(Exception): pass
class PositionTaken(Exception): pass


class TicTacToe():
    X_BINDINGS = {'a': 0, 'b': 1, 'c': 2}

    def __init__(self):
        self.grid = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            ]
        self.current_player = 'X'
        self.stop = False

    def display_board(self):
        print()
        for idx, col in enumerate(self.grid):
            row = F"{idx + 1} | {col[0]} | {col[1]} | {col[2]} |"
            print(row)
            print('-' * len(row))
        print("    A   B   C\n")
    
    def run(self):
        while not self.stop:
            self.take_turn()
            self.stop = self.scan_winner()
        
        self.end_round()
        self.save_scoreboard()

    def end_round(self):
        self.switch_player()
        os.system('clear')
        self.display_board()
        print("Game Over")
        print(F"{self.current_player} won!")

    def save_scoreboard(self):
        with open('tictactoc_scoreboard', 'r') as file:
            scores = file.readlines()

        with open('tictactoc_scoreboard', 'w') as file:
            if len(scores) > 0:
                prev_scores = [line.split()[-1] for line in scores]
                scores[0] = F"Player X {int(prev_scores[0]) + 1 if self.current_player == 'X' else prev_scores[0]}\n"
                scores[1] = F"Player O {int(prev_scores[1]) + 1 if self.current_player == 'O' else prev_scores[1]}"
                file.writelines(scores)
            else:
                scores.append(F"Player X {1 if self.current_player == 'X' else 0}\n")
                scores.append(F"Player O {1 if self.current_player == 'O' else 0}")
                file.writelines(scores)

    def scan_winner(self):
        return (
            any([all_equal(row) and ' ' not in row for row in self.grid])
            or any([all_equal(row) and ' ' not in row for row in zip(*self.grid)])
            or (' ' not in [self.grid[0][0], self.grid[1][1], self.grid[2][2]] and all_equal([self.grid[0][0], self.grid[1][1], self.grid[2][2]]))
            or (' ' not in [self.grid[0][2], self.grid[1][1], self.grid[2][0]] and all_equal([self.grid[0][2], self.grid[1][1], self.grid[2][0]]))
            )

    def take_turn(self):
        os.system('clear')
        self.display_board()
        print(F"Make a move {'Player One' if self.current_player == 'X' else 'Player Two'}...")
        pos = self.read_move()
        self.grid[pos['y']][pos['x']] = self.current_player
        self.switch_player()

    def switch_player(self):
        self.current_player = 'X' if self.current_player == 'O' else 'O'


    def read_move(self):
        x = None
        y = None
        while x == None and y == None:
            response = input("Enter the target position: ")
            try:
                if len(response) > 2:
                    raise TooManyCharacters

                x = response[0]
                if x.isnumeric():
                    raise InitialCharNumber
                if x.lower() not in ['a', 'b', 'c']:
                    raise InvalidXCharacter

                y = response[1]
                y = int(y) - 1
                if y < 0 or y > 2:
                    raise OutOfRangeY

                x =  TicTacToe.X_BINDINGS[x.lower()]
                if self.grid[y][x] != ' ':
                    raise PositionTaken

            except InitialCharNumber:
                print("Please use a letter and then a number")
                x = None
                y = None
            except TooManyCharacters:
                print("Please input two characters only")
                x = None
                y = None
            except ValueError:
                print("Second character must be a number")
                x = None
                y = None
            except OutOfRangeY:
                print("Valid numbers go from 1 to 3")
                x = None
                y = None
            except InvalidXCharacter:
                print("Please use a letter between A and C")
                x = None
                y = None
            except PositionTaken:
                print("Position is already taken")
                x = None
                y = None
        
        return {'x': x, 'y': y}

if __name__ == '__main__':
    game = TicTacToe()
    game.run()