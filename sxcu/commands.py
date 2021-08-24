from redbot.core import commands

from .core import SXCU


class Commands(SXCU, name="SXCU"):
    @commands.command()
    async def shorten(self, ctx: commands.Context, link: str):
        """Shorten a link."""
        await self._shorten_command_logic(ctx, link)

    @commands.command(aliases=["uploadimage", "imageupload"], cooldown_after_parsing=True)
    @commands.is_owner()
    @commands.cooldown(1, 60)
    async def upload(self, ctx: commands.Context):
        """Upload an image to SXCU.

        You must upload an image with the command.
        You can send the following files type:
        `.png`, `.jpg`/`.jpeg`, `.tif`/`.tiff`, `.gif`, `.ico`, `.bmp` and `.webm`.
        """
        await self._image_upload_command_logic(ctx)

    @commands.command()
    @commands.is_owner()
    async def setsxcu(self, ctx: commands.Context):
        message = (
            "To register your SXCU URL:\n"
            "1. Go on https://sxcu.net and create your subdomain.\n"
            "2. Click on 'Private' if you want to be the only person to upload image, keep the "
            "token.\n"
            "3. Use `[p]set api sxcu url <Your URL>` (***IF*** you checked private, add `api_key "
            "<Your token>` to the command)."
        )
        await ctx.maybe_send_embed(message)
