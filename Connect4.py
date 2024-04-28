class Connect4:

    def __init__(self, board=None, turn="A"):
        if board is None:
            board = [["x" for i in range(7)] for i in range(6)]
        self.board = board
        self.turn = turn

    def __str__(self):
        # surround the board with | and - to make it look like a connect4 board with a column count at the bottom
        result = " "
        result += "  ".join(str(i) for i in range(7)) + "\n"
        for row in self.board:
            result += "|" + " |".join(row) + "|\n"
        result += "-" * 15
        return result

    def make_move(self, col, player):
        if self.board[0][col] != "x":
            return False
        for row in range(5, -1, -1):
            if self.board[row][col] == "x":
                self.board[row][col] = player
                return True
        return False

    def check_winner(self):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == "x":
                    continue
                if col + 3 < 7 and self.board[row][col] == self.board[row][col + 1] == self.board[row][col + 2] == \
                        self.board[row][col + 3]:
                    return self.board[row][col]
                if row + 3 < 6:
                    if self.board[row][col] == self.board[row + 1][col] == self.board[row + 2][col] == \
                            self.board[row + 3][col]:
                        return self.board[row][col]
                    if col + 3 < 7 and self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][
                        col + 2] == self.board[row + 3][col + 3]:
                        return self.board[row][col]
                    if col - 3 >= 0 and self.board[row][col] == self.board[row + 1][col - 1] == self.board[row + 2][
                        col - 2] == self.board[row + 3][col - 3]:
                        return self.board[row][col]
        return None

    def play_game(self):
        while True:
            print(self)
            col = int(input(f"Player {self.turn}, enter a column: "))
            if self.make_move(col, self.turn):
                winner = self.check_winner()
                if winner:
                    print(self)
                    print(f"Player {winner} wins!")
                    break
                self.turn = "B" if self.turn == "A" else "A"
            else:
                print("Invalid move, try again.")
        print("Game over!")

class Game:
    def __init__(self, player1, player2=None):
        self.player1 = player1
        self.player2 = player2
        self.game = Connect4()
        self.current_turn = (player1 if self.game.turn == "A" else player2)

    def __str__(self):

        emoji_board = []
        for row in self.game.board:
            emoji_row = []
            for cell in row:
                if cell == "A":
                    emoji_row.append(":red_circle:")
                elif cell == "B":
                    emoji_row.append(":large_blue_circle:")
                else:
                    emoji_row.append(":white_circle:")
            emoji_board.append("|" + "|".join(emoji_row) + "|")
        column_numbers = "   0    1     2    3    4     5    6"
        result = ""
        if not self.game.check_winner():
            if not self.player2 and not self.current_turn:
                result = f"Waiting for player 2 to join.\n"
            else:
                result = f"It's <@{self.current_turn}>'s turn.\n"
        result += "\n".join(emoji_board) + "\n" + column_numbers
        return result

    def __repr__(self):
        result = ""
        if not self.game.check_winner():
            if not self.player2 and not self.current_turn:
                result = f"Waiting for player 2 to join.\n"
            else:
                result = f"It's <@{self.current_turn}>'s turn.\n"
        result += self.game.__str__()
        return result

    def update_turn(self):
        self.current_turn = self.player1 if self.current_turn == self.player2 else self.player2

    def make_move(self, col, user):
        if self.current_turn == self.player1:
            player = "A"
        elif self.current_turn == self.player2:
            player = "B"
        else:
            return False, "You are not part of this game."
        if user != self.current_turn:
            return False, "It's not your turn."
        if self.game.make_move(col, player):
            winner = self.game.check_winner()
            if winner:
                return True, f"Player {winner} wins!"
            self.update_turn()
            return True, f"Move made. It's <@{self.current_turn}>'s turn."
        return False, "Invalid move, try again."