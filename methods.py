import discord
import os
from dotenv import load_dotenv
from conn_db import Connection
from utils import Utils

load_dotenv()

class Methods:
    cargos = {
        "python": 1007645678589186109,
        "react native": 1007666765892964442,
        "frontend": 1007645794683334687, #Temporariamente ta o cargo de HTML e CSS
        "javascript": 1007645747719712768,
        "php": 1007645637896061002,
        "c#": 1007645892028932107,
        "c++": 1007645941702070272,
        "sql": 1011484510333972562,
        "rust": 1062127941301059654,
        "java": 1011458824244305920,
        "windows": 1007914490806939649,
        "linux": 1007914480279224320,
        "mac": 1007914566371512320,
        "blue team": 1014284598693335170,
        "red team": 1014284532993753169,
        "html e css": 1007645794683334687,
        "purple team": 1014286037293482027,
        "busco emprego": 1007917610727387176,
        "contratante": 1011458921120153620,
        "notificacao e eventos": 1063667765099106356,
        "tab news": int(os.environ["TABNEWS_ROLE"])
    }
    
    selectSistemaOperacional = None
    selectRedBlueTeam = None
    choosed = None
    connector = Connection()
    utils = Utils()

    def __init__(self, bot=None):
        self.bot = bot
    
    async def givingRole(self, member, guild, idRole, dontRemove=False):
        role = guild.get_role(int(idRole))
        
        if not dontRemove:
            for r in member.roles:
                if r.id == role.id:
                    await member.remove_roles(role)
                    return False

        await member.add_roles(role)
        return True

    async def workingForFunctionsLanguages(self, interaction: discord.Interaction, word, dontRemove):
        Methods.utils.mensagemIniciacaoLinguagem(interaction.user, word, interaction.channel)
        self.workingForFunctions(interaction, word, dontRemove)
    
    async def workingForFunctions(self, interaction: discord.Interaction, word, dontRemove=False):
        guild = interaction.client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        if dontRemove:
            #Não remove
            if await self.givingRole(interaction.user, guild, self.cargos[word.lower()], dontRemove=True):
                await interaction.response.send_message(f"Cargo {word} adicionado", ephemeral=True)
            else:
                await interaction.response.send_message(f"Cargo {word} retirado", ephemeral=True)
        else:
            #Remove
            if await self.givingRole(interaction.user, guild, self.cargos[word.lower()]):
                await interaction.response.send_message(f"Cargo {word} adicionado", ephemeral=True)
            else:
                await interaction.response.send_message(f"Cargo {word} retirado", ephemeral=True)
    
    @classmethod
    async def messageLanguage(cls, linguagem: str):
        pass
    
    @classmethod
    async def init(cls, client, bot=None):
        if bot:
            await Methods.startCallbackCargosLinguagens(client, bot=bot)
        else:
            await Methods.startCallbackCargosLinguagens(client)
        await Methods.startCallbackRedBlueTeams(client)
        await Methods.startCallbackSistemaOperacional(client)
        await Methods.startCallbackProcuraEmprego(client)
        await Methods.startCallbackContratante(client)
        # await Methods.startCallbackEquipeFreelance(client)
        await Methods.starCallbackIdeiaProjeto(client)
        await Methods.startCallbackNotificacaoEEventos(client)
        await Methods.startCallbackTabNews(client)
    
    @classmethod
    async def startCallbackRedBlueTeams(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["RED_BLUE_MESSAGE"]))
        view = discord.ui.View.from_message(message)
        view.timeout = None
        
        for child in view.children:
            Methods.selectRedBlueTeam = child
            child.callback = Methods.callbackChildRedBlueTeam
        
        await message.edit(view=view)
    
    @classmethod
    async def startCallbackTabNews(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["TABNEWS_MESSAGE"]))
        view = discord.ui.View.from_message(message)
        view.timeout = None
        
        for child in view.children:
            print(child)
            if str(child.label).lower() == "sim":
                child.callback = Methods.simCallbackTabNews
            elif str(child.label).lower() == "não":
                child.callback = Methods.naoCallbackTabNews
        
        await message.edit(view=view)
    
    @classmethod
    async def startCallbackSistemaOperacional(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["SISTEMA_OPERACIONAL_MESSAGE"]))
        
        view = discord.ui.View.from_message(message)
        view.timeout = None
        for child in view.children:
            Methods.selectSistemaOperacional = child
            child.callback = Methods.callbackChildSistemaOperacional
        
        await message.edit(view=view)
    
    @classmethod
    async def callbackChildRedBlueTeam(cls, interaction: discord.Interaction):
        sistemList = ["red team", "blue team", "purple team"]
        choosed = None
        
        option = cls.selectRedBlueTeam.values[0]
        print(option)
        if option == "Red Team":
            choosed = "red team"
            await cls().workingForFunctions(interaction, "Red Team")
        elif option == "Blue Team":
            choosed = "blue team"
            await cls().workingForFunctions(interaction, "Blue Team")
        elif option == "Purple Team":
            choosed = "purple team"
            await cls().workingForFunctions(interaction, "Purple Team")
        
        print("Cargo adicionado")
        for sistem in sistemList:
            guild = interaction.client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
            if sistem != choosed:
                role = guild.get_role(Methods.cargos[sistem])
                await interaction.user.remove_roles(role)
    
    @classmethod
    async def callbackChildSistemaOperacional(cls, interaction: discord.Interaction):
        sistemList = ["windows", "mac", "linux"]
        choosed = None
        
        option = cls.selectSistemaOperacional.values[0]
        print(option)
        if option == "Team Windows":
            choosed = "windows"
            await cls().workingForFunctions(interaction, "Windows")
        elif option == "Team Mac":
            choosed = "mac"
            await cls().workingForFunctions(interaction, "Mac")
        elif option == "Team Linux":
            choosed = "linux"
            await cls().workingForFunctions(interaction, "Linux")
        
        print("Cargo adicionado")
        for sistem in sistemList:
            guild = interaction.client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
            print(f"Sistem: {sistem}, Choosed: {choosed}")
            if sistem != choosed:
                role = guild.get_role(Methods.cargos[sistem])
                await interaction.user.remove_roles(role)

    @classmethod
    async def startCallbackNotificacaoEEventos(cls, client, bot=None):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["NOTIFICACAO_E_EVENTOS_MESSAGE"]))
        view = discord.ui.View.from_message(message)
        view.timeout = None
        
        for child in view.children:
            if str(child.label).lower() == "sim":
                child.callback = Methods.simNotificacaoEEventos
            elif str(child.label).lower() == "não":
                child.callback = Methods.naoNotificacaoEEventos
        
        await message.edit(view=view)    
    
    @classmethod
    async def startCallbackCargosLinguagens(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["LINGUAGENS_MESSAGE"]))
        
        view = discord.ui.View.from_message(message)
        view.timeout = None

        for child in view.children:
            if str(child.label).lower() == "python":
                child.callback = Methods.python
                l = "python"
            elif str(child.label).lower() == "javascript":
                child.callback = Methods.javascript
                l = "javascript"
            elif str(child.label).lower() == "react native":
                child.callback = Methods.reactnative
                l = "react"
            elif str(child.label).lower() == "php":
                child.callback = Methods.php
                l = "php"
            elif str(child.label).lower() == "c#":
                child.callback = Methods.csharp
                l = "c#"
            elif str(child.label).lower() == "c++":
                child.callback = Methods.cplus
                l = "c++"
            elif str(child.label).lower() == "sql":
                child.callback = Methods.sql
                l = "SQL"
            elif str(child.label).lower() == "java":
                child.callback = Methods.java
                l = "java"
            elif str(child.label).lower() == "html e css":
                child.callback = Methods.html_e_css
                l = "frontend"
            elif str(child.label).lower() == "rust":
                child.callback = Methods.rust
                l = "rust"
                
        m = l
        if l == "java" or l == "c#" or l == "c++" or l == "SQL":
            m = "outras"
        c = client.get_channel(int(os.environ[f"{m.upper()}_CHANNEL"]))
    
        await message.edit(view=view)
    
    @classmethod
    async def startCallbackProcuraEmprego(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["BUSCANDO_EMPREGO_MESSAGE"]))
        view = discord.ui.View.from_message(message)
        view.timeout = None
        
        for child in view.children:
            if str(child.label).lower() == "sim":
                child.callback = Methods.simCallbackProcuraEmprego
            elif str(child.label).lower() == "não":
                child.callback = Methods.naoCallbackProcuraEmprego
        
        await message.edit(view=view)
    
    @classmethod
    async def starCallbackIdeiaProjeto(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["PROJETOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["IDEIA_PROJETO_MESSAGE"]))
        view = discord.ui.View.from_message(message)
        view.timeout = None
        
        if view.children[0]:
            view.children[0].callback = Methods.callbackIdeiaProjetos
            
        await message.edit(view=view)

    
    @classmethod
    async def startCallbackContratante(cls, client):
        guild = client.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        message = await channel.fetch_message(int(os.environ["BUSCANDO_PROFISSIONAIS_MESSAGE"]))
        
        view = discord.ui.View.from_message(message)
        view.timeout = None
        
        for child in view.children:
            if str(child.label).lower() == "sim":
                child.callback = Methods.simCallbackContratante
            elif str(child.label).lower() == "não":
                child.callback = Methods.naoCallbackContratante
        
        await message.edit(view=view)
        
    @classmethod
    async def simCallbackContratante(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Contratante")
    
    @classmethod
    async def naoCallbackContratante(cls, interaction: discord.Interaction):
        role = interaction.guild.get_role(Methods.cargos["contratante"])
        for cargo in interaction.user.roles:
            if cargo.id == role.id:
                return await cls().workingForFunctions(interaction, "Contratante")
        
        return await interaction.response.send_message("Sem cargo para retirar", ephemeral=True)
    
    @classmethod
    async def simCallbackTabNews(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Tab news")
    
    @classmethod
    async def naoCallbackTabNews(cls, interaction: discord.Interaction):
        role = interaction.guild.get_role(Methods.cargos["tab news"])
        for cargo in interaction.user.roles:
            if cargo.id == role.id:
                return await cls().workingForFunctions(interaction, "Tab news")
        
        return await interaction.response.send_message("Sem cargo para retirar", ephemeral=True)
    
    @classmethod
    async def simCallbackProcuraEmprego(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Busco emprego")
    
    @classmethod
    async def simNotificacaoEEventos(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Notificacao e Eventos")
        
    @classmethod
    async def naoNotificacaoEEventos(cls, interaction: discord.Interaction):
        role = interaction.guild.get_role(Methods.cargos["notificacao e eventos"])
        for cargo in interaction.user.roles:
            if cargo.id == role.id:
                return await cls().workingForFunctions(interaction, "Notificacao e eventos")
        
        return await interaction.response.send_message("Sem cargo para retirar", ephemeral=True)
    
    @classmethod
    async def naoCallbackProcuraEmprego(cls, interaction: discord.Interaction):
        role = interaction.guild.get_role(Methods.cargos["busco emprego"])
        for cargo in interaction.user.roles:
            if cargo.id == role.id:
                return await cls().workingForFunctions(interaction, "Busco emprego")
        
        return await interaction.response.send_message("Sem cargo para retirar", ephemeral=True)
    
    @classmethod
    async def callbackIdeiaProjetos(cls, interaction: discord.Interaction):
        respostas_cargo = interaction.client.get_channel(int(os.environ["RESPOSTAS_CARGO_CHANNEL"]))
        await interaction.response.send_message("Vou avisar o ADM, já ele entra em contato!", ephemeral=True)
        await respostas_cargo.send(f"{interaction.user.mention} disse que teve uma ideia de projeto, fala com ele!")
    
    @classmethod
    async def callbackFreelanceMessage(cls, interaction: discord.Interaction):
        await interaction.response.send_message("Processando...", ephemeral=True)
        respostas_cargo = interaction.client.get_channel(int(os.environ["RESPOSTAS_CARGO_CHANNEL"]))
        comoGanharPontos = interaction.guild.get_channel(int(os.environ["COMO_GANHAR_PONTOS_CHANNEL"]))
        pontos = int(await Methods.connector.getPontos(interaction.user.id))
        member = interaction.guild.get_member(int(interaction.user.id))
        freelance_channel = interaction.guild.get_channel(int(os.environ["FREELANCE_CHANNEL"]))
        if pontos < 800:
            await interaction.user.send(f"Desculpe, mas são necessários 🪙 800 bucks para participar da equipe de freelance. Por enquanto você está com 🪙 {pontos} bucks")
            await interaction.user.send(f"Para ganhar mais bucks, dê uma olhada no chat de {comoGanharPontos.mention}.")
            await interaction.user.send("A outra má notícia é que o grupo de freelance está parado. Normalmente ele acontecia no proprio discord. Mas o ADM está fazendo um sistema bolado no codecompany.org")
        else:
            await interaction.user.send("Você tem os 🪙 800 bucks necessários, mas infelizmente o grupo de freelance está parado 😥")
            await interaction.user.send("Mas calma... ele ta parado porque o ADM ta fazendo um sistema brabo para freelance no codecompany.org!")
        await interaction.user.send("A previsão é que volte no começo de 2023, mas não temos certeza ainda. Qualquer mudança será anunciada na Code Company, então não se preocupe!")
        await respostas_cargo.send(f"FREELANCE: {interaction.user.mention} Queria participar mas estamos parados 😥")
    
    @classmethod
    async def windows(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Windows")
    
    @classmethod
    async def linux(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "linux")
        
    @classmethod
    async def mac(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "mac")
    
    @classmethod
    async def python(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Python")
    
    @classmethod
    async def html_e_css(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "HTML e CSS")
    
    @classmethod
    async def rust(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Rust")
    
    @classmethod
    async def javascript(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Javascript")
    
    @classmethod
    async def php(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "PHP")
        
    @classmethod
    async def reactnative(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "React native")
    
    @classmethod
    async def frontend(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Frontend")
    
    @classmethod
    async def csharp(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "C#")
    
    @classmethod
    async def frontend(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "HTML e CSS")
    
    @classmethod
    async def cplus(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "C++")
    
    @classmethod
    async def java(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "Java")
    
    @classmethod
    async def sql(cls, interaction: discord.Interaction):
        await cls().workingForFunctions(interaction, "SQL")
        