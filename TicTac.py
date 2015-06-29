#!/usr/bin/env python

# This is a tic-tac-toe program with included AI
# Kellen Lask

##  Opens a tkinter canvas and draws a board which accepts mouse clicks to indicate
##  user moves. Then, the program determines an optimal move for the other side, and
##  takes it.

from tkinter import *
from tkinter.messagebox import askquestion


# ---------------------------------------------
#
#       Move Class
#
# ---------------------------------------------
class Move:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.weight = 0

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_weight(self):
		return self.weight

	def set_weight(self, weight):
		self.weight = weight

# ---------------------------------------------
#
#       TicTac Class
#
# ---------------------------------------------
class TicTac:
	COMPUTER = 2
	HUMAN = 1
	DRAW = 0
	NOT_OVER = -1
	LOSS = 1
	WIN = 2

	X_DIM = 500
	Y_DIM = 500

	# ---------------------------------------------
	#
	#       Graphics Functions
	#
	# ---------------------------------------------

	def draw_empty_board(self):
		# Draw a TicTacToe board
		self.canvas.create_line(0, self.Y_DIM / 3, self.X_DIM, self.Y_DIM / 3)
		self.canvas.create_line(0, 2 * self.Y_DIM / 3, self.X_DIM, 2 * self.Y_DIM / 3)
		self.canvas.create_line(self.X_DIM / 3, 0, self.X_DIM / 3, self.Y_DIM)
		self.canvas.create_line(2 * self.X_DIM / 3, 0, 2 * self.X_DIM / 3, self.Y_DIM)


	# x and y are 0-2 (indexes on the board, not coords)
	def draw_x(self, x, y):
		# Top-Left to Bottom-right
		x1 = self.X_DIM / 3 * x + 5
		y1 = self.Y_DIM / 3 * y + 5
		x2 = self.X_DIM / 3 * x + 162
		y2 = self.Y_DIM / 3 * y + 162
		self.canvas.create_line(x1, y1, x2, y2)

		# Bottom-left to Top Right
		y1 = self.Y_DIM / 3 * y + 162
		y2 = self.Y_DIM / 3 * y + 5
		self.canvas.create_line(x1, y1, x2, y2)


	# x and y are 0-2 (indexes on the board, not coords)
	def draw_o(self, x, y):
		x1 = self.X_DIM / 3 * x + 5
		y1 = self.Y_DIM / 3 * y + 5
		x2 = self.X_DIM / 3 * x + 162
		y2 = self.Y_DIM / 3 * y + 162
		self.canvas.create_oval(x1, y1, x2, y2)


	# Find the TicTacToe box that was clicked based on the mouse coords
	def get_box(self, xCoord, yCoord):
		# Figure out board X coord
		if xCoord < (self.X_DIM / 3):
			x = 0
		elif xCoord > (self.X_DIM / 3) and xCoord < (2 * self.X_DIM / 3):
			x = 1
		else:
			x = 2

		# Figure out board Y coord
		if yCoord < (self.Y_DIM / 3):
			y = 0
		elif yCoord > (self.Y_DIM / 3) and yCoord < (2 * self.Y_DIM / 3):
			y = 1
		else:
			y = 2

		return [x, y]


	def end_game_menu(self, winner):
		# Declare the end of the game
		if winner == self.COMPUTER:
			player = "The computer"
		elif winner == self.HUMAN:
			player = "You"
		else:
			player = "Nobody"

		choice = askquestion(player + " won!", "New Game?")

		# New game
		if choice == 'yes':
			# Reset the game
			self.canvas.delete("all")
			self.draw_empty_board()
			self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
			self.player = self.HUMAN

		# Quit
		else:
			sys.exit(0)

	# ---------------------------------------------
	#
	#       Artificial Intelligence
	#
	# ---------------------------------------------
	#Determines the value of a given move
	def get_weight(self, winner, depth):
		if winner == self.COMPUTER: # Win
			return 10 - depth
		elif winner == self.HUMAN:  # Loss
			return -10 + depth
		else:   # Draw
			return 0


	#Use the minimax algorithm to determine the best move (No pruning)
	def minimax(self, board, player, depth):
		openMoves = self.get_available_moves(board)

		bestMove = openMoves[0]
		bestWeight = -20

		#Go through all the empty moves, and determine their weights
		for move in openMoves:
			board[move.get_x()][move.get_y()] = player

			endGame = self.get_end_game(board)
			if endGame != self.NOT_OVER:
				#Board reached an evaluable end game
				move.set_weight(self.get_weight(endGame, depth))

			else:
				#Board is not at an end game yet
				if player == self.COMPUTER:
					otherPlayer = self.HUMAN
				else:
					otherPlayer = self.COMPUTER

				#We must go deeper
				nextMove = self.minimax(board, otherPlayer, depth + 1)
				move.set_weight(nextMove.get_weight())

			#If the move is the best so far, record it
			if move.get_weight() > bestWeight:
				bestMove = move
				bestWeight = bestMove.get_weight()

			#Undo the test move
			board[move.get_x()][move.get_y()] = 0

		return bestMove


	#Go through the given board and return all the empty spaces
	@staticmethod
	def get_available_moves(board):
		moveList = []

		for i in range(len(board[0])):
			for j in range(len(board[1])):
				if board[i][j] == 0:
					moveList.append(Move(i, j))

		return moveList

	# ---------------------------------------------
	#
	#       Game Logic
	#
	# ---------------------------------------------
	# runs the code for a complete move cycle (player move, AI move)
	def move(self, event):
		if self.player == self.HUMAN:
			#Find the clicked box
			points = self.get_box(event.x, event.y)

			# If the space is empty, execute game logic
			if self.board[points[0]][points[1]] == 0:
				# Update the board with the new move
				self.board[points[0]][points[1]] = 1
				self.draw_x(points[0], points[1])

				# Check for end-game
				winningPlayer = self.get_end_game(self.board)

				# If the game is over, show the menu
				if winningPlayer != self.NOT_OVER:
					self.end_game_menu(winningPlayer)

				# If the game is still going
				else:
					# Establish the moving player
					self.player = self.COMPUTER

					# Find best move
					move = self.minimax(self.board, self.player, 0)

					# Update the board
					self.draw_o(move.get_x(), move.get_y())
					self.board[move.get_x()][move.get_y()] = self.COMPUTER

					# Check for end-game
					winningPlayer = self.get_end_game(self.board)

					# If the game is over, show the menu
					if winningPlayer != self.NOT_OVER:
						self.end_game_menu(winningPlayer)

					# Establish the moving player
					self.player = self.HUMAN


	# Determine if there's an endgame: -1 = no, 0 = cat's game, 1 = Human wins, 2 = Computer wins
	def get_end_game(self, board):

		# Check if Human won
		if self.did_player_win(1, board):
			return self.HUMAN  # Player 1 won

		# Check if Computer won
		if self.did_player_win(2, board):
			return self.COMPUTER  # Player 2 won

		# Check for empty spaces
		for i in range(len(board[0])):
			for row in board:
				if row[i] == 0:
					return self.NOT_OVER  # Game is still in progress

		return self.DRAW


	# Store the ugly conditional to see if a player won
	def did_player_win(self, player, board):
		if    ((board[0][0] == player and board[0][1] == player and board[0][2] == player)
			or (board[0][0] == player and board[1][0] == player and board[2][0] == player)
			or (board[0][0] == player and board[1][1] == player and board[2][2] == player)
			or (board[1][0] == player and board[1][1] == player and board[1][2] == player)
			or (board[2][0] == player and board[2][1] == player and board[2][2] == player)
			or (board[0][2] == player and board[1][1] == player and board[2][0] == player)
			or (board[0][1] == player and board[1][1] == player and board[2][1] == player)
			or (board[0][2] == player and board[1][2] == player and board[2][2] == player)):
			return True  # The passed player won (human or computer)

		return False

	# ---------------------------------------------
	#
	#       Constructor
	#
	# ---------------------------------------------
	def __init__(self):
		# Creating the canvas
		self.canvas = Canvas(width=self.X_DIM, height=self.Y_DIM)
		self.canvas.bind('<ButtonPress-1>', self.move)
		self.canvas.pack()
		self.draw_empty_board()

		# Preparing the Game
		self.player = self.HUMAN  # It's the human's turn
		self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # indexed from left to right, top to bottom (like a book)

# ---------------------------------------------
#
#       Entry Point
#
# ---------------------------------------------
# Start the game
TicTac()

# Complete the loop
mainloop()
