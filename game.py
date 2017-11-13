#!/usr/bin/env python3
# encoding: utf-8
# © 2017 Benjamin Mintz <bmintz@protonmail.com>

from typing import Union
from itertools import groupby, chain

class Board(list):

	def __init__(self, width, height, player1_name=None, player2_name=None):
		self.width = width
		self.height = height
		for x in range(width):
			self.append([0] * height)

	def __getitem__(self, pos: Union[int, tuple]):
		if isinstance(pos, int):
			return list(self)[pos]
		elif isinstance(pos, tuple):
			x, y = pos
			return list(self)[x][y]
		else:
			raise TypeError('pos must be an int or tuple')

	def __setitem__(self, pos: Union[int, tuple], new_value):
		x, y = self._xy(pos)

		if self[x, y] != 0:
			raise IndexError("there's already a move at that position")

		# basically self[x][y] = new_value
		# super().__getitem__(x).__setitem__(y, new_value)
		self[x][y] = new_value

	def _xy(self, pos):
		if isinstance(pos, tuple):
			return pos[0], pos[1]
		elif isinstance(pos, int):
			x = pos
			return x, self._y(x)
		else:
			raise TypeError('pos must be an int or tuple')

	def _y(self, x):
		"""find the lowest empty row for column x"""
		# start from the bottom and work up
		for y in range(self.height-1, -1, -1):
			if self[x, y] == 0:
				return y
		raise ValueError('that column is full')

	def _pos_diagonals(self):
		"""Get positive diagonals, going from bottom-left to top-right."""
		for di in ([(j, i - j) for j in range(self.width)] for i in range(self.width + self.height - 1)):
			yield [self[i, j] for i, j in di if i >= 0 and j >= 0 and i < self.width and j < self.height]

	def _neg_diagonals(self):
		"""Get negative diagonals, going from top-left to bottom-right."""
		for di in ([(j, i - self.width + j + 1) for j in range(self.height)] for i in range(self.width + self.height - 1)):
			yield [self[i, j] for i, j in di if i >= 0 and j >= 0 and i < self.width and j < self.height]

	def _full(self):
		"""is there a move in every position?"""

		for x in range(self.width):
			if self[x, 0] == 0:
				return False
		return True


class Connect4Game:

	TIE = -1
	NO_WINNER = 0

	PIECES = (
		'\N{medium white circle}'
		'\N{large red circle}'
		'\N{large blue circle}'
	)

	def __init__(self, player1_name=None, player2_name=None):
		if player1_name is not None and player2_name is not None:
			self.names = (player1_name, player2_name)
		else:
			self.names = ('Player 1', 'Player 2')

		self.board = Board(7, 6)
		self.turn_count = 0

	def move(self, x):
		self.board[x] = self._whomst_turn()
		self.turn_count += 1

	def _get_player_name(self, player_number):
		player_number -= 1 # these lists are 0-indexed but the players aren't

		return self.names[player_number]

	def _whomst_turn(self):
		return self.turn_count%2+1

	def _get_instructions(self):
		instructions = ''
		for i in range(1, self.board.width+1):
			instructions += str(i) + '\N{combining enclosing keycap}'
		return instructions + '\n'

	def __str__(self):
		win_status = self.whomst_won()
		instructions = ''

		if win_status == self.NO_WINNER:
			status = self._get_player_name(self._whomst_turn()) + "'s turn"
			instructions = self._get_instructions()
		elif win_status == self.TIE:
			status = "It's a tie!"
		else:
			status = self._get_player_name(win_status) + ' won!'
		status = status + '\n'

		return (
			status
			+ instructions
			+ '\n'.join(self._format_row(y) for y in range(self.board.height))
		)

	def _format_row(self, y):
		return ''.join(self[x, y] for x in range(self.board.width))

	def __getitem__(self, pos):
		x, y = pos
		return self.PIECES[self.board[x, y]]

	def whomst_won(self):
		"""Get the winner on the current board.
		If there's no winner yet, return Connect4Game.NO_WINNER.
		If it's a tie, return Connect4Game.TIE"""

		lines = (
			self.board, # columns
			zip(*self.board), # rows (zip picks the nth item from each column)
			self.board._pos_diagonals(), # positive diagonals
			self.board._neg_diagonals(), # negative diagonals
		)

		for line in chain(*lines):
			for player, group in groupby(line):
				if player != 0 and len(list(group)) >= 4:
					return player

		if self.board._full():
			return self.TIE
		else:
			return self.NO_WINNER

