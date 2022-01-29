from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from collections import defaultdict
from redbot.core.errors import CogLoadError

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class InviteTracker(commands.Cog):
    """
    An invite tracker cog for Red.
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=572944636209922059,
            force_registration=True,
        )
        default_guild = {
            "enabled": False,
            "channel": None,
        }
        self.config.register_guild(**default_guild)
        self.invites = defaultdict(list)

    __version__ = "1.2.0"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        n = "\n" if "\n\n" not in pre_processed else ""
        return f"{pre_processed}{n}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        return

    async def load(self, ctx):
        self.bot.loop.create_task(self.load(ctx))
        if ctx.me.guild_permissions.manage_guild == True:
            try:
                self.invites[ctx.guild.id] = await ctx.guild.invites()
            except discord.Forbidden:
                pass
            except Exception as e:
                print(e, flush=True)
        else:
            raise CogLoadError("")

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv

    @commands.group(aliases=["invset"])
    @commands.admin()
    @commands.guild_only()
    async def invitetrackerset(self, ctx):
        """Invite tracker settings

        Commands:
        `[p]invset channel` - Sets the invite logging channel
        `[p]invset enable` - Enable invite logging in your server
        """
        pass

    @invitetrackerset.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the invite tracker channel

        Arguments:
        `channel`: Select the channel for the invite logging to be sent to
        """
        if ctx.channel.permissions_for(channel.guild.me).send_messages == True:
            async with ctx.typing():
                await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"The log channel has been set to {channel.mention}")
        else:
            await ctx.send(
                "I can't send messages in that channel! Please give me perms and retry this command."
            )

    @commands.bot_has_permissions(manage_guild=True)
    @invitetrackerset.command()
    async def enable(self, ctx, yes_or_no: bool):
        """
        Enable/disable invite logging

        Arguments:
        `yes_or_no`: Enable/disable invite logging with yes or no, true or false, etc.
        """
        async with ctx.typing():
            await self.config.guild(ctx.guild).enabled.set(yes_or_no)
        if yes_or_no is True:
            await ctx.send("Join invite tracking has been turned on for this guild.")
        else:
            await ctx.send("Join invite tracking has been turned off for this guild.")

    @commands.command(aliases=["userinvites"])
    @commands.guild_only()
    async def invitesforuser(self, ctx, user: discord.Member = None):
        """See how many times a user's invites have been used"""
        if ctx.channel.permissions_for(ctx.me).manage_guild == True:
            async with ctx.typing():
                if user is None:
                    user = ctx.author
                total_invites = 0
                for i in await ctx.guild.invites():
                    if i.inviter == user:
                        total_invites = total_invites + 1
                embed = discord.Embed(title="📫 Invite counter")
                embed.add_field(
                    name=f"Invites for {user.name}#{user.discriminator}",
                    value=f"{total_invites} invites!",
                )
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                "I can't access invites. Please make sure I have the right permissions and try again."
            )

    # Invite tracking
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """On member listener for new users"""
        logs_channel = await self.config.guild(member.guild).channel()
        logs = self.bot.get_channel(logs_channel)
        invs_before = self.invites[member.guild.id]
        invs_after = await member.guild.invites()
        self.invites[member.guild.id] = invs_after
        if await self.config.guild(member.guild).enabled():
            embed = discord.Embed(
                title="Just joined the server",
                color=0x03D692,
            )
            embed.set_author(name=str(member), icon_url=member.avatar_url)
            embed.set_footer(text=f"ID: {member.id}")
            for invite in invs_before:
                if invite.uses < self.find_invite_by_code(invs_after, invite.code).uses:
                    embed.add_field(
                        name="Used invite",
                        value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\nCode: `{invite.code}`\nUses: `{str(invite.uses)}`",
                        inline=False,
                    )
                else:
                    embed = discord.Embed(
                        title="Just joined the server",
                        color=0x03D692,
                    )
                    embed.set_author(name=str(member), icon_url=member.avatar_url)
                    embed.set_footer(text=f"ID: {member.id}")
                    embed.clear_fields()
                    embed.add_field(
                        name="Couldn't find invite!",
                        value=f"I couldn't find the invite that this user used. ",
                        inline=False,
                    )
            await logs.send(embed=embed)
