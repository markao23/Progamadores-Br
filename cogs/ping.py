import discord
from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # O decorador app_commands.command transforma isso num Slash Command (/)
    @app_commands.command(name="ping", description="Mostra a latência do bot e da API.")
    async def ping(self, interaction: discord.Interaction):
        # bot.latency retorna em segundos (ex: 0.15). Multiplicamos por 1000 para virar milissegundos (ms)
        latencia = round(self.bot.latency * 1000)

        # Responde a interação
        await interaction.response.send_message(
            f"🏓 Pong! Minha latência atual é de **{latencia}ms**."
        )


# Função obrigatória para o main.py conseguir carregar esse arquivo
async def setup(bot):
    await bot.add_cog(Ping(bot))
