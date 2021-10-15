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
]


class AdvancedEconomy(commands.Cog):
    """
    An advanced economy cog.
    """

    __version__ = "1.0.0"

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
            "next_payday": int(datetime.datetime.now().timestamp()),
        }
        self.config.register_global(**default_global)
        self.config.register_member(**default_user)
        self.startup_task = self.bot.loop.create_task(self.startup())

    def cog_unload(self):
        self.startup_task.cancel()

    async def startup(self):
        await bank.set_global(True)

    async def red_delete_data_for_user(
        self, *, requester: RequestType, user_id: int
    ) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.Cog.listener()
    async def on_cog_load(self):
        await bank.set_global(True)
        pass

    @commands.group()
    @commands.guild_only()
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
        await self.config.default_payday.set(amount)
        await ctx.tick()

    @economyset.command()
    async def setcreditname(self, ctx: commands.Context, credit_name):
        """
        Set the credit name

        Default: `credits`
        """
        await bank.set_currency_name(credit_name)
        await ctx.tick()

    @economyset.command()
    async def setmaxbal(self, ctx: commands.Context, amount: int):
        """
        Set the maximum balance allowed
        """
        await bank.get_max_balance(amount)
        await ctx.tick()

    @economyset.command()
    async def setbankname(self, ctx: commands.Context, *, bank_name):
        """
        Set bank name

        Default: `First Bank of Red`
        """
        await bank.set_bank_name(bank_name)
        await ctx.tick()

    @economyset.command()
    async def setcooldown(self, ctx: commands.Context, cooldown: int):
        """
        Set cooldown (in seconds)

        Default: `300`
        """
        await self.config.payday_cooldown.set(cooldown)
        await ctx.tick()

    @commands.command()
    @commands.guild_only()
    async def payday(self, ctx: commands.Context):
        """
        Get daily money
        """

        if await self.config.member(
            ctx.author
        ).next_payday() == None or await self.config.member(
            ctx.author
        ).next_payday() <= int(
            datetime.datetime.now().timestamp()
        ):
            currency = await self.config.default_payday()
            next_payday_config = await self.config.payday_cooldown()
            next_payday = int(datetime.datetime.now().timestamp()) + next_payday_config
            credit_name = await bank.get_currency_name()
            current_bal = await bank.get_balance(ctx.author)
            await bank.deposit_credits(amount=currency, member=ctx.author)
            embed = discord.Embed(title="PAYDAY!! 🤑💰🤑", color=await ctx.embed_color())
            embed.add_field(
                name="It's time to get paid!",
                value=f"You just earned {currency} {credit_name}! \n\nYour new balance is: {current_bal} {credit_name}\n\nCome back <t:{next_payday}:R> to claim more money!",
                inline=False,
            )
            embed.set_footer(text="💸💸")
            await ctx.send(embed=embed)
            await self.config.member(ctx.author).next_payday.set(next_payday)
            return

        if await self.config.member(ctx.author).next_payday() >= int(
            datetime.datetime.now().timestamp()
        ):
            currency = await self.config.default_payday()
            next_payday = await self.config.member(ctx.author).next_payday()
            credit_name = await self.config.credits_name()
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
    @commands.guild_only()
    async def work(self, ctx):
        """
        Work at a job and gain/lose some currency.
        """
        range = random.randint(10, 1000)
        random_index = random.choice(_JOBS)
        credit_name = await bank.get_currency_name()
        message = await ctx.send(
            random_index.replace("{amount}", str(range)).replace(
                "{credit_name}", credit_name
            )
        )
        if "lose" in message.content:
            await bank.withdraw_credits(amount=range, member=ctx.author)
            message
        else:
            await bank.deposit_credits(amount=range, member=ctx.author)
