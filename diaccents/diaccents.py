from typing import Literal

import discord
import dcl

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class Diaccents(commands.Cog):
    """
    Diaccents = Diacritic + accents
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

    @commands.group(name="diaccents", aliases=["diac"], autohelp=True)
    async def diaccents(self, ctx: commands.Context) -> None:
        """
        Diaccents = Diacritic + accents
        """
        pass

    @diaccents.command(name="acute")
    async def diaccents_acute(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get an acute diacritic for a letter
        """
        try:
            accent = dcl.acute(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="breve")
    async def diaccents_breve(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a breve diacritic for a letter
        """
        try:
            accent = dcl.breve(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="caron")
    async def diaccents_caron(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a caron diacritic for a letter
        """
        try:
            accent = dcl.caron(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="cedilla")
    async def diaccents_cedilla(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a cedilla diacritic for a letter
        """
        try:
            accent = dcl.cedilla(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="circumflex")
    async def diaccents_circumflex(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a circumflex diacritic for a letter
        """
        try:
            accent = dcl.circumflex(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)
        
    @diaccents.command(name="diaresis")
    async def diaccents_diaresis(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a diaresis diacritic for a letter
        """
        try:
            accent = dcl.diaresis(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)


    @diaccents.command(name="grave")
    async def diaccents_grave(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a grave diacritic for a letter
        """
        try:
            accent = dcl.grave(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="macron")
    async def diaccents_macron(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a macron diacritic for a letter
        """
        try:
            accent = dcl.macron(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="ogonek")
    async def diaccents_ogonek(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get an ogonek diacritic for a letter
        """
        try:
            accent = dcl.ogonek(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="ring")
    async def diaccents_ring(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a ring diacritic for a letter
        """
        try:
            accent = dcl.ring(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="tilde")
    async def diaccents_tilde(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a tilde diacritic for a letter
        """
        try:
            accent = dcl.tilde(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)
    
    @diaccents.command(name="umlaut")
    async def diaccents_umlaut(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a umlaut diacritic for a letter
        """
        try:
            accent = dcl.umlaut(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)

    @diaccents.command(name="umlmac")
    async def diaccents_umlmac(self, ctx: commands.Context, *, letter: str) -> None:
        """
        Get a umlaut and macron diacritic for a letter
        """
        try:
            accent = dcl.umlaut_and_macron(letter)
        except dcl.errors.DiacriticError:
            await ctx.send("This diacritic does not work with this letter, please try another ")
        else:
            await ctx.send(accent)
