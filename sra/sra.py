import aiohttp
import discord
from redbot.core import commands

class SRA(commands.Cog):
    """API requests from Some Random API"""
    @commands.group()
    async def fact(self, ctx):
       """go ahead children, make my day"""

    @fact.command()
    async def dog(self, ctx):
        """Get a random dog fact"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/dog") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url='https://thetrendler.com/wp-content/uploads/2016/08/10tb-dogsperm01-superJumbo.jpg')
                embed.add_field(name='Here\'s a random dog fact!',value=response['fact'])
                await ctx.send(embed=embed)

    @fact.command()
    async def cat(self, ctx):
        """Get a random cat fact"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/cat") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url='https://i.ytimg.com/vi/C8NAYW-Z54o/maxresdefault.jpg')
                embed.add_field(name='Here\'s a random cat fact!',value=response['fact'])
                await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        """Get a random dog fact"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/hug") as request:
                response = await request.json()
                await ctx.send(user.mention)
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url=response['link'])
                embed.add_field(name='ctx.author.mention hugged you!')
                await ctx.send(embed=embed)
