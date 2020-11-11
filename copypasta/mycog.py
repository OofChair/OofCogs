from redbot.core import commands
import discord
class Copypasta(commands.Cog):
    """Random fun commands"""

    @commands.command()
    async def behappy(self, ctx):
        """Test command"""
        # Your code will go here
        embed=discord.Embed(title="Hi! I'm Oofchair - Experimental Edition :D", description="undefined?", color=0xff0000)
        embed.set_thumbnail(url="https://s.yimg.com/ny/api/res/1.2/12UU2JphAsbxTTDca.7QFQ--~A/YXBwaWQ9aGlnaGxhbmRlcjtzbT0xO3c9MTA4MDtoPTcxNg--/https://media-mbst-pub-ue1.s3.amazonaws.com/creatr-uploaded-images/2019-11/7b5b5330-112b-11ea-a77f-7c019be7ecae")
        embed.add_field(name="", value="", inline=False)
        embed.set_footer(text="OofChair - Experimental Edition")
        await ctx.send(embed=embed)
