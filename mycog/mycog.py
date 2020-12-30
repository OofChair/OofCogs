from redbot.core import commands

class Mycog(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def test(self, ctx):
        """This does stuff!"""
        # Your code will go here
            await ctx.send("helo!")
