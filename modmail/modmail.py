from redbot.core import commands
import discord

class Modmail(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def setup(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await Guild.create_category("wot")
        await ctx.send("owo")
