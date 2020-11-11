from redbot.core import commands

class Copypasta(commands.Cog):
    """Random fun commands"""

    @commands.command()
    async def behappy(self, ctx):
        """Rickroll your friends!"""
        # Your code will go here
        await ctx.send("behappy")
