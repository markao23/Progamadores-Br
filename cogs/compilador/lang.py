import discord
from discord.ext import commands
from discord import app_commands

class Langs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="langs", description="Lista todas as linguagens suportadas pelo compilador do bot.")
    async def langs(self, interaction: discord.Interaction):
        # Cria a base do Embed (Título, descrição e cor da barra lateral)
        embed = discord.Embed(
            title="🌐 Linguagens Suportadas",
            description="Aqui estão todas as linguagens que nosso compilador consegue executar. Use o comando de compilação para testar seus códigos diretamente no chat!",
            color=discord.Color.blurple() # Uma cor azul-arroxeada clássica do Discord
        )

        # Categoria 1: Linguagens Populares / Scripting
        embed.add_field(
            name="📜 Populares & Scripting",
            value=(
                "▫️ `python` - Python 3\n"
                "▫️ `javascript` - Node.js\n"
                "▫️ `typescript` - TypeScript\n"
                "▫️ `ruby` - Ruby\n"
                "▫️ `php` - PHP"
            ),
            inline=True # inline=True faz as colunas ficarem lado a lado
        )

        # Categoria 2: Linguagens Compiladas (Tipagem Forte)
        embed.add_field(
            name="⚙️ Compiladas",
            value=(
                "▫️ `c` - GCC C\n"
                "▫️ `cpp` - C++\n"
                "▫️ `java` - Java\n"
                "▫️ `csharp` - C# (.NET)\n"
                "▫️ `rust` - Rust\n"
                "▫️ `go` - Golang"
            ),
            inline=True
        )

        # Quebra de linha invisível para organizar o layout (opcional, mas fica bonito)
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        # Categoria 3: Outras / Funcionais
        embed.add_field(
            name="🛠️ Outras Ferramentas",
            value=(
                "▫️ `lua` - Lua\n"
                "▫️ `kotlin` - Kotlin\n"
                "▫️ `swift` - Swift\n"
                "▫️ `bash` - Shell Script\n"
                "▫️ `haskell` - Haskell"
            ),
            inline=True
        )

        # Rodapé do Embed com uma dica
        embed.set_footer(
            text="Dica: Use a sintaxe markdown do Discord com a sigla correta para compilar!",
            icon_url=self.bot.user.display_avatar.url
        )

        # Envia a mensagem respondendo a interação
        await interaction.response.send_message(embed=embed)

# Função obrigatória para carregar a Cog
async def setup(bot):
    await bot.add_cog(Langs(bot))