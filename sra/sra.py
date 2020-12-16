import aiohttp
import discord
from redbot.core import commands

class sra(commands.Cog):
    """API requests from Some Random API"""
    @commands.group()
    async def fact(self, ctx):
       """go ahead children, make my day"""

        @fact.command()
        async def dog(ctx, self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/dog") as request:
                response = await request.json()
                embed = discord.Embed(colour=await ctx.embed_colour())
                embed.set_image(url='https://thetrendler.com/wp-content/uploads/2016/08/10tb-dogsperm01-superJumbo.jpg')
                embed.add_field(name='Here\'s a random dog fact!',value=response['fact'])
                await ctx.send(embed=embed)
