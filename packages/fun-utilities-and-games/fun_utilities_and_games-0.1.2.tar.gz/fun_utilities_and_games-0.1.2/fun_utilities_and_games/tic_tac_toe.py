import tkinter as tk
import random

def run_tic_tac_toe():
    class TicTacToe:
        def __init__(self, root):
            self.root = root
            self.root.title("Tic Tac Toe")
            self.board = [[" " for _ in range(3)] for _ in range(3)]
            self.buttons = [[None for _ in range(3)] for _ in range(3)]
            self.current_player = "X"
            self.difficulty = "Easy"
            self.create_widgets()

        def create_widgets(self):
            tk.Label(self.root, text="Tic Tac Toe", font=("Arial", 16)).grid(row=0, column=0, columnspan=3)
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j] = tk.Button(
                        self.root, text=" ", font=("Arial", 20), height=2, width=5,
                        command=lambda i=i, j=j: self.make_move(i, j)
                    )
                    self.buttons[i][j].grid(row=i + 1, column=j)

            tk.Button(self.root, text="Restart", font=("Arial", 12), command=self.reset_board).grid(row=4, column=0, columnspan=3)
            tk.Label(self.root, text="Difficulty:", font=("Arial", 12)).grid(row=5, column=0)
            tk.Button(self.root, text="Easy", font=("Arial", 12), command=lambda: self.set_difficulty("Easy")).grid(row=5, column=1)
            tk.Button(self.root, text="Hard", font=("Arial", 12), command=lambda: self.set_difficulty("Hard")).grid(row=5, column=2)

        def set_difficulty(self, level):
            self.difficulty = level

        def make_move(self, row, col):
            if self.board[row][col] == " " and self.current_player == "X":
                self.board[row][col] = "X"
                self.buttons[row][col].config(text="X")
                if self.check_winner("X"):
                    self.show_winner("Player")
                elif self.is_draw():
                    self.show_winner("Draw")
                else:
                    self.current_player = "O"
                    self.computer_move()

        def computer_move(self):
            if self.difficulty == "Easy":
                self.easy_computer_move()
            else:
                self.hard_computer_move()
            if self.check_winner("O"):
                self.show_winner("Computer")
            elif self.is_draw():
                self.show_winner("Draw")
            else:
                self.current_player = "X"

        def easy_computer_move(self):
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
            row, col = random.choice(empty_cells)
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")

        def hard_computer_move(self):
            best_score = float("-inf")
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = " "
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            row, col = best_move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")

        def minimax(self, is_maximizing):
            if self.check_winner("O"):
                return 1
            if self.check_winner("X"):
                return -1
            if self.is_draw():
                return 0

            if is_maximizing:
                best_score = float("-inf")
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == " ":
                            self.board[i][j] = "O"
                            score = self.minimax(False)
                            self.board[i][j] = " "
                            best_score = max(best_score, score)
                return best_score
            else:
                best_score = float("inf")
                for i in range(3):
                    for j in range(3):
                        if self.board[i][j] == " ":
                            self.board[i][j] = "X"
                            score = self.minimax(True)
                            self.board[i][j] = " "
                            best_score = min(best_score, score)
                return best_score

        def check_winner(self, mark):
            for row in self.board:
                if all(cell == mark for cell in row):
                    return True
            for col in range(3):
                if all(self.board[row][col] == mark for row in range(3)):
                    return True
            if all(self.board[i][i] == mark for i in range(3)) or all(self.board[i][2 - i] == mark for i in range(3)):
                return True
            return False

        def is_draw(self):
            return all(cell != " " for row in self.board for cell in row)

        def show_winner(self, winner):
            if winner == "Draw":
                result = "It's a draw!"
            else:
                result = f"{winner} wins!"
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(state="disabled")
            tk.Label(self.root, text=result, font=("Arial", 14), fg="red").grid(row=6, column=0, columnspan=3)

        def reset_board(self):
            self.board = [[" " for _ in range(3)] for _ in range(3)]
            self.current_player = "X"
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].config(text=" ", state="normal")
            for widget in self.root.grid_slaves():
                if int(widget.grid_info()["row"]) == 6:
                    widget.destroy()

    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()

