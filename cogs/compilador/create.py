import discord
from discord.ext import commands
from discord import app_commands
import io
import contextlib
import re

# Isso é um "banco de dados" na memória. 
# Atenção: Se o bot reiniciar, os arquivos salvos aqui somem!
arquivos_salvos = {}

class Compilador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- COMANDO /CREATE ---
    @app_commands.command(name="create", description="Salva um código Python na memória do bot.")
    async def create(self, interaction: discord.Interaction, nome_arquivo: str, codigo: str):
        # Essa mágica aqui remove as crases e o "py" que o usuário manda no markdown do Discord
        codigo_limpo = re.sub(r"^```(py|python)?|```$", "", codigo.strip(), flags=re.MULTILINE).strip()

        # Salva o código limpo no nosso dicionário usando o nome do arquivo
        arquivos_salvos[nome_arquivo] = codigo_limpo

        # Cria um Embed bonitão confirmando a criação
        embed = discord.Embed(
            title="📄 Arquivo Criado",
            description=f"O arquivo `{nome_arquivo}.py` foi salvo temporariamente!",
            color=discord.Color.green()
        )
        # Mostra uma prévia do código salvo (limite de 1000 caracteres pra não quebrar o embed)
        embed.add_field(name="Seu Código:", value=f"```py\n{codigo_limpo[:1000]}\n```", inline=False)
        
        await interaction.response.send_message(embed=embed)


    # --- COMANDO /RUN ---
    @app_commands.command(name="run", description="Executa um arquivo salvo anteriormente.")
    async def run(self, interaction: discord.Interaction, nome_arquivo: str):
        # Verifica se o arquivo existe na memória
        if nome_arquivo not in arquivos_salvos:
            return await interaction.response.send_message(f"❌ O arquivo `{nome_arquivo}` não foi encontrado. Use o /create primeiro!", ephemeral=True)

        # Pega o código salvo
        codigo = arquivos_salvos[nome_arquivo]

        # Prepara um espaço falso no console para capturar os "prints"
        saida_console = io.StringIO()
        erro = None

        try:
            # Tudo que o código printar, vai ser redirecionado para a variável 'saida_console'
            with contextlib.redirect_stdout(saida_console):
                # EXEC() RODA O CÓDIGO. (Muito cuidado com isso em bots públicos!)
                exec(codigo, {})
        except Exception as e:
            # Se o código do usuário tiver erro (ex: faltou fechar parênteses), capturamos aqui
            erro = str(e)

        # Pega o texto gerado
        resultado = saida_console.getvalue()

        # Monta o Embed de resposta
        embed = discord.Embed(title=f"▶️ Executando: `{nome_arquivo}.py`", color=discord.Color.blue())
        
        if erro:
            embed.add_field(name="⚠️ Erro no Código", value=f"```py\n{erro}\n```", inline=False)
            embed.color = discord.Color.red()
        elif resultado:
            embed.add_field(name="🖥️ Saída (Console)", value=f"```txt\n{resultado[:1000]}\n```", inline=False)
        else:
            embed.add_field(name="🖥️ Saída (Console)", value="```txt\n[Nenhuma saída. Você esqueceu de usar print?]\n```", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Compilador(bot))