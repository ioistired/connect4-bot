#!/usr/bin/env python3
# encoding: utf-8

import time

from discord.ext import commands


def static_command(*args, **kwargs):
	def wrapper(func):
		return staticmethod(commands.command(*args, **kwargs)(func))
	return wrapper


class Misc:
	def __init__(self, bot):
		self.bot = bot

	@static_command()
	async def invite(context):
		await context.send(
				'<https://discordapp.com/oauth2/authorize?client_id=378978711673896961&scope=bot&permissions=27712>')

	@static_command()
	async def ping(context):
		pong = '🏓 Pong! '
		start = time.time()
		message = await context.send(pong)
		rtt = (time.time() - start) * 1000
		# 10 µs is plenty precise
		await message.edit(content=pong + '│{:.2f}ms'.format(rtt))


def setup(bot):
	bot.add_cog(Misc(bot))
