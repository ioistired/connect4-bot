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
import re
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


class Bot(commands.AutoShardedBot):
	SEPARATOR = '━'

	def __init__(self, **kwargs):
		super().__init__(
			command_prefix=self.get_prefix_,
			description=kwargs.pop('description'),
			activity=discord.Game(name='!c4 help | shutting down on July 27')
		self.config = kwargs.pop('config')
		self.development_mode = self.config.get('release') == 'development'
		self.add_check(self.should_reply, call_once=True)

		self.start_time = None
		self.app_info = None

		self.loop.create_task(self.track_start())
		self.loop.create_task(self.load_all_extensions())


	async def should_reply(self, context):
		author = context.message.author

		if author == self.user:
			return False
		if not self.development_mode and author.bot:
			return False

		return True

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
		match = re.search(r'^!c4\s+', message.content)
		prefix = '' if match is None else match.group(0)

		if match:
			prefix = match.group(0)
			return commands.when_mentioned_or(prefix)(bot, message)
		else:
			return commands.when_mentioned(bot, message)

	async def load_all_extensions(self):
		await self.wait_until_ready()
		await asyncio.sleep(1)	# ensure that on_ready has completed and finished printing
		for extension in (
				'cogs.connect4',
				'cogs.meta',
				'ben_cogs.misc',
				'ben_cogs.stats',
				'ben_cogs.debug',
				'jishaku'):
			try:
				self.load_extension(extension)
			except:
				error = extension + '\n' + traceback.format_exc()
				message = 'failed to load extension ' + error
			else:
				message = 'loaded ' + str(extension)
			print(message)

	async def on_ready(self):
		"""
		This event is called every time the bot connects or resumes connection.
		"""
		self.app_info = await self.application_info()
		self.client_id = self.app_info.id
		lines = (
			'Logged in as: {0.user}'.format(self),
			'Using discord.py version: {}'.format(discord.__version__),
			'Owner: {0.app_info.owner}'.format(self),
			'Template Maker: SourSpoon / Spoon#7805')
		separator = self.SEPARATOR * max(map(len, lines))
		print(separator, '\n'.join(lines), separator, sep='\n')


logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.close()
