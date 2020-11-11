from redbot.core import commands

class OEEvariable(commands.Cog):
    """Random fun commands"""

    @commands.command()
    async def rickroll(self, ctx):
        """Rickroll your friends!"""
        # Your code will go here
        await ctx.send("https://giphy.com/gifs/rick-astley-Ju7l5y9osyymQ")

    @commands.command()
    async def jebait(self, ctx):
        """Rickroll your friends!"""
        # Your code will go here
        await ctx.send("https://media1.tenor.com/images/065a5ddbe6bd52171c59967167217287/tenor.gif?itemid=14527830")
