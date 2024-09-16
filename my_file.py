import sys

class Checkers:
    def __init__(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.current_turn = 'white'
        self.pieces = {'white': 12, 'red': 12}
    
    def initialize_board(self):
        """Initialize the board with pieces for both players."""
        # Place white pieces
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'w'
        
        # Place red pieces
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = 'r'

    def print_board(self):
        """Helper function to print the board state."""
        print('-'*50)
        for row in self.board:
            print(' '.join(row))
        print('-'*50)
        print()

    def capture(self, x0, y0, x1, y1, only_check = False):
        """Check if a capture is possible and if further captures are possible."""
        dx, dy = x1 - x0, y1 - y0
        if abs(dx) == 2 and abs(dy) == 2:
            mid_x, mid_y = (x0 + x1) // 2, (y0 + y1) // 2
            mid_piece = self.board[mid_y][mid_x]
            if ((self.current_turn == 'white' and mid_piece == 'r') or 
                (self.current_turn == 'red' and mid_piece == 'w')) and self.board[y1][x1] == '.':
                # Perform the capture
                if not only_check:
                    self.board[mid_y][mid_x] = '.'
                    self.pieces['white' if mid_piece == 'w' else 'red'] -= 1
                further_capture_possible = self.check_further_captures(x1, y1)
                return True, further_capture_possible
        return False, False

    def check_further_captures(self, x, y):
        """Check if further captures are possible from the given position."""
        directions = [(2, 2), (-2, 2)] if self.current_turn == 'white' else [(2, -2), (-2, -2)]
        for all in directions:
            dx, dy = all[0], all[1]
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:  # Check if within board
                mid_x, mid_y = (x + nx) // 2, (y + ny) // 2
                mid_piece = self.board[mid_y][mid_x]
                if ((self.current_turn == 'white' and mid_piece == 'r') or 
                    (self.current_turn == 'red' and mid_piece == 'w')) and self.board[ny][nx] == '.':
                    return True
        return False

    def make_move(self, x0, y0, x1, y1):
        """Execute the move on the board."""
        capture_made, further_capture_possible = self.capture(x0, y0, x1, y1)
        # print(capture_made)
        # print(further_capture_possible)
        piece = self.board[y0][x0]
        self.board[y0][x0] = '.'
        self.board[y1][x1] = piece
        
        return further_capture_possible

    def check_move(self, x0, y0, x1, y1):
        """Check if the move is valid."""
        if x0 < 0 or x0 >= 8 or y0 < 0 or y0 >= 8 or x1 < 0 or x1 >= 8 or y1 < 0 or y1 >= 8:
            return False, "out of bounds"
        
        piece = self.board[y0][x0]
        if piece == '.':
            return False, "no piece at the starting position"
        
        if (self.current_turn == 'white' and piece != 'w') or (self.current_turn == 'red' and piece != 'r'):
            return False, "wrong player's turn"

        dx, dy = x1 - x0, y1 - y0


        if abs(dx) != abs(dy) or abs(dx) > 2:
            return False, "invalid move pattern"
        
        if abs(dx) == 1: 
            if (self.current_turn == 'white' and dy != 1) or (self.current_turn == 'red' and dy != -1):
                return False, "invalid direction"
        
        if abs(dx) == 2:
            if (self.current_turn == 'white' and dy != 2) or (self.current_turn == 'red' and dy != -2): # Since there are no kings, this checks if there is a move where jump is backwards.
                return False, "invalid jump direction"
            if not self.capture(x0, y0, x1, y1, only_check = True)[0]:
                return False, "invalid jump"

        if self.is_capture_possible() and abs(dx) != 2: # Check if there is a jump on the board and the move at hand is different. If so, this is an illegal move.
            return False, "Jump should be taken"
        
        if self.board[y1][x1] != '.':
            return False, "destination occupied"
        
        return True, ""

    def is_capture_possible(self):
        """ This function is to validate a move, and see if the necessary jump is being taken """
        for y in range(8):
            for x in range(8):
                if (self.board[y][x] == 'w' and self.current_turn == 'white') or (self.board[y][x] == 'r' and self.current_turn == 'red'):
                    if self.check_further_captures(x,y):
                        return True
        return False
    
    def has_valid_moves(self, player):
        """Check if the current player has any legal moves left."""
        directions = [(1, 1), (-1, 1)] if player == 'white' else [(1, -1), (-1, -1)]
        for y in range(8):
            for x in range(8):
                if (self.board[y][x] == 'w' and player == 'white') or (self.board[y][x] == 'r' and player == 'red'):
                    for dx, dy in directions:
                        # Check for regular move
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == '.':
                            return True
                        if self.check_further_captures(x,y):
                            return True
        return False


    def play_game(self, moves, print_board = False):
        """Process a list of moves and handle game play."""
        step = 0
        illegal_flag = False
        if print_board:
            print("Initial Board")
            self.print_board()
        for line_number, move in enumerate(moves, start=1):
            try:
                x0, y0, x1, y1 = map(int, move.strip().split(','))
            except ValueError:
                illegal_flag = True
                print(f"line {line_number} illegal move: {move}")
                break

            valid, message = self.check_move(x0, y0, x1, y1)
            if not valid:
                print(f"line {line_number} illegal move: {move} ({message})")
                illegal_flag = True
                break

            further_capture_possible = self.make_move(x0, y0, x1, y1)
            # Initial check if any of the pieces do not exist. This is just an early stop condition.
            # if self.pieces['white'] == 0:
            #     print('red')
            #     return
            # if self.pieces['red'] == 0:
            #     print('white')
            #     return

            step += 1
            if print_board:
                print("STEP", step)
                self.print_board()

            # Switch turn if no further capture is possible
            if not further_capture_possible:
                self.current_turn = 'red' if self.current_turn == 'white' else 'white'

            # Check if there are any possible moves.
            if not self.has_valid_moves(self.current_turn):
                no_of_w = self.pieces['white']
                no_of_r = self.pieces['red']
                if no_of_w > no_of_r:
                    print("White")
                elif no_of_r > no_of_w:
                    print("Red")
                else:
                    print("Tie")
                return

        # If game is incomplete
        if not illegal_flag:
            print("incomplete game")

def main():
    if len(sys.argv) != 2:
        print("Usage: python checkers.py <path_to_moves_file>. This needs an argument.")
        return

    file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            moves = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    game = Checkers()
    game.play_game(moves)

if __name__ == "__main__":
    main()
