#!/usr/bin/env python3
# encoding: utf-8
# © 2017 Benjamin Mintz <bmintz@protonmail.com>

from typing import Union

class Connect4Board(list):

	def __init__(self, width, height):
		self.width = width
		self.height = height

		# fill the board with 0s
		for y in range(height):
			self.append([0] * width)

	def __getitem__(self, xy):
		x, y = xy
		# basically self[y][x] but since this is __getitem__,
		# that would be recursive
		return list(self)[y][x]

	def __setitem__(self, pos: Union[int, tuple], new_value):
		"""Set self[x] or self[x,y] to new_value
		If pos is a tuple, attempt to set board[*pos] (x, y) to new_value.
		If pos is an int, attempt to play as player `player` at column `pos`

		If that position is already filled, raise IndexError
		"""

		x, y = self._xy(pos)

		if self[x, y] != 0:
			raise IndexError('there is already a move at that position')

		print(type(list(self)))
		type(list(self)[y][x]))
		list(self)[y][x] = new_value

	def __iter__(self):
		for y in range(self.height):
			for x in range(self.width):
				yield x, y

	def _xy(self, pos):
		if isinstance(pos, int):
			x = pos
			# only a column was passed
			return x, self._y(x)
		else:
			x, y = pos
			if y < self._y(x):
				# the given y is too damn high!
				raise IndexError('you can only move in the lowest empty position')
		return x, y

	def _y(self, x):
		"""find the lowest empty position for the column indicated by x"""
		# start from the bottom of the board and move up
		for y in range(self.height - 1, 0, -1):
			if self[x, y] == 0:
				return y
		raise ValueError('that column is full')


class Connect4Game:

	def __init__(self):
		self.board = Connect4Board(5, 5)
		self._turn_count = 0

	def move(self, player: int, column):
		if player not in (1, 2):
			raise ValueError('you may only play as player 1 or 2')
		if player != self._whose_turn():
			raise ValueError("it's not your turn!")

		self.board[column] = player
		self.turn_count += 1

	def __str__(self):
		return (
			"Player {}'s turn\n".format(self._whose_turn())
			+ '\n'.join(self._format_row(y) for y in range(self.board.height))
		)

	def _game_over(self):
		"""Has the game ended? If so, return the player that won,
		or 0 if no player won. If the game is not over, return False"""

		board = list(self.board) # makes it easier to slice

		#for x, y in self.board:
			#if board


	def _whose_turn(self):
		return self._turn_count % 2 + 1

	def _format_row(self, y):
		print(y)
		return ''.join(self[x, y] for x in range(self.board.width))

	def __getitem__(self, pos):
		pieces = '\N{medium white circle}\N{large red circle}\N{large blue circle}'

		print('game.getitem', self.board[pos])
		return pieces[self.board[pos]]
