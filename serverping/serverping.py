from typing import Literal, Tuple
from simple_ping import Ping

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

__version__ = "1.0.0"


class ServerPing(commands.Cog):
    """
    Ping a server.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=572944636209922059,
            force_registration=True,
        )

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        """Nothing to delete"""
        return

    def setup_string(self, item: str) -> Tuple[str, bool]:
        """Set a string as a url"""
        changed = False
        if item.startswith("https://"):
            item = item[8:]
            changed = True
        if "/" in item:
            item = item.split("/")[0]
            changed = True
        return item, changed

    @commands.command()
    async def serverping(self, ctx, server: str):
        """Ping a server or an IP. \n\n**Pinging a specific port will not work. This is due to restrictions with the lib.** \n\nExample request: `[p]serverping oofchair.xyz` Adding https://, adding a trailing slash, or adding something after the / will cause this to not work."""
        server, changed = self.setup_string(server)
        msg = None
        if changed:
            msg = await ctx.send(
                content=f"I have edited your address to be pingable... (**{server}**)"
            )
        await ctx.trigger_typing()
        ping = Ping(server)
        embed = discord.Embed(title=f"Pinged {server}!", color=await ctx.embed_colour())
        embed.add_field(
            name=f":green_circle: **Server returned {ping.avg} ms!**",
            value=f"**It returned {ping.returncode} error(s)!**",
            inline=False,
        )
        embed.set_footer(text=f"I pinged {server}!")
        if msg is not None:
            await msg.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def pingversion(self, ctx):
        """Check what version the cog is on."""
        await ctx.send(f"This cog is on version {__version__}.")


# Ping avg return: {ping.avg}
# Ping errors return: {ping.returncode}
