import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import urllib.parse
import traceback # <-- Biblioteca essencial para caçar bugs!

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="docs", description="Pesquisa documentações oficiais (MDN, Python, etc).")
    @app_commands.choices(linguagem=[
        app_commands.Choice(name="🌐 JavaScript / HTML / CSS (MDN)", value="mdn"),
        app_commands.Choice(name="🐍 Python 3", value="python")
    ])
    async def docs(self, interaction: discord.Interaction, linguagem: app_commands.Choice[str], pesquisa: str):
        # LOG 1: Saber se o bot pelo menos recebeu o comando
        print(f"\n▶️ [LOG] Comando /docs acionado por {interaction.user.name} (Lang: {linguagem.value} | Busca: {pesquisa})")
        
        try:
            # LOG 2: Tentar deferir (avisar o Discord para esperar)
            print("⏳ [LOG] Tentando deferir a interação...")
            await interaction.response.defer()
            print("✅ [LOG] Interação deferida com sucesso!")

            # --- BUSCA NA MDN (WEB/JS) ---
            if linguagem.value == "mdn":
                print("🔍 [LOG] Iniciando bloco da MDN...")
                query_formatada = urllib.parse.quote(pesquisa)
                url_api = f"https://developer.mozilla.org/api/v1/search?q={query_formatada}"
                print(f"🌐 [LOG] URL de busca: {url_api}")

                async with aiohttp.ClientSession() as session:
                    async with session.get(url_api) as resposta:
                        print(f"📡 [LOG] Status da requisição HTTP: {resposta.status}")
                        if resposta.status == 200:
                            dados = await resposta.json()
                            print("📦 [LOG] JSON lido com sucesso!")
                            
                            if dados.get('documents'):
                                primeiro_resultado = dados['documents'][0]
                                print(f"📄 [LOG] Resultado encontrado: {primeiro_resultado.get('title')}")
                                
                                embed = discord.Embed(
                                    title=f"📚 MDN: {primeiro_resultado['title']}",
                                    url=f"https://developer.mozilla.org{primeiro_resultado['mdn_url']}",
                                    description=primeiro_resultado.get('summary', 'Resumo não disponível.'),
                                    color=discord.Color.yellow()
                                )
                                embed.set_footer(text="Fonte: MDN Web Docs")
                                
                                await interaction.followup.send(embed=embed)
                                print("✅ [LOG] Mensagem enviada com sucesso pro Discord!")
                            else:
                                print("⚠️ [LOG] Nenhum documento na MDN.")
                                await interaction.followup.send(f"❌ Não encontrei nenhum resultado na MDN para `{pesquisa}`.")
                        else:
                            print("❌ [LOG] A API da MDN retornou um erro.")
                            await interaction.followup.send("⚠️ A API da MDN está fora do ar no momento.")

            # --- BUSCA NO PYTHON ---
            elif linguagem.value == "python":
                print("🔍 [LOG] Iniciando bloco do Python...")
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
                print("✅ [LOG] Mensagem enviada com sucesso pro Discord!")

        except Exception as e:
            # SE QUALQUER COISA DER ERRO, O CÓDIGO CAI AQUI!
            print("\n❌ [ERRO CRÍTICO NO /DOCS] ❌")
            traceback.print_exc() # Imprime a linha exata e o motivo do erro no terminal
            print("---------------------------------\n")
            
            # Tenta avisar o usuário que deu erro para a mensagem vermelha não aparecer
            try:
                if interaction.response.is_done():
                    await interaction.followup.send(f"⚠️ Vish, deu um erro interno no bot: `{e}`", ephemeral=True)
                else:
                    await interaction.response.send_message(f"⚠️ Vish, deu um erro interno no bot: `{e}`", ephemeral=True)
            except:
                pass # Se falhar ao avisar, apenas segue o baile

async def setup(bot):
    await bot.add_cog(Docs(bot))