from typing import Literal
import aiohttp
import discord
from redbot.core import commands  # , Config
from redbot.core.bot import Red

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class RedditPic(commands.Cog):
    """
    Get a random picture from Reddit subreddits.
    """

    # Version
    __version__ = "1.0.7"

    # Cookiecutter things
    def __init__(self, bot: Red) -> None:
        self.bot = bot
        #        self.config = Config.get_conf(
        #            self,
        #            identifier=572944636209922059,
        #            force_registration=True,
        #        )
        self.session = aiohttp.ClientSession()


    # Kill session on cog unload
    def cog_unload(self):
        self.bot.loop.run_until_complete(self.session.close())

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    # Comamnd code

    @commands.command()
    async def randmeme(self, ctx):
        """Get a random meme from r/memes"""
        await ctx.trigger_typing()
        async with self.session.get(
            f"https://imageapi.fionn.live/reddit/memes"
        ) as request:
            response = await request.json()
            if "err" in response:
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed = discord.Embed(
                    title="Oops!", description="**That didn't work!**"
                )
                embed.add_field(
                    name="The subreddit you are trying to access is not available!",
                    value="Some reasons this might be happening: \n - The subreddit is NSFW\n - The subreddit doesn't have any pictures. \n - The subreddit is blacklisted.",
                    inline=True,
                )
                embed.add_field(
                    name="If your problem does not match anything above,",
                    value="There might be a problem with the API.",
                    inline=True,
                )
                embed.set_footer(text="RedditPic cog, (c) OofChair 2021")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url=response["img"])
                embed.add_field(
                    name=response["title"],
                    value=f"Posted by u/{response['author']}\nCan't see the picture? [Click here]({response['img']})",
                )
                embed.set_footer(
                    text=f"{response['upvotes']} 👍 {response['downvotes']} 👎 | Posted on: r/{response['endpoint']} | Took {response['took']}"
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def subr(self, ctx, subreddit):
        """Get a random picture from a subreddit \n\n If an error occurs, please wait a few seconds, then try again."""
        await ctx.trigger_typing()
        async with self.session.get(
            f"https://imageapi.fionn.live/reddit/{subreddit}"
        ) as request:
            response = await request.json()
            if "err" in response:
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed = discord.Embed(
                    title="Oops!", description="**That didn't work!**"
                )
                embed.add_field(
                    name="The subreddit you are trying to access is not available!",
                    value="Some reasons this might be happening: \n - The subreddit is NSFW\n - The subreddit doesn't have any pictures. \n - The subreddit is blacklisted.",
                    inline=True,
                )
                embed.add_field(
                    name="If your problem does not match anything above,",
                    value="There might be a problem with the API.",
                    inline=True,
                )
                embed.set_footer(text="RedditPic cog, (c) OofChair 2021")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url=response["img"])
                embed.add_field(
                    name=response["title"],
                    value=f"Posted by u/{response['author']}\nCan't see the picture? [Click here]({response['img']})",
                )
                embed.set_footer(
                    text=f"{response['upvotes']} 👍 {response['downvotes']} 👎 | Posted on: r/{response['endpoint']} | Took {response['took']}"
                )
                await ctx.send(embed=embed)

    @commands.command()
    async def memeversion(self, ctx):
        """Find cog version"""
        await ctx.send(f"This cog is on version {self.__version__}.")
