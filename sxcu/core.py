import re
from typing import Literal, Optional, Union

import aiohttp
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import humanize_list

from .errors import SubNeedToken, SubWrongToken, UnallowedFileType


class SXCU(commands.Cog):

    __author__ = ["Predeactor"]
    __version__ = "Beta 0.4"

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        """
        Nothing to delete...
        """
        pass

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return "{pre_processed}\n\nAuthor: {authors}\nCog Version: {version}".format(
            pre_processed=pre_processed,
            authors=humanize_list(self.__author__),
            version=self.__version__,
        )

    # Commands logic

    async def _image_upload_command_logic(self, ctx: commands.Context):
        # Getting image and upload
        try:
            image = await ctx.message.attachments[0].read()
        except IndexError:
            await ctx.send("You must upload an image.")
            ctx.command.reset_cooldown(ctx)
            return
        try:
            result = await self.image_upload(image)
        except (RuntimeError, AttributeError) as error:
            await ctx.send(error)
            return
        except (SubWrongToken, SubNeedToken) as error:
            await ctx.send("I was unable to send your file: `{error}`".format(error=error))
            ctx.command.reset_cooldown(ctx)
            return
        except UnallowedFileType as error:
            available_file_type = [
                ".png",
                ".jpg/.jpeg",
                ".tif/.tiff",
                ".gif",
                ".ico",
                ".bmp",
                ".webm",
            ]
            await ctx.send(
                str(error)
                + "\nRemember that the only available file type are:\n"
                + humanize_list(available_file_type)
            )
            return

        # Sending image, if everthing is okay
        url = result[0]
        deletion_url = result[1]
        thumbnail = result[2]
        user_dmed = await self._try_send_private_message_deletion(
            await ctx.embed_color(), ctx.author, url, deletion_url
        )
        raw_message, maybe_embed = await self._make_embed_and_raw_message(
            ctx, url, deletion_url if not user_dmed else None, thumbnail
        )
        await ctx.send(raw_message, embed=maybe_embed or None)

    async def _shorten_command_logic(self, ctx: commands.Context, link: str):
        # Looking if the given URL is correct
        possible_link = re.search(r"(?P<url>https?://[^\s]+)", link)
        if not possible_link:
            await ctx.send(
                "It look like your link isn't valid, you must add 'http(s)' at the beginning."
            )
            return

        # Shorten the URL, we don't habe much errors to check for.
        try:
            result = await self.shortener(link)
        except (RuntimeError, AttributeError) as error:
            await ctx.send(error)
            return

        # Send the result
        url = result[0]
        deletion_url = result[1]
        user_dmed = await self._try_send_private_message_deletion(
            await ctx.embed_color(), ctx.author, url, deletion_url
        )
        raw_message, maybe_embed = await self._make_embed_and_raw_message(
            ctx, url, deletion_url if not user_dmed else None
        )
        await ctx.send(raw_message, embed=maybe_embed or None)

    @staticmethod
    async def _try_send_private_message_deletion(
        color: Optional[int],
        user: Union[discord.Member, discord.User],
        original_link: str,
        deletion_link: str,
    ):
        """Try to send a private message to an user with links.

        Returns True if succeded, or False.
        """
        if not color:
            color = 0
        try:
            embed = discord.Embed(title="Deletion Link", color=color)
            embed.add_field(
                name="Link",
                value="[Click for deleting access]({url}) to {link}.".format(
                    url=deletion_link, link=original_link
                ),
            )
            await user.send(embed=embed)
            return True
        except discord.HTTPException:
            return False

    @staticmethod
    async def _make_embed_and_raw_message(
        ctx: commands.Context = None,
        url_to_use: str = None,
        deletion_url: str = None,
        thumbnail: str = None,
    ):
        """Return a text and maybe an embed with the link(s).

        Giving the deletion_url argument will add the URL to the embed and raw message."""
        embed = discord.Embed(title="Your link is available! 🎉", color=await ctx.embed_color())
        if ctx.channel.permissions_for(ctx.me).embed_links and await ctx.embed_requested():
            content = "URL: {url}".format(url=url_to_use)
            embed.add_field(
                name="Here is your shareable URL!",
                value=(
                    "Get access to your content [by clicking on me]({url})!".format(url=url_to_use)
                ),
            )
            if deletion_url:
                content += "\nDeletion URL: {url}".format(url=deletion_url)
                embed.add_field(
                    name="Deletion URL",
                    value=(
                        "[Click here]({url}) if you wish to delete the link.".format(
                            url=deletion_url
                        )
                    ),
                )
            if thumbnail:
                link = re.search(r"(?P<url>https?://[^\s]+)", thumbnail)
                if link:
                    embed.set_thumbnail(url=thumbnail)
            return content, embed
        message = (
            "Your content has been uploaded! 🎉\nYou can access it through this link: "
            "{url}".format(url=url_to_use)
        )
        if deletion_url:
            message += "\n\nUse this link to delete access: {delurl}".format(
                url=url_to_use, delurl=deletion_url
            )
        return message, None

    async def image_upload(self, image: bytes):
        """Function to upload an image.

        Parameter:
            image: bytes: The image we're uploading.

        Return:
            list: Return the URL, deletion URL and thumbnail link.

        Raise:
            AttributeError: No URL or token are defined.
            RuntimeError: An unknow error happened.
            SubNeedToken: The subdomain require a token for the payload.
            SubWrongToken: The subdomain received a wrong token.
            UnallowedFileType: The file type is not correct.
        """
        infos = await self._obtain_creditentials(True)
        url = infos[0]
        token = infos[1]
        payload = {"image": image}
        if token:
            payload["token"] = token
        async with aiohttp.ClientSession() as session:
            async with session.post(url + "/upload", data=payload) as response:
                status_code = response.status
                if status_code == 407:
                    raise SubNeedToken()
                if status_code == 403:
                    raise SubWrongToken()
                if status_code == 415:
                    raise UnallowedFileType()
                if status_code != 200:
                    raise RuntimeError("The server returned an unknow error. Try again later.")
                result: dict = await response.json()
        return [result["url"], result["del_url"], result["thumb"]]

    async def shortener(self, link: str):
        """Function to shorten a link.

        Parameter:
            link: str: The link we're reducing.

        Return:
            list: Return the URL and the URL used for deletion.

        Raise:
            AttributeError: No URL are defined.
            RuntimeError: An unknow error happened.
        """
        url = await self._obtain_creditentials(False)
        payload = {"link": link}
        async with aiohttp.ClientSession() as session:
            async with session.post(url + "/shorten", data=payload) as response:
                status_code = response.status
                if status_code != 200:
                    raise RuntimeError("An error has been returned by the server.")
                result: dict = await response.json()
        return [result["url"], result["del_url"]]

    async def _obtain_creditentials(self, need_token: bool = True):
        """Return the URL and the token if needed.

        Parameter:
            need_token: bool: If a token must be added.

        Return:
            str: The URL.
            str: The token if requested and existing.
        """
        listing = []
        keys = await self.bot.get_shared_api_tokens("sxcu")
        possible_url = keys.get("url")
        if not possible_url:
            raise AttributeError("URL for sxcu.net is not configured.")
        listing.append(possible_url)
        if need_token:
            possible_token = keys.get("api_key")
            listing.append(possible_token)
        if possible_url.endswith("/"):
            possible_url = possible_url[:-1]
            await self.bot.set_shared_api_tokens("sxcu", url=possible_url)
        return listing if need_token else possible_url
