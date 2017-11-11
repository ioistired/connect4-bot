import discord
from discord.ext import commands


class Sample:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def test(self, ctx):
        """
        A test command, Mainly used to show how commands and cogs should be laid out.
        """
        await ctx.send('Tested!')
    
    @commands.group(has_subcommands=True, invoke_without_command=True)
    async def foo(self, ctx):
        """
        A sub command group, Showing how sub command groups can be made.
        """
        await ctx.send('try my subcommand')
    
    @foo.command(aliases=['an_alias'])
    async def bar(self, ctx):
        """
        I have an alias!, I also belong to command 'foo'
        """
        await ctx.send('foo bar!')


def setup(bot):
    bot.add_cog(Sample(bot))
