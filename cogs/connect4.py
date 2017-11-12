#!/usr/bin/env python3
# encoding: utf-8
# © 2017 Benjamin Mintz <bmintz@protonmail.com>
#
# Using code from SourSpoon under the MIT License
# https://github.com/SourSpoon/Discord.py-Template

import asyncio

import discord
from discord.ext import commands

from game import Connect4Game


class Connect4:

	DIGITS = [str(digit) + '\N{combining enclosing keycap}' for digit in range(1, 8)]

	def __init__(self, bot):
		self.bot = bot
		self.games = {}

	@commands.command()
	async def play(self, ctx, player2: discord.Member):
		"""
		Play connect4 with another player
		"""
		game = Connect4Game(
			await self.get_name(ctx.message.author),
			await self.get_name(player2)
		)

		self.games[ctx.message.author] = game

		game.message = await ctx.send(str(game))

		for digit in self.DIGITS:
			await game.message.add_reaction(digit)

		def check(reaction, user):
			return (
				user in (ctx.message.author, player2)
				and str(reaction) in self.DIGITS
			)

		while game.whomst_won() == game.NO_WINNER:
			reaction, user = await self.bot.wait_for(
				'reaction_add',
				check=check
			)

			await asyncio.sleep(0.3)
			await game.message.remove_reaction(reaction, user)

			try:
				# convert the reaction to a 0-indexed int and move in that column
				game.move(self.DIGITS.index(str(reaction)))
			except ValueError:
				pass # the column may be full

			await game.message.edit(content=str(game))
			self.games[ctx.message.author] = game

		await game.message.clear_reactions()
		await game.message.edit(content=str(game))
		await self.delete_game(ctx.message.author)

	@commands.command()
	async def leave(self, ctx):
		try:
			await game.message.edit(
				content='Player 2 won (Player 1 forfeited)'
				# skip the first two lines
				# (the status line and the instruction line)
				+ '\n'.join('\n'.split(str(game))[2:])
			)
		except:
			pass

		try:
			await self.delete_game(ctx.message.author)
		except KeyError:
			await ctx.send("You don't have a game to leave!")

	async def delete_game(self, author):
		del self.games[author]

	async def get_name(self, member):
		return member.nick or member.name


def setup(bot):
	bot.add_cog(Connect4(bot))
