from redbot.core import commands
import discord
class Copypasta(commands.Cog):
    """Random fun commands"""

    @commands.command()
    async def behappy(self, ctx):
        """Test command"""
        # Your code will go here
        embed=discord.Embed(title="Be Happy by Dixie D'amelio", color=0xff0000)
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/e/e7/Dixie_D%27Amelio_-_Be_Happy.png/220px-Dixie_D%27Amelio_-_Be_Happy.png")
        embed.add_field(name="ᗷᕼᑌᗴᔕᒍYᗴᔕ", value="\nᗷᕼᑌᗴᔕᒍYᗴᔕ 🤷sometimes✨i🙁don't😢wanna😱be😼happy🧚don't✋hold😇it🤪against😈me🙆", inline=False)
        embed.add_field(name="Link:", value="[Be Happy Music Video](https://www.youtube.com/watch?v=wKOptbo-QFw)")
        embed.set_footer(text="(c) DAM FAM Records")
        await ctx.send(embed=embed)
