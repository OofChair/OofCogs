from .commands import Commands


def setup(bot):
    cog = Commands(bot)
    bot.add_cog(cog)
