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
    __version__ = "1.1.0"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        n = "\n" if "\n\n" not in pre_processed else ""
        return f"{pre_processed}{n}\nCog Version: {self.__version__}"

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

    # Command code

    @commands.command()
    async def randmeme(self, ctx):
        """Get a random meme from r/memes"""
        await ctx.trigger_typing()
        async with self.session.get(
            "https://imageapi.fionn.live/reddit/memes"
        ) as request:
            try:
                response = await request.json()
            except aiohttp.ContentTypeError:
                embed = await self.error_embed(ctx)
                return await ctx.send(embed=embed)
            if request.status != 200:
                embed = await self.error_embed(ctx)
            else:
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url=response["img"])
                embed.add_field(
                    name=response["title"],
                    value=f"Posted by u/{response['author']}\nCan't see the picture? [Click here]({response['img']})",
                )
                embed.set_footer(
                    text=f"{response['upvotes']} 👍 {response['downvotes']} 👎 | Posted on: r/{response['endpoint']}"
                )

            await ctx.send(embed=embed)

    @commands.command()
    async def subr(self, ctx, subreddit):
        """Get a random picture from a subreddit \n\n If an error occurs, please wait a few seconds, then try again."""
        await ctx.trigger_typing()
        async with self.session.get(
            f"https://imageapi.fionn.live/reddit/{subreddit}"
        ) as request:
            try:
                response = await request.json()
            except aiohttp.ContentTypeError:
                embed = await self.error_embed(ctx)
                return await ctx.send(embed=embed)
            if request.status != 200:
                embed = await self.error_embed(ctx)
            else:
                embed = discord.Embed(color=(await ctx.embed_colour()))
                embed.set_image(url=response["img"])
                embed.add_field(
                    name=response["title"],
                    value=f"Posted by u/{response['author']}\nCan't see the picture? [Click here]({response['img']})",
                )
                embed.set_footer(
                    text=f"{response['upvotes']} 👍 {response['downvotes']} 👎 | Posted on: r/{response['endpoint']}"
                )

            await ctx.send(embed=embed)

    @commands.command()
    async def memeversion(self, ctx):
        """Find cog version"""
        await ctx.send(f"This cog is on version {self.__version__}.")

    async def error_embed(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Oops!",
            description="**That didn't work!**",
            color=(await ctx.embed_colour()),
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
        return embed
