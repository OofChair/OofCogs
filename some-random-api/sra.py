import aiohttp
from redbot.core import commands


class SRA(commands.Cog):
    """API requests from Some Random API"""

    @commands.command()
    async def dogfact(self, ctx):
        """This does stuff!"""
        # Your code will go here
        async def something():
            async with aiohttp.ClientSession() as session:
                async with session.get("https://some-random-api.ml/facts/dog") as request:
                    response = await request.json()
                    print(response)
                    await something()
