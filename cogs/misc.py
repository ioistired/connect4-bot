#!/usr/bin/env python3
# encoding: utf-8

import time

from discord.ext import commands


class Misc:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def invite(self, context):
		"""Sends you the link to add Connect 4 to your server."""
		await context.send(
				'<https://discordapp.com/oauth2/authorize?client_id=378978711673896961&scope=bot&permissions=27712>')

	@commands.command()
	async def ping(self, context):
		"""Shows you the latency between Connect 4 and Discord's servers."""

		pong = '🏓 Pong! '
		start = time.time()
		message = await context.send(pong)
		rtt = (time.time() - start) * 1000
		# 10 µs is plenty precise
		await message.edit(content=pong + '│{:.2f}ms'.format(rtt))


def setup(bot):
	bot.add_cog(Misc(bot))
