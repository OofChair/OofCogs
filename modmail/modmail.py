from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import asyncio
import discord
from cogs.utils import checks
from discord.ext import commands
from __main__ import send_cmd_help
import json
import os
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Modmail(commands.Cog):
    """
    Modmail cog, ported from Bakersbakebread/Bread-Cogs
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


menu = {
    "reply": "📩",
    "delete": "❌"
}



class ModMail:

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/modmail/settings.json')
        self.set_server = self.bot.get_channel(self.settings["channel"])
        self.ignored_users = dataIO.load_json("data/modmail/ignoredlist.json")

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        author = message.author

        if isinstance(message.channel, discord.PrivateChannel):
            if author.id in self.ignored_users["ignored"]:
                print("Ignored user")
                return

            for server in self.bot.servers:
                member = server.get_member(author.id)
                if member:
                    author = member
                break  # this is checking for silly nicknames.

            if isinstance(author, discord.Member) and author.nick:
                author_name = '{0.nick} ({0})'.format(author)
            else:
                author_name = str(author)
            embed = discord.Embed(
                color=0xff0000,
                description=message.content
                )
            embed.set_author(
                name=(author_name),
                icon_url=author.avatar_url if author.avatar else author.default_avatar_url)
            embed.set_footer(text="User ID: {}".format(author.id))

            if message.attachments:
                attachment_urls = []
                for attachment in message.attachments:
                    attachment_urls.append('[{}]({})'.format(attachment['filename'], attachment['url']))
                attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} s '.join(attachment_urls)
                embed.add_field(
                    name='Attachments',
                    value=attachment_msg,
                    inline=False
                    )
            mothership = await self.bot.send_message(self.set_server, embed=embed)
            await self.bot.add_reaction(mothership, "📩")
            await self.bot.add_reaction(mothership, "❌")

            def check(reaction, user): # thanks 26
                return not user.bot

            react = await self.bot.wait_for_reaction(emoji=["📩", "❌"], message=mothership, check=check)
            reacts = {v: k for k, v in menu.items()}
            react = reacts[react.reaction.emoji]
            if react == "reply":
                embed.add_field(name=":envelope_with_arrow:", value="Message marked as replied.")
                await self.bot.edit_message(mothership, new_content=None, embed=embed)
                try:
                    await self.bot.clear_reactions(mothership)
                except Exception as e:
                    print("Couldn't clear reactions on modmail (No Permissions)")

            elif react == "delete":
                await self.bot.delete_message(mothership)

    @checks.admin_or_permissions(manager_server=True)
    @commands.group(pass_context=True)
    async def modmail(self, ctx):
        """All messages sent to the bot will go to set channel."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @checks.admin_or_permissions(manager_server=True)
    @modmail.command(pass_context=True)
    async def reply(self, ctx, user: discord.Member=None, *, message):
        """Reply to a message, logs to set channel."""
        if user is None:
            user = ctx.message.mention

        member = ctx.message.author
        if member:
            embed = discord.Embed(color=0x00c100, description=message)
            to_send = '{}: '.format(member.name)
            to_send += message
            myMilkshake = '{0.name} replied to:  {1.name} {1.id} '.format(member, user)
            if member.id in self.ignored_users["ignored"]:
                    myMilkshake += ' (replies ignored)'
            embed.set_footer(text=myMilkshake,
                icon_url="https://emojipedia-us.s3.amazonaws.com/thumbs/60/emoji-one/44/envelope_2709.png")
            try:
                await self.bot.send_message(user, to_send)
                await self.bot.send_message(self.set_server, embed=embed)
                try:
                    await self.bot.delete_message(ctx.message)
                except discord.errors.Forbidden:
                    pass
            except discord.errors.InvalidArgument:
                await self.bot.say("No modmail channel has been set-up.")
            except discord.errors.Forbidden:
                await self.bot.send_message(self.set_server,
                    '{0} {1.mention} is not in a shared server, or has disabled DM\'s'
                    .format(user.mention, member))

    @checks.admin_or_permissions(manager_server=True)
    @modmail.command(pass_context=True)
    async def ignore(self, ctx, user: discord.Member, *, reason=None):
        """Add a user to the ignore list.

        Example: ?modmail ignore @BakersBakeBread Spamming"""
        if user.id not in self.ignored_users["ignored"]:
            if reason is None:
                reason = "Reason not specified"
            self.ignored_users["ignored"].append(user.id)

            dataIO.save_json("data/modmail/ignoredlist.json", self.ignored_users)
             #should store this in a func
            embed = discord.Embed(
                title=':no_bell: {0} is now ignored.'.format(user),
                description= "`User id: {}\nReason: {}` ".format(user.id, reason),
                color=0xff8040)
            embed.set_footer(
                text="Ignored by: {}".format(ctx.message.author))
            await self.bot.send_message(self.set_server, embed=embed)

        else:
            await self.bot.send_message(self.set_server,
                ':no_bell: {} is already ignored.'.format(user.mention))
        try:
            await self.bot.delete_message(ctx.message) # delete command message to leave just modmail
        except discord.errors.Forbidden:
            pass

    @checks.admin_or_permissions(manager_server=True)
    @modmail.command(pass_context=True)
    async def channel(self, ctx, channel:discord.Channel=None):
        """Set the channel modmail will be sent too"""

        if channel is None:
            channel = ctx.message.channel
        self.settings["channel"] = channel.id
        self.set_server = self.bot.get_channel(self.settings["channel"])
        dataIO.save_json("data/modmail/settings.json", self.settings)
        try:
            await self.bot.send_message(channel, "I will send modmail here.")
        except discord.errors.Forbidden:
            await self.bot.send_message(channel,
                "I need the \"Embed Links\" permission to send messages here.")

    @checks.admin_or_permissions(manager_server=True)
    @modmail.command(pass_context=True)
    async def unignore(self, ctx, user: discord.Member):
        """Removes user from ignore list.

        Example: ?modmail unignore @BakersBakeBread"""
        author = ctx.message.author
        if user.id in self.ignored_users["ignored"]:
            self.ignored_users["ignored"].remove(user.id)
            dataIO.save_json("data/modmail/ignoredlist.json", self.ignored_users)
            embed = discord.Embed(
                title=':bell: {0} has been removed from the ignore list.'.format(user),
                description= "`User id: {}` ".format(user.id),
                color=0xff8040)
            embed.set_footer(text="Unignored by: {}".format(author))
            await self.bot.send_message(self.set_server, embed=embed)

        else:
            await self.bot.send_message(
                self.set_server, ("{} `{}` is not ignored.").format(user.mention, user.id))

    @checks.admin_or_permissions(manager_server=True)
    @modmail.command(name="list")
    async def _list(self):
        """A list of users ignored in ModMail"""
        ignorelist = self._makelist(self.ignored_users["ignored"])

        if ignorelist:
            for page in ignorelist:
                embed = discord.Embed(
                    title="Ignored Users:",
                    description=page,)
                await self.bot.say(embed=embed)
        else:
            await self.bot.say("There is no-one on the ignore list..")

    def _makelist(self, _list):
        users = []
        total = len(_list)

        for user_id in _list:
            user = discord.utils.get(self.bot.get_all_members(), id=user_id)
            if user:
                users.append(":no_bell: **" + str(user) + "**")

        if users:
            not_found = total - len(users)
            users = "\n".join(users)
            if not_found:
                users += "\n\n ... and {} users I could not find".format(not_found)
            return list(pagify(users, delims=[" ", "\n"]))

        return []
def check_folder():
    if not os.path.exists('data/modmail'):
        print('Creating modmail folder...')
        os.makedirs('data/modmail')

def check_files():
    if not os.path.exists("data/modmail/ignoredlist.json"):
        print("Creating empty ignores.json...")
        data = {"ignored": []}

        dataIO.save_json("data/modmail/ignoredlist.json", data)
    if not os.path.exists("data/modmail/settings.json"):
        print("Creating settings.json...")
        data = {"channel": " "}

        dataIO.save_json("data/modmail/settings.json", data)

def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(ModMail(bot))
