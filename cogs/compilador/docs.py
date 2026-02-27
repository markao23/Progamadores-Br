import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import urllib.parse

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Criando o comando com opções de escolha (Choices)
    @app_commands.command(name="docs", description="Pesquisa documentações oficiais (MDN, Python, etc).")
    @app_commands.choices(linguagem=[
        app_commands.Choice(name="🌐 JavaScript / HTML / CSS (MDN)", value="mdn"),
        app_commands.Choice(name="🐍 Python 3", value="python")
    ])
    async def docs(self, interaction: discord.Interaction, linguagem: app_commands.Choice[str], pesquisa: str):
        
        # ⚠️ IMPORTANTE: Como vamos buscar na internet, pode demorar mais de 3 segundos.
        # O defer() avisa o Discord: "Espera aí que eu tô pensando!" para não dar erro de "Aplicativo não respondeu"
        await interaction.response.defer()

        # --- BUSCA NA MDN (WEB/JS) ---
        if linguagem.value == "mdn":
            # Formata o texto para URL (ex: "Array map" vira "Array%20map")
            query_formatada = urllib.parse.quote(pesquisa)
            url_api = f"https://developer.mozilla.org/api/v1/search?q={query_formatada}"

            # Faz a requisição na API da MDN
            async with aiohttp.ClientSession() as session:
                async with session.get(url_api) as resposta:
                    if resposta.status == 200:
                        dados = await resposta.json()
                        
                        # Se encontrou algum resultado
                        if dados.get('documents'):
                            primeiro_resultado = dados['documents'][0]
                            
                            embed = discord.Embed(
                                title=f"📚 MDN: {primeiro_resultado['title']}",
                                url=f"https://developer.mozilla.org{primeiro_resultado['mdn_url']}",
                                description=primeiro_resultado.get('summary', 'Resumo não disponível.'),
                                color=discord.Color.yellow()
                            )
                            embed.set_footer(text="Fonte: MDN Web Docs")
                            
                            # Usamos followup.send porque já usamos o defer() lá em cima
                            await interaction.followup.send(embed=embed)
                        else:
                            await interaction.followup.send(f"❌ Não encontrei nenhum resultado na MDN para `{pesquisa}`.")
                    else:
                        await interaction.followup.send("⚠️ A API da MDN está fora do ar no momento.")

        # --- BUSCA NO PYTHON ---
        elif linguagem.value == "python":
            query_formatada = urllib.parse.quote(pesquisa)
            link_pesquisa = f"https://docs.python.org/3/search.html?q={query_formatada}"
            
            embed = discord.Embed(
                title=f"🐍 Documentação Python: {pesquisa}",
                url=link_pesquisa,
                description=f"Clique no título azul acima para ver os resultados oficiais de **`{pesquisa}`** na documentação do Python 3.",
                color=discord.Color.blue()
            )
            embed.set_footer(text="Fonte: Python Docs")
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Docs(bot))