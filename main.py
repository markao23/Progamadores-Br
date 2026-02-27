import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
token = os.getenv("TOKEN")


class MeuBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="P!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog carregada: {filename}")
        await self.tree.sync()
        print("🌍 Comandos de barra sincronizados!")


bot = MeuBot()


@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")


bot.run(token)
