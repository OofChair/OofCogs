from redbot.core import commands

class Copypasta(commands.Cog):
    """Random fun commands"""

    @commands.command()
    async def behappy(self, ctx):
        """Rickroll your friends!"""
        # Your code will go here
        embed=discord.Embed(title="Tile", description="Desc", color=0x00ff00)
embed.add_field(name="Fiel1", value="hi", inline=False)
embed.add_field(name="Field2", value="hi2", inline=False)
await self.bot.say(embed=embed)
