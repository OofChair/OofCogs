from redbot.core import commands

class OEEvariable(commands.Cog):
    """Random fun commands"""

    @commands.command()
    async def rickroll(self, ctx):
        """Rickroll your friends!"""
        # Your code will go here
        await ctx.send("https://giphy.com/gifs/rick-astley-Ju7l5y9osyymQ")
