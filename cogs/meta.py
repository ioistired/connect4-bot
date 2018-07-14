#!/usr/bin/env python3
# encoding: utf-8

import discord
from discord.ext import commands


class Meta:
	def __init__(self, bot):
		self.bot = bot
		self.bot.loop.create_task(self._init())

	async def _init(self):
		app_info = await self.bot.application_info()
		self.bot.owner = app_info.owner

	@commands.command()
	async def invite(self, context):
		"""Sends you the link to add Connect 4 to your server."""
		await context.send(
			f'Sorry, this bot is no longer public. It will shut down on July 27.\n'
			f'Please contact @{self.bot.owner} for more information and alternative bots.')


def setup(bot):
	bot.add_cog(Meta(bot))
