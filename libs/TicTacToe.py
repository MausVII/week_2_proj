import os
from itertools import chain
from more_itertools import all_equal
import libs.tic_utils as tic_utils

class OutOfRangeY(Exception): pass
class TooManyCharacters(Exception): pass
class InvalidXCharacter(Exception): pass
class InitialCharNumber(Exception): pass
class PositionTaken(Exception): pass


class TicTacToe():
    X_BINDINGS = {'a': 0, 'b': 1, 'c': 2}
    EMPTY_BOARD = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            ]

    def __init__(self):
        self.grid = TicTacToe.EMPTY_BOARD.copy()
        self.current_player = 'X'
        self.running = True

    def run(self):
        while self.running:
            self.clear_terminal()
            self.display_main_menu()
            choice = self.get_main_option()
        
            # Play option
            if choice.lower() == 'p':
                round_over = False
                # Round loop
                while round_over == False:
                    self.take_turn()
                    # Scan will end round if win conditions are met
                    if self.scan_winner():
                        self.end_round()
                        self.display_win()
                        self.save_scoreboard()
                        round_over = True
                    # Scan will end round if there are no available positions left
                    # If scan_winner() didn't trigger, it is a tie
                    elif self.scan_gameover():
                        self.end_round()
                        self.display_tie()
                        round_over = True

            # Scoreboard option
            elif choice.lower() == 's':
                self.display_scoreboard()

            # Quit option
            elif choice.lower() == 'q':
                input("Press any key to confirm.")
                quit()

    def display_board(self):
        print()
        for idx, col in enumerate(self.grid):
            row = F"{idx + 1} | {col[0]} | {col[1]} | {col[2]} |"
            print(row)
            print('-' * len(row))
        print("    A   B   C\n")

    def display_main_menu(self):
        print(tic_utils.ter_colors.OKCYAN + tic_utils.get_game_title())
        print("\t\tP) Play")
        print("\t\tS) See Scoreboard")
        print("\t\tQ) Quit\n")

    def end_round(self):
        self.switch_player()
        self.clear_terminal()
        self.display_board()
        
    
    def display_win(self):
        print("Game Over")
        print(F"{self.current_player} won!")
        input("Press any key to continue")

    def display_tie(self):
        print("Game Over")
        print(F"The game resulted in a tie")
        input("Press any key to continue")

    def display_scoreboard(self):
        self.clear_terminal()
        with open('tictactoc_scoreboard', 'r') as file:
            lines = file.readlines()
            for line in lines:
                player = line.split()[:-1]
                score = line.split()[-1]
                print(F"{' '.join(player)}: {score}")
        
        input("Press any key to continue")

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
            any((all_equal(row) and ' ' not in row for row in self.grid))
            or any((all_equal(row) and ' ' not in row for row in zip(*self.grid)))
            or (' ' not in (grid[idx] for idx, grid in enumerate(self.grid)) and all_equal(grid[idx] for idx, grid in enumerate(self.grid)))
            or (' ' not in (grid[0 - idx] for idx, grid in enumerate(self.grid)) and all_equal(grid[0 - idx] for idx, grid in enumerate(self.grid)))
            )

    def scan_gameover(self):
        return ' ' not in chain(*self.grid)

    def take_turn(self):
        self.clear_terminal()
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
    
    def get_main_option(self):
        response = ''
        response = input()
        while response.isnumeric() or response.lower() not in ['p', 's', 'q']:
            print("Invalid command. Please enter p, s, or q")
            input("Press any key to continue...")
            self.clear_terminal()
            self.display_main_menu()
            response = input()
        return response

    def clear_terminal(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
