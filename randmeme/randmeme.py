from typing import Literal
import aiohttp
import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class RandMeme(commands.Cog):
    """
    Get a random meme from Reddit.
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


# actual code :Kappa:
    @commands.command()
    async def randmeme(self, ctx):
        """Get a random dog fact"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://imageapi.fionn.live/reddit/memes") as request:
                response = await request.json()
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.add_field(name=response[title],value=response[author]
                await ctx.send(embed=embed)