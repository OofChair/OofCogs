from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from collections import defaultdict

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
            "joinenabled": True,
            "leaveenabled": True,
        }
        self.config.register_guild(**default_guild)
        self.invites = defaultdict(list)
        bot.loop.create_task(self.load())

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
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    async def load(self):
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()
            except discord.Forbidden:
                pass
            except Exception as e:
                print(e, flush=True)

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv

    @commands.group(aliases=["invset"])
    @commands.admin()
    @commands.bot_in_a_guild()
    async def invitetrackerset(self, ctx):
        """Invite tracker settings

        Commands:
        `[p]invset channel` - Sets the invite logging channel
        `[p]invset enable` - Enable invite logging in your server
        `[p]invset leaveenable` - Enable/disable leave messages
        `[p]invset joinenable` - Enable/disable join invite messages
        """
        pass

    @invitetrackerset.command()
    async def channel(self, ctx, channel: discord.TextChannel):
        """Set the invite tracker channel

        Arguments:
        `channel`: Select the channel for the invite logging to be sent to
        """
        async with ctx.typing():
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(f"The log channel has been set to {channel.mention}")

    @invitetrackerset.command()
    async def enable(self, ctx, yes_or_no: bool):
        """Enable/disable invite logging

        Arguments:
        `yes_or_no`: Enable/disable invite logging with yes or no, true or false, etc.
        """
        async with ctx.typing():
            await self.config.guild(ctx.guild).enabled.set(yes_or_no)
            if yes_or_no is True:
                await ctx.send("Invite tracking has been turned on for this guild.")
            else:
                await ctx.send("Invite tracking has been turned off for this guild.")

    @invitetrackerset.command()
    async def leaveenable(self, ctx, yes_or_no: bool):
        """Enable/disable leave messages

        Arguments:
        `yes_or_no`: Enable/disable leave logging with yes or no, true or false, etc.
        """
        async with ctx.typing():
            await self.config.guild(ctx.guild).leaveenabled.set(yes_or_no)
            if yes_or_no is True:
                await ctx.send(
                    "Leave invite tracking has been turned on for this guild."
                )
            else:
                await ctx.send(
                    "Leave invite tracking has been turned off for this guild."
                )

    @invitetrackerset.command()
    async def joinenable(self, ctx, yes_or_no: bool):
        """Enable/disable join messages

        Arguments:
        `yes_or_no`: Enable/disable join invite logging with yes or no, true or false, etc.
        """
        async with ctx.typing():
            await self.config.guild(ctx.guild).joinenabled.set(yes_or_no)
            if yes_or_no is True:
                await ctx.send(
                    "Join invite tracking has been turned on for this guild."
                )
            else:
                await ctx.send(
                    "Join invite tracking has been turned off for this guild."
                )

    @commands.command(aliases=["userinvites"])
    async def invitesforuser(self, ctx, user: discord.Member = None):
        """See how many times a user's invites have been used"""
        async with ctx.typing():
            if user == None:
                user = ctx.author
            else:
                user = user
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    total_invites += i.uses
            embed = discord.Embed(title="📫 Invite counter")
            embed.add_field(
                name=f"​​​​​Invites for {user.name}#{user.discriminator}",
                value=f"{total_invites} times!",
            )
            await ctx.send(embed=embed)

    # Invite tracking

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        """On member listener for new users"""
        logs_channel = await self.config.guild(member.guild).channel()
        logs = self.bot.get_channel(logs_channel)
        embed = discord.Embed(
            description="Just joined the server", color=0x03D692, title=" "
        )
        embed.set_author(name=str(member), icon_url=member.avatar_url)
        embed.set_footer(text="ID: " + str(member.id))
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses < self.find_invite_by_code(invs_after, invite.code).uses:
                    embed.add_field(
                        name="Used invite",
                        value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\nCode: `{invite.code}`\nUses: ` {str(invite.uses)} `",
                        inline=False,
                    )
        except Exception as e:
            print(str(e))
        if (
            self.config.guild(member.guild).enabled
            and self.config.guild(member.guild).joinenabled
        ):
            await logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        """On member listener for users leaving"""
        logs_channel = await self.config.guild(member.guild).channel()
        logs = self.bot.get_channel(int(logs_channel))
        embed = discord.Embed(
            description="Just left the server", color=0xFF0000, title=" "
        )
        embed.set_author(name=str(member), icon_url=member.avatar_url)
        embed.set_footer(text="ID: " + str(member.id))
        embed.timestamp = member.joined_at
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses > self.find_invite_by_code(invs_after, invite.code).uses:
                    embed.add_field(
                        name="Used invite",
                        value=f"Inviter: {invite.inviter.mention} (`{invite.inviter}` | `{str(invite.inviter.id)}`)\nCode: `{invite.code}`\nUses: ` {str(invite.uses)} `",
                        inline=False,
                    )
        except Exception as e:
            print(str(e))
        if (
            self.config.guild(member.guild).enabled
            and self.config.guild(member.guild).joinenabled
        ):
            await logs.send(embed=embed)
