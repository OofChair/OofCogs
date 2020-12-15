import aiohttp
from redbot.core import commands

class sra(commands.Cog):
    """API requests from Some Random API"""
    @commands.command()
    async def dogfact(self, ctx):
        """Gets random dog fact"""
        # Your code will go here
            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/facts/dog") as request:
                    response = await request.json()
             await ctx.send(response['fact'])
