from typing import Literal

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config

# MySQL
import mysql.connector

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class SQL(commands.Cog):
    """
    SQL experiment og
    """

    

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=572944636209922059,
            force_registration=True,
        )
        self.startup_task = self.bot.loop.create_task(self.startup())

    async def startup(self):
        mysql_cred = await self.bot.get_shared_api_tokens("mysql")
        self.sqql = mysql.connector.connect(user=mysql_cred.get("username"), password=mysql_cred.get("password"), database="")
        self.cursorr = self.sqql.cursor()
        self.cursorr.execute("SET @@wait_timeout = 31536000")

    def cog_unload(self):
        self.startup_task.cancel()
    
    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)
    
    
    @commands.is_owner()
    @commands.group()
    async def sql(self, ctx):
        """SQL commands"""
        pass

    @sql.group()
    async def mysql(self, ctx):
        """MySQL commands"""
        pass

    @mysql.group()
    async def delete(self, ctx):
        """Delete database/table"""

    @mysql.command()
    async def create(self, ctx, database_name):
        """Create a database with MySQL"""
        await ctx.trigger_typing()
        self.cursorr.execute(f"CREATE DATABASE {database_name}")
        await ctx.tick()
        await ctx.send(f"{database_name} has been created.")

    @mysql.command()
    async def list(self, ctx):
        """List databases in MySQL"""
        await ctx.trigger_typing()
        databases = ("show databases")
        self.cursorr.execute(databases)
        embed = discord.Embed(title="MySQL Databases", description="Here are the databases that your have on your machine:")
        embed.add_field(name="Databases:", value=", ".join(x for (x,) in self.cursorr))
        embed.set_footer(text="MySQL")
        await ctx.send(embed=embed)

    @delete.command(aliases=["database"])
    async def db(self, ctx , database_name):
        """Remove database"""
        await ctx.trigger_typing()
        self.cursorr.execute(f"DROP DATABASE IF EXISTS {database_name}")
        await ctx.tick()
        await ctx.send("If the database exists, it has been removed.")
            
    

