import json
from pathlib import Path

from redbot.core.bot import Red

from .serverping import ServerPing

with open(Path(__file__).parent / "info.json") as fp:

    async def setup(bot: Red) -> None:
        bot.add_cog(ServerPing(bot))
