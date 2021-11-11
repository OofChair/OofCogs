from typing import Literal, Optional

import discord
from discord.ext.commands.core import cooldown
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
import datetime
from redbot.core import bank
import random

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

_JOBS = [
    "You work at McRonalds serving fries and gain {amount} {credit_name}.",
    "You work at McRonalds frying chicken and gain {amount} {credit_name}.",
    "You work at McRonalds serving burgers and gain {amount} {credit_name}.",
    "You work at Worst Buy selling phones and gain {amount} {credit_name}.",
    "You work at Worst Buy selling computers and gain {amount} {credit_name}.",
    "You work at Worst Buy selling monitors and gain {amount} {credit_name}.",
    "You work at Worst Buy selling keyboards and gain {amount} {credit_name}.",
    "You work at Alti selling blush and gain {amount} {credit_name}.",
    "You work at Alti selling lipstick and gain {amount} {credit_name}.",
    "You work at Alti selling eyeshadow and gain {amount} {credit_name}.",
    "You work with aikaterna on Audio and earn {amount} {credit_name} for dealing with Java.",
    "You work with Slime and get... slimed. Gain {amount} {credit_name} for having to deal with that.",
    "You host Red on Heroku and lose {amount}.",
    "You try to host Red on repl.it and lose {amount} {credit_name}.",
]


class AdvancedEconomy(commands.Cog):
    """
    An advanced economy cog.
    """

    __version__ = "1.0.1"

    def format_help_for_context(self, ctx):
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        n = "\n" if "\n\n" not in pre_processed else ""
        return f"{pre_processed}{n}\nCog Version: {self.__version__}"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=572944636209922059,
            force_registration=True,
        )
        default_global = {
            "default_payday": 500,
            "payday_cooldown": 300,
        }
        default_user = {
            "next_payday": 0,
        }
        self.config.register_global(**default_global)
        self.config.register_user(**default_user)
        self.startup_task = self.bot.loop.create_task(self.startup())

    def cog_unload(self):
        self.startup_task.cancel()

    async def startup(self):
        await bank.set_global(True)

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        return

    @commands.group()
    @commands.guild_only()
    @commands.is_owner()
    async def economyset(self, ctx):
        """
        Economy and bank settings
        """
        pass

    @economyset.command()
    async def setpayday(self, ctx: commands.Context, amount: int) -> None:
        """
        Set the default payday amount.

        Default: `500`
        """
        # Add amount arg to config
        if amount <= 0:
            await ctx.send("This value can't be set below 0.")
        else:
            await self.config.default_payday.set(amount)
            await ctx.tick()

    @economyset.command()
    async def setcooldown(self, ctx: commands.Context, cooldown: int):
        """
        Set cooldown (in seconds)

        Default: `300`
        """
        if cooldown <= 0:
            await ctx.send("This value can't be set below 0.")
        else:
            await self.config.payday_cooldown.set(cooldown)
            await ctx.tick()

    @economyset.command()
    async def about(self, ctx):
        """
        How to set other settings not found here
        """
        embed = discord.Embed(title="AdvancedEconomy")
        embed.add_field(
            name="How do I set more commands??",
            value="More commands, such as setting the credit name, bank name, and setting t he maximum balance a user can have, are located in the Bank cog. Do not change the `bankset setglobal` value, as this will cause problems with AdvancedEconomy.",
            inline=False,
        )
        embed.add_field(
            name="How do I get to the Bank cog?",
            value=f"You can load the Bank cog with `{ctx.prefix}load bank`. ",
            inline=False,
        )
        embed.set_footer(text="AdvancedEconomy")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def payday(self, ctx: commands.Context):
        """
        Get daily money
        """
        if await self.config.user(
            ctx.author
        ).next_payday() == None or await self.config.user(
            ctx.author
        ).next_payday() <= int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        ):
            currency = await self.config.default_payday()
            next_payday_config = await self.config.payday_cooldown()
            next_payday = (
                int(datetime.datetime.now(datetime.timezone.utc).timestamp())
                + next_payday_config
            )
            credit_name = await bank.get_currency_name()
            current_bal = await bank.get_balance(ctx.author)
            try:
                await bank.deposit_credits(amount=currency, member=ctx.author)
            except bank.errors.BalanceTooHigh as e:
                await bank.set_balance(ctx.author, e.max_balance)
            current_bal = await bank.get_balance(ctx.author)
            msg = (
                f"You just earned {currency} {credit_name}!\n\n"
                f"You new balance is {current_bal} {credit_name}\n\nCome back <t:{next_payday}:R> to claim more money!"
            )
            if await ctx.embed_requested():
                embed = discord.Embed(
                    title="PAYDAY!! 🤑💰🤑", color=await ctx.embed_color()
                )
                embed.add_field(
                    name="It's time to get paid!",
                    value=msg,
                    inline=False,
                )
                embed.set_footer(text="💸💸")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"**Payday!!**\n\n{msg}")
            await self.config.user(ctx.author).next_payday.set(next_payday)
            return

        if await self.config.user(ctx.author).next_payday() >= int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        ):
            currency = await self.config.default_payday()
            next_payday = await self.config.user(ctx.author).next_payday()
            current_bal = await bank.get_balance(ctx.author)
            await ctx.send(
                f"Sorry, you can't redeem your payday yet! You can redeem your next payday <t:{next_payday}:R>."
            )
            return

    @commands.command(aliases=["bal"])
    @commands.guild_only()
    async def balance(self, ctx):
        """
        Get your bank balance.
        """
        current_bal = await bank.get_balance(ctx.author)
        credit_name = await bank.get_currency_name()
        await ctx.send(f"{ctx.author.mention}, your balance is {current_bal} ")

    @commands.command(aliases=["job"])
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.guild_only()
    async def work(self, ctx):
        """
        Work at a job and gain/lose some currency.
        """
        _range = random.randint(10, 1000)
        random_index = random.choice(_JOBS)
        credit_name = await bank.get_currency_name()
        message = await ctx.send(
            random_index.format(amount=str(_range), credit_name=credit_name)
        )
        if "lose" in message.content:
            try:
                await bank.withdraw_credits(amount=_range, member=ctx.author)
                message
            except ValueError:
                await ctx.send(
                    "You would've lost money on this payday, but you have nothing to lose! "
                )
                await bank.set_balance(member=ctx.author, amount=0)
        else:
            try:
                await bank.deposit_credits(amount=_range, member=ctx.author)
            except bank.errors.BalanceTooHigh as e:
                await bank.set_balance(ctx.author, e.max_balance)
