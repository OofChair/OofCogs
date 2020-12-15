import aiohttp
from redbot.core import commands


class Mycog(commands.Cog):
    """My custom cog"""

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
