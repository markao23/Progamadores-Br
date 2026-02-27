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
        for root, dirs, files in os.walk("./cogs"):
            for filename in files:
                if filename.endswith(".py"):
                    caminho_completo = os.path.join(root, filename)
                    modulo = (
                        caminho_completo.replace("./", "")
                        .replace(".py", "")
                        .replace("\\", ".")
                        .replace("/", ".")
                    )
                    await self.load_extension(modulo)
                    print(f"✅ Cog carregada: {filename}")
            await self.tree.sync()
            print("🌍 Comandos de barra sincronizados!")


bot = MeuBot()


@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")


bot.run(token)
