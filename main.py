#!/usr/bin/env python3
# encoding: utf-8
# © 2017 Benjamin Mintz <bmintz@protonmail.com>
#
# Using code from SourSpoon
# https://github.com/SourSpoon/Discord.py-Template


import asyncio
import datetime
import json
import logging
from pathlib import Path
import traceback

import discord
from discord.ext import commands


def config_load():
	with open('data/config.json', 'r', encoding='utf-8') as doc:
		#  Please make sure encoding is correct, especially after editing the config file
		dump = json.load(doc)
		return dump


async def run():
	"""
	Where the bot gets started. If you wanted to create an aiohttp pool or other session for the bot to use,
	it's recommended that you create it here and pass it to the bot as a kwarg.
	"""

	config = config_load()
	bot = Bot(
		config=config,
		description=config['description'])
	try:
		await bot.start(config['tokens']['discord'])
	except KeyboardInterrupt:
		await bot.logout()


class Bot(commands.Bot):
	SEPARATOR = '━'

	def __init__(self, **kwargs):
		super().__init__(
			command_prefix=self.get_prefix_,
			description=kwargs.pop('description'))
		self.start_time = None
		self.app_info = None

		self.loop.create_task(self.track_start())
		self.loop.create_task(self.load_all_extensions())

	async def track_start(self):
		"""
		Waits for the bot to connect to discord and then records the time.
		Can be used to work out uptime.
		"""
		await self.wait_until_ready()
		self.start_time = datetime.datetime.utcnow()

	async def get_prefix_(self, bot, message):
		"""
		A coroutine that returns a prefix.

		I have made this a coroutine just to show that it can be done. If you needed async logic in here it can be done.
		A good example of async logic would be retrieving a prefix from a database.
		"""
		prefix = ['!']
		return commands.when_mentioned_or(*prefix)(bot, message)

	async def load_all_extensions(self):
		await self.wait_until_ready()
		await asyncio.sleep(1)	# ensure that on_ready has completed and finished printing
		for extension in (x.stem for x in Path('cogs').glob('*.py')):
			try:
				self.load_extension('cogs.'+extension)
			except Exception as e:
				error = extension + '\n' + traceback.format_exc()
				message = 'failed to load extension ' + error
			else:
				message = 'loaded ' + str(extension)
			separator = self.SEPARATOR * len(message)
			print(separator, message, separator, sep='\n')

	async def on_ready(self):
		"""
		This event is called every time the bot connects or resumes connection.
		"""
		self.app_info = await self.application_info()
		lines = (
			'Logged in as: {0.user}'.format(self),
			'Using discord.py version: {}'.format(discord.__version__),
			'Owner: {0.app_info.owner}'.format(self),
			'Template Maker: SourSpoon / Spoon#7805')
		separator = self.SEPARATOR * max(map(len, lines))
		print(separator, '\n'.join(lines), separator, sep='\n')

	async def on_message(self, message):
		"""
		 This event triggers on every message received by the bot. Including one's that it sent itself
		"""
		if message.author.bot:
			return	# ignore all bots
		await self.process_commands(message)


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
