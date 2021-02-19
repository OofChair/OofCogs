from typing import Literal

import aiohttp
import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Fun(commands.Cog):
    """
    Fun cog, with fun features.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=572944636209922059,
            force_registration=True,
        )

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)


    @commands.group()
    async def fact(self, ctx):
        """Animal facts from Some Random API"""

    @fact.command()
    async def dog(self, ctx):
        """Get a random dog fact"""
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/dog") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(
                    url="https://thetrendler.com/wp-content/uploads/2016/08/10tb-dogsperm01-superJumbo.jpg"
                )
                embed.add_field(
                    name="Here's a random dog fact!", value=response["fact"]
                )
                await ctx.send(embed=embed)

    @fact.command()
    async def cat(self, ctx):
        """Get a random cat fact"""
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/cat") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(
                    url="https://i.ytimg.com/vi/C8NAYW-Z54o/maxresdefault.jpg"
                )
                embed.add_field(
                    name="Here's a random cat fact!", value=response["fact"]
                )
                await ctx.send(embed=embed)

    @fact.command()
    async def panda(self, ctx):
        """Get a random panda fact"""
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/panda") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(
                    url="https://nationalzoo.si.edu/sites/default/files/support/adopt/giantpanda-03.jpg"
                )
                embed.add_field(
                    name="Here's a random panda fact!", value=response["fact"]
                )
                await ctx.send(embed=embed)
    @commands.group()
    async def action(self, ctx):
        """Action commands, like hug, kiss, and more"""


    @action.command()
    async def hug(self, ctx, user: discord.Member):
        """Hug a user"""
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/animu/hug") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url=response["link"])
                embed.add_field(
                    name=f"{ctx.author.name} just hugged someone!",
                    value=f"{ctx.author.mention} hugged {user.mention}!",
                )
                await ctx.send(embed=embed)
