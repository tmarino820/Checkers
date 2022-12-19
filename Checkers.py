"""
author: Antonio Marino
tools: ChatGPT
Summary: This is a Python implementation of the game of Checkers using the
graphics package created by John Zelle. The code was generated
using OpenAI's ChatGPT, accessed at https://chat.openai.com/chat,
with some bug fixes done by hand.

The Checkers class has an __init__ method that initializes the game
window, the game board, and the current player's turn. It also
initializes variables to store the currently selected piece, and
a list of valid moves for that piece. The __init__ method also
draws the board and the pieces on the game window.

The play method is a loop that runs the game. It gets mouse clicks
from the player, and processes them to determine the selected piece
and the move to make. If the player selects a valid piece and a valid
move, the game makes the move and updates the game state. If the
game is won by either player, the loop ends and a congratulatory
message is printed.
"""
from graphics import *

class Checkers:
    def __init__(self):
        self.win = GraphWin("Checkers", 600, 600)
        self.board = [[0, 1, 0, 1, 0, 1, 0, 1],
                      [1, 0, 1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [-1, 0, -1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1, 0, -1],
                      [-1, 0, -1, 0, -1, 0, -1, 0]]
        self.turn = 1
        self.selected = None
        self.valid_moves = []

        # draw the board
        for i in range(8):
            for j in range(8):
                if (i+j) % 2 == 0:
                    color = "white"
                else:
                    color = "gray"
                rect = Rectangle(Point(i*75, j*75), Point((i+1)*75, (j+1)*75))
                rect.setFill(color)
                rect.draw(self.win)

        # draw the pieces
        self.graphical_board = []
        for i in range(8):
            self.graphical_board.append([])
            for j in range(8):
                if self.board[i][j] == 1:
                    self.graphical_board[i].append(self.draw_piece(i, j, "red"))
                elif self.board[i][j] == -1:
                    self.graphical_board[i].append(self.draw_piece(i, j, "black"))
                else:
                    self.graphical_board[i].append(None)

    def play(self):
        while True:
            if self.red_won() or self.black_won():
                print("Congrats", "red" if self.red_won() else "black", "won")
            # get mouse click from player
            p = self.win.getMouse()
            x = int(p.getX() // 75)
            y = int(p.getY() // 75)
            print("Selected piece:",[tuple({x,y})])
            # check if a piece is selected
            if self.selected is None:
                if self.board[x][y] == self.turn or self.board[x][y] == 2*self.turn:
                    self.selected = (x, y)
                    self.valid_moves = self.get_valid_moves(x, y)
                    print("Valid moves:",self.valid_moves)
                elif self.board[x][y] == 0:
                    print("You must select a piece.")
                else:
                    print("You must select one of your own pieces.")
            else:
                if (x, y) in self.valid_moves:
                    jumped = len(self.get_jumps_moves(self.selected[0], self.selected[1]))>0
                    self.make_move(x, y)
                    if (len(self.get_jumps_moves(x, y))>0) and jumped:
                        self.selected = (x, y)
                        self.valid_moves = self.get_valid_moves(self.selected[0], self.selected[1])
                    else:
                        self.turn = -self.turn
                        self.selected = None
                        self.valid_moves = []
                else:
                    jumped = len(self.get_jumps_moves(self.selected[0], self.selected[1]))>0
                    print("That is not a valid move.")
                    if jumped:
                        print("You must perform another jump with the peice in", self.selected)
                        print("Valid moves:", self.valid_moves)
                    else:
                        self.selected = None

    def draw_piece(self, x, y, color, king=False):
        # draw the piece on the board
        center = Point(x*75 + 37.5, y*75 + 37.5)
        piece = Circle(center, 30)
        piece.setFill(color)
        piece.draw(self.win)
        if (king):
            crown = Circle(center, 20)
            crown.setFill("blue")
            crown.draw(self.win)
            return tuple({center, piece, crown})
        return tuple({center, piece})

    def undraw_piece(self, x, y):
        if (self.graphical_board[x][y] != None):
            for item in self.graphical_board[x][y]:
                item.undraw()
        return None

    def get_jumps_moves(self, x, y):
        jumps = []
        # check for jump moves
        if (y+2 <= 7 and x+2 <= 7) and (self.board[x+1][y+1] == -self.turn and self.board[x+2][y+2] == 0) and (self.board[x][y] == 1 or abs(self.board[x][y]) == 2):
            jumps.append((x+2,y+2))
        if (y-2 >= 0 and x+2 <= 7) and (self.board[x+1][y-1] == -self.turn and self.board[x+2][y-2] == 0) and (self.board[x][y] == 1 or abs(self.board[x][y]) == 2):
            jumps.append((x+2,y-2))
        if (y+2 <= 7 and x-2 >= 0) and (self.board[x-1][y+1] == -self.turn and self.board[x-2][y+2] == 0) and (self.board[x][y] == -1 or abs(self.board[x][y]) == 2):
            jumps.append((x-2, y+2))
        if (y-2 >= 0 and x-2 >= 0) and (self.board[x-1][y-1] == -self.turn and self.board[x-2][y-2] == 0) and (self.board[x][y] == -1 or abs(self.board[x][y]) == 2):
            jumps.append((x-2, y-2))
        return jumps

    def get_normal_moves(self, x, y):
        moves = []
        if (y+1 <= 7 and x+1 <= 7) and self.board[x+1][y+1] == 0 and (self.board[x][y] == 1 or abs(self.board[x][y]) == 2):
            moves.append((x+1,y+1))
        if (y-1 >= 0 and x+1 <= 7) and self.board[x+1][y-1] == 0 and (self.board[x][y] == 1 or abs(self.board[x][y]) == 2):
            moves.append((x+1,y-1))
        if (y+1 <= 7 and x-1 >= 0) and self.board[x-1][y+1] == 0 and (self.board[x][y] == -1 or abs(self.board[x][y]) == 2):
            moves.append((x-1, y+1))
        if (y-1 >= 0 and x-1 >= 0) and self.board[x-1][y-1] == 0 and (self.board[x][y] == -1 or abs(self.board[x][y]) == 2):
            moves.append((x-1, y-1))
        return moves

    def get_valid_moves(self, x, y):
        moves = []
        # check for jump moves first
        jumps = self.get_jumps_moves(x, y)
        if len(jumps)!=0:
            return jumps
        # if there are no jump moves, check for normal moves
        normal = self.get_normal_moves(x, y)
        if len(normal)!=0:
            return normal
        return []

    def make_move(self, x, y):
        type_of_piece = self.board[self.selected[0]][self.selected[1]]
        # remove the piece from the selected position
        x_decriment = 1 - 2*(self.selected[0] > x)
        y_decriment = 1 - 2*(self.selected[1] > y)
        for i in range(len(range(self.selected[0],x, x_decriment))):
            self.graphical_board[range(self.selected[0],x,x_decriment)[i]][range(self.selected[1],y,y_decriment)[i]] = self.undraw_piece(range(self.selected[0],x,x_decriment)[i], range(self.selected[1],y,y_decriment)[i])
            self.board[range(self.selected[0],x,x_decriment)[i]][range(self.selected[1],y,y_decriment)[i]] = 0

        # update the board
        if ((x == 0 and self.turn == -1) or (x == 7 and self.turn == 1)) or (abs(type_of_piece)==2):
            self.board[x][y] = 2*self.turn
        else:
            self.board[x][y] = self.turn
        self.board[self.selected[0]][self.selected[1]] = 0

        # draw the piece at the new position
        if abs(self.board[x][y])==2:
            self.graphical_board[x][y] = self.draw_piece(x, y, "red" if self.turn == 1 else "black",True)
        else:
            self.graphical_board[x][y] = self.draw_piece(x, y, "red" if self.turn == 1 else "black")

    def get_piece(self, x, y):
        return self.board[x][y]

    def red_won(self):
        game_done = True
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                game_done = self.board[i][j] >= 0

    def black_won(self):
        game_done = True
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                game_done = self.board[i][j] <= 0

game = Checkers()
game.play()
