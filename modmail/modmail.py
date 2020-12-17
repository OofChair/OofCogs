import aiohttp
import discord
from redbot.core import commands

class Modmail(commands.Cog):
    """Modmail uwu"""

    @commands.command()
    async def setup(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.guild.create_category(lol does this work? owo)
