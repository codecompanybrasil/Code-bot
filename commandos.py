import discord
import os
import asyncio
import typing
from dotenv import load_dotenv
from discord.ext import commands as c
import requests
from bs4 import BeautifulSoup
from conn_db import Connection
from utils import Utils

class Auxiliar:
    def __init__(self, bot=None):
        self. connector = Connection()
        self.bot = bot
    
    async def isAdmin(self, interaction: discord.Interaction, notReturn=False):
        idUser = int(interaction.user.id)
        await self.connector.connect()
        self.connector.cursor.execute(f"SELECT * FROM admin WHERE id = {idUser};")
        data = self.connector.cursor.fetchone()
        if not notReturn and not data:
            return await interaction.followup.send(f"{interaction.user.mention} não tem permissões administradoras para esse comando")
        
        if data:
            return True
        return False
    
    async def isAdminWithMessage(self, message: discord.Message, notReturn=False):
        idUser = int(message.author.id)
        await self.connector.connect()
        self.connector.cursor.execute(f"SELECT * FROM admin WHERE id = {idUser};")
        data = self.connector.cursor.fetchone()
        if not notReturn and not data:
            return await message.channel.send(f"{message.author.mention} não tem permissões administradoras para esse comando")
        
        if data:
            return True
        return False

    async def isLiderDeProjeto(self, idUser):
        await self.connector.connect()
        self.connector.cursor.execute(f"SELECT isLiderDeProjeto FROM membros WHERE idUser = {idUser};")
        data = self.connector.cursor.fetchone()
        if list(data)[0]:
            return True
        return False

    async def testingIntParam(self, interaction:discord.Interaction, param, tipo=int):
        try:
            param = tipo(param)
        except:
            await interaction.followup.send("Parametros incorretos. Leia a descrição dos parametros e tente novamente!", ephemeral=True)
            return False
        else:
            return True

class TabReader:
    def __init__(self, profile: str="codecompanybrasil", bot: c.Bot=None, link=None):
        load_dotenv()
        self.profile = f"https://www.tabnews.com.br/{profile}"
        self.bot = bot
        self.req = requests.get(self.profile)
        self.soup = BeautifulSoup(self.req.text, 'html.parser')
        if link:
            self.last = link
        else:
            self.last = self.lastPost()
    
    def lastPost(self):
        elements = []
        for element in self.soup.find_all("article"):
            if element.find("a", {"class": "Link-sc-hrxz1n-0 bPBLTS"}):
                elements.append(element.find("a"))
        
        return f"https://www.tabnews.com.br{elements[0]['href']}"

    async def sendPost(self):
        guild = self.bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        channel = guild.get_channel(int(os.environ["TABNEWS_CHANNEL"]))
        role = guild.get_role(int(os.environ["TABNEWS_ROLE"]))
        m = await channel.send(f"{role.mention}\n{self.last}")
        await m.publish()


load_dotenv()
bot = c.Bot(command_prefix=".", intents=discord.Intents.all())
auxiliar = Auxiliar()
connector = Connection()
utils = Utils(pessoa=bot)
globals = {}
guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))

@bot.tree.command(name="ping", description="Para saber se o bot ta on")
async def func(interaction: discord.Interaction):
    await interaction.response.send_message("Pong", ephemeral=True)

@bot.tree.command(name="help", description="Mostra os comandos do bot!")
async def func(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    embed = discord.Embed(
        title="Meus comandos são esses:",
        description="Olha só como sou simples de usar :)",
        color = discord.Color.dark_orange(),
    )

    embed.add_field(name="/help", value="Abre uma tabela de ajuda.", inline=False)
    embed.add_field(name="/ranking", value="Mostra o ranking de níveis para subir", inline=False)
    #embed.add_field(name="/github", value="Mosta o GitHub do projeto (Envie no canal próprio do projeto)", inline=False)
    embed.add_field(name="/server info", value="Mostra informações sobre o servidor", inline=False)
    embed.add_field(name="/profile", value="Mostra suas informações", inline=False)
    embed.add_field(name="/profile <ID do usuario>", value="Mostra informações do perfil", inline=False)
    #embed.add_field(name="/palavra", value="Gera uma palavra aleatoria.", inline=False)
    #embed.add_field(name="/new project <> <>", value="cria um projeto novo", inline=False)
    embed.add_field(name="/ping", value="Diz se o bot está vivo", inline=False)
    embed.add_field(name="/admin self", value="Você tem permissões sobre mim? descubra.", inline=False)
    if await auxiliar.isAdmin(interaction) == True:
        embed.add_field(name='/share <ID do cargo> "<Mensagem>"  //ADM', value="Manda mensagem para todos do cargo", inline=False)
        embed.add_field(name="/bucks add <Bucks> <ID do usuario>  //ADM", value="Adiciona bucks ao usuario", inline=False)
        embed.add_field(name="/event start <ID do canal do evento> //ADM", value="Inicie um evento", inline=False)
        embed.add_field(name="/event status //ADM", value="Dados do evento", inline=False)
        embed.add_field(name="/event finish <ID do canal do evento> //ADM", value="Encerre o evento", inline=False)
        embed.add_field(name="/move <ID call> <ID para onde mexer> //ADM", value="Mova as pessoas de chamadas", inline=False)
        embed.add_field(name="/clean <ID do canal>   //ADM", value="Apaga todas as mensagens do canal", inline=False)
        embed.add_field(name="/freelance add  <ID do usuario>  //ADM", value="Abre uma tabela de ajuda.", inline=False)
        embed.add_field(name="/freelance remove <ID do usuario>  //ADM", value="Abre uma tabela de ajuda.", inline=False)
        embed.add_field(name="/freelance message <ID da mensagem>  //ADM", value="Envia um embed de job da área de freelance para o chat privado do ADM", inline=False)
        embed.add_field(name="/freelance message <ID da mensagem> <ID do canal> //ADM", value="Envia um embed de job da área de freelance para alguem", inline=False)
        #embed.add_field(name="/freelance send <LINK DO FREELANCE.COM>  //ADM", value="Envia um job para o canal jobs de freelance", inline=False)
        #embed.add_field(name="/freelance send --list ['<LINK1>', '<LINK2>']  //ADM", value="Envia uma lista de links para o canal com quantos links forem colocados", inline=False)
        embed.add_field(name="/freelance job (ID do trabalho)  //ADM", value="Adiciona um job oficial a lista de jobs do freelance", inline=False)
        embed.add_field(name="/addLiderProjeto <ID do usuario>   (Enviar no canal do projeto)   //ADM", value="Seta ele como lider de projeto", inline=False)
        embed.add_field(name="/addMensagemProjeto <ID da mensagem>   (Enviar no canal do projeto)   //ADM", value="Adiciona a mensagem para os interessados reagirem", inline=False)
        embed.add_field(name="/admin add (ID do usuario)  //ADM", value="Da permissões administradoras ao usuario", inline=False)
        embed.add_field(name="/admin remove (ID do usuario)  //ADM", value="Tira permissões administradoras do usuario", inline=False)
        #embed.add_field(name="/ban (ID do usuario) (Motivo) //ADM", value="Bane o usuario e posta seu motivo no canal", inline=False)   
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name="ranking", description="Mostra o ranking de níveis da comunidade")
async def func(interaction: discord.Interaction):
    await interaction.response.defer()
    pontos = await connector.getPontos(interaction.user.id)
    await utils.checkingRanking(pontos, interaction.user.id)

    r = await connector.getRanking(interaction.user.id)
    r = await utils.formatingRankingName(str(r), tipo="letter")
    embed = discord.Embed(
        title="Ranking",
        description=f"Você está em: {r}",
        color=discord.Color.gold()
    )
    embed.add_field(name="Iniciante", value="a partir de 🪙 0 bucks")
    embed.add_field(name="Gafanhoto", value="a partir de 🪙 150 bucks")
    embed.add_field(name="Junior", value="a partir de 🪙 300 bucks")
    embed.add_field(name="Pleno", value="a partir de 🪙 500 bucks")
    embed.add_field(name="Webmaster", value="a partir de 🪙 700 bucks")
    embed.add_field(name="Senior", value="a partir de 🪙 1000 bucks")

    await interaction.followup.send(embed=embed)

@bot.hybrid_group(name="server")
async def server(ctx):
    pass

@server.command(name="info", description="Mostra informações sobre o servidor")
async def func(ctx: c.Command):
    await ctx.defer(ephemeral=True)
    embed = discord.Embed(
        title="Code Company",
        description="Alguns dados e informações sobre a Code Company",
        color=discord.Color.dark_blue()
    )
    embed.add_field(name="Nome do Servidor", value=ctx.guild.name)
    embed.add_field(name="Criado em", value=str(ctx.guild.created_at).split(" ")[0])
    embed.add_field(name="Quantidade de membros", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="Dono do server", value=f"{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}")
    embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/111263313?v=4")
    await ctx.send(embed=embed, ephemeral=True)

@bot.tree.command(name="profile", description="Mostra informações sobre o servidor")
@discord.app_commands.describe(id="ID de um usuario. (Sem esse parametro ele pega o seu ID)batata")
async def profile(interaction: discord.Interaction, id: str = ""):
    #pesquisar sobre esse int do typing Optional
    await interaction.response.defer(ephemeral=True)
    if id:
        if not await auxiliar.testingIntParam(interaction, id):
            return False
        authorId = int(id)
    else:
        authorId = interaction.user.id
    print(authorId)

    perfil = await connector.getProfile(authorId)
    if perfil:
        try:
            avatar_url = bot.get_user(authorId).avatar.url
        except:
            avatar_url = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"
        r = await connector.getRanking(authorId)
        r = await utils.formatingRankingName(r, tipo="letter")
        member = interaction.guild.get_member(authorId)
        embed = discord.Embed(
            title=f"Profile {perfil[2]}#{perfil[3]}",
            color=discord.Color.dark_blue()
        )
        embed.add_field(name="Nome", value=f"{perfil[2]}#{perfil[3]}", inline=False)
        #embed.add_field(name="Bucks", value=f"🪙 {perfil[1]} bucks", inline=False)
        # embed.add_field(name="Ranking", value=f"🏅 {r}", inline=False)
        embed.add_field(name="ID", value=perfil[0], inline=False)
        embed.add_field(name="Membro desde", value=str(member.joined_at).split(" ")[0], inline=False)
        embed.set_thumbnail(url=avatar_url)
        await interaction.followup.send(member.mention, embed=embed)
    else:
        await interaction.followup.send("Desculpa, mas não estou encontrando seu perfil, tente novamente mais tarde")

# @bot.tree.command(name="admin", description="Você é um ADM? O comando responde")
# async def admin(interaction: discord.Interaction):
#     if await auxiliar.isAdmin(interaction, notReturn=True):
#         await interaction.followup.send(f"{interaction.user.name} tem permissões administradoras. :)", ephemeral=True)
#     else:
#         await interaction.followup.send(f"{interaction.user.name} não é um admin. :(", ephemeral=True)

@bot.hybrid_group(name="admin", description="Você é um ADM? O comando responde", fallback="self")
async def admin(ctx: c.Context):
    await ctx.defer(ephemeral=True)
    if await auxiliar.isAdmin(ctx.interaction, notReturn=True):
        await ctx.send(f"{ctx.author.name} tem permissões administradoras. :)", ephemeral=True)
    else:
        await ctx.send(f"{ctx.author.name} não é um admin. :(", ephemeral=True)

@admin.command(name="add", description="Adiciona um ADM  //ADM")
@discord.app_commands.describe(id="ID do usuario")
async def add(ctx: c.Context, id: str):
    #adicionar de verdade ksksk
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        usuario = bot.get_user(int(id))
        if str(usuario) == "None":
            await ctx.send("ID invalido")
            return False
        user_name = f"{usuario.name}#{usuario.discriminator}"
        await connector.connect()
        connector.cursor.execute(f"SELECT * FROM admin WHERE id = {id}")
        if connector.cursor.fetchone():
            await ctx.send(f"{usuario.name} já é um admin", ephemeral=True)
        else:
            await connector.connect()
            connector.cursor.execute(f"INSERT INTO admin (id, nome) VALUES ({id}, '{user_name}');")
            connector.con.commit()
            await ctx.send(f"{usuario.name} é um admin agora.")

@admin.command(name="remove", description="Remove um ADM  //ADM")
@discord.app_commands.describe(id="ID do usuario")
async def remove(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        if id == int(os.environ["ADM_ID"]):
            await ctx.send(f"Impossível tirar o CEO")
        else:
            usuario = bot.get_user(int(id))
            await connector.connect()
            connector.cursor.execute(f"SELECT * FROM admin WHERE id = {id}")
            if connector.cursor.fetchone():
                connector.cursor.execute(f"DELETE FROM admin WHERE id = {id};")
                connector.con.commit()
                await ctx.send(f"{usuario.name} foi removido da administração", ephemeral=True)
            else:
                await ctx.send(f"{usuario.name} não é um ADM ksks", ephemeral=True)
        


@bot.tree.command(name="share", description="Manda uma mensagem para todos do cargo  //ADM")
@discord.app_commands.describe(role="ID do cargo", mensagem="A mensagem que quer enviar")
async def share(interaction: discord.Interaction, role: str, mensagem: str):
    await interaction.response.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(interaction, role):
        return False
    
    if await auxiliar.isAdmin(interaction):
        guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        for member in guild.get_role(int(role)).members:
            try:
                await member.send(mensagem)
            except:
                pass

@bot.hybrid_group(name="bucks")
async def bucks(ctx):
    pass

@bucks.command(name="add", description="Adiciona bucks a um membro  //ADM")
@discord.app_commands.describe(id="ID do usuario", bucks="Os bucks que serão adicionados", motivo="Mensagem exibida ao dar os bucks")
async def add(ctx: c.Context, id: str, bucks: int, motivo: str = ""):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        atualPontos = await connector.getPoint(int(id))
        mandante = bot.get_user(ctx.author.id)
        membro = bot.get_user(int(id))
        await utils.setPoint(int(atualPontos) + bucks, int(id))
        if motivo:
            await utils.pointMessage(int(id), bucks, f"{mandante.mention} te deu 🪙 {bucks} bucks!\n{motivo}")
        else:
            await utils.pointMessage(int(id), bucks, f"{mandante.mention} te deu 🪙 {bucks} bucks!")

@bot.hybrid_group(name="event")
async def event(ctx):
    pass
        

@event.command(name="start", description="Inicia um evento  //ADM")
@discord.app_commands.describe(id="ID do canal do evento")
async def start(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        if await connector.isEvent():
            await ctx.send("Já tem um evento acontencendo", ephemeral=True)
        else:
            await connector.connect()
            connector.cursor.execute(f"INSERT INTO eventos (idChannel) VALUES ({id});")
            connector.con.commit()
            await ctx.send("Evento iniciado!", ephemeral=True)

@event.command(name="status", description="Dados do evento  //ADM")
async def status(ctx: c.Context):
    await ctx.defer(ephemeral=True)
    if await auxiliar.isAdmin(ctx.interaction):
        data = await connector.isEvent()
        if data:
            canal = bot.get_channel(int(data[0]))
            await ctx.send(f"Tem evento acontecendo no canal {canal.mention}; ID: {canal.id}", ephemeral=True)
        else:
            await ctx.send("Sem evento acontecendo no momento", ephemeral=True)

@event.command(name="finish", description="Encerra o evento  //ADM")
@discord.app_commands.describe(id="ID do canal do evento")
async def finish(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        await connector.connect()
        connector.cursor.execute(f"DELETE FROM eventos WHERE idChannel = {id};")
        connector.con.commit()
        participantes = await connector.getParticipantesEvent(int(id))
        channel = bot.get_channel(int(id))
        await ctx.send("Evento encerrado!", ephemeral=True)
        embed = discord.Embed(
            title="Participantes do Evento em:",
            description=f"{channel.mention}",
            color=discord.Color.brand_green()
        )
        if participantes:
            for participante in participantes:
                idParticipante = list(participante)[0]
                user = bot.get_user(int(idParticipante))
                await utils.setPoint(50, int(idParticipante))
                await utils.pointMessage(int(idParticipante), 50, "Participou de um evento da Code Company! Obrigado pela presença, toma ai 🪙 50 bucks!")
                embed.add_field(name=f"{user.name}#{user.discriminator}", value=str(idParticipante), inline=False)
        else:
            embed.add_field(name="Nenhum participante", value=":sob:", inline=True)
        adm = bot.get_user(int(os.environ["ADM_ID"]))
        await adm.send(embed=embed)
        await connector.connect()
        connector.cursor.execute("TRUNCATE participantesEvento;")
        connector.con.commit()

@bot.tree.command(name="move", description="Mova todos de um canal para o outro  //ADM")
@discord.app_commands.describe(call="ID do canal", destino="ID do canal de destino")
async def move(interaction: discord.Interaction, call: str, destino: str):
    await interaction.response.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(interaction, call) or not await auxiliar.testingIntParam(interaction, call):
        return False
    
    if await auxiliar.isAdmin(interaction):
        guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        c1 = guild.get_channel(int(call))
        c2 = guild.get_channel(int(destino))
        for member in c1.members:
            await member.move_to(c2)
        await interaction.followup.send("Membros movidos", ephemeral=True)

@bot.tree.command(name="clean", description="Discord não apaga sapora")
async def clean(interaction: discord.Interaction):
    print("\n\nComando Clean\n\n")
    channel = bot.get_channel(int(interaction.channel.id))
    await channel.send("DISCORD TA UM CU HOJE")

@bot.tree.command(name="doclean", description="Apaga mensagens no canal  //ADM")
@discord.app_commands.describe(id="ID do canal", limit="Limite para apagar mensagens", msgInicio="ID da primeira mensagem", msgFinal="ID da ultima mensagem")
async def doclean(interaction: discord.Interaction, id: str="", limit: int=0, msgInicio: str="0", msgFinal: str="0"):
    #Seta o starter do inicio
    if msgInicio:
        starter = False
    else:
        starter = True
    
    
    await interaction.response.defer(ephemeral=True)
    
    if await auxiliar.isAdmin(interaction):
        #Pega o canal
        if id:
            if not await auxiliar.testingIntParam(interaction, id):
                return False
            channel = bot.get_channel(int(id))
        else:
            channel = bot.get_channel(int(interaction.channel.id))
        
        
        try:
            async for message in channel.history():
                if starter:
                    if int(msgFinal) == message.id:
                        break
                    
                    if limit > 0:
                        await message.delete()
                        limit -= 1
                    else:
                        break
                else:
                    if int(msgInicio) == message.id:
                        starter = True
        except Exception as erro:
            raise erro
        await interaction.followup.send("Canal limpo!", ephemeral=True)

@bot.hybrid_group(name="freelance")
async def freelance(ctx):
    pass

@freelance.command(name="add", description="Adiciona um membro à equipe de freelance  //ADM")
async def add(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        bemVindo = bot.get_channel(int(os.environ["BEM_VINDO_FREELANCE_CHANNEL"]))
        usuario = bot.get_user(int(id))
        membro = guild.get_member(usuario.id)
        freelancer = guild.get_role(1007666930649407569)
        
        await connector.connect()
        con = await connector.con
        cursor = await connector.cursor
        nome_completo = f"{membro.name}#{membro.discriminator}"
        cursor.execute(f"INSERT INTO freelancers (idUser, nome) VALUES ({id}, '{nome_completo}');")
        con.commit()
        con.close()

        embed = discord.Embed(
            title=f"😎 Sejá bem vindo a equipe de Freelance da {guild.name} {nome_completo}! 😎",
            description="Espero que se divirta",
            color = discord.Color.green()
        )
        embed.set_footer(text="Comprimentos do ADM")
        try:
            avatar = membro.avatar.url
        except:
            avatar = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"
        embed.set_author(name=f"{membro.name}", icon_url=avatar)
        embed.set_image(url=avatar)
        await bemVindo.send(embed=embed)
        
        await membro.add_roles(freelancer)
        await ctx.send("Membro adicionado", ephemeral=True)

@freelance.command(name="remove", description="Remove o usuario da equipe de freelance  //ADM")
async def remove(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        tchau = bot.get_channel(int(os.environ["TCHAU_FREELANCE_CHANNEL"]))
        membro = guild.get_member(int(id))
        freelancer = guild.get_role(1007666930649407569) 
        nome_completo = f"{membro.name}#{membro.discriminator}"

        await connector.connect()
        connector.cursor.execute(f"DELETE FROM freelancers WHERE idUser = {id};")
        connector.con.commit()
        connector.con.close()

        try:
            avatar = membro.avatar.url
        except:
            avatar = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"

        embed = discord.Embed(
        title=f"{nome_completo} saiu do equipe ",
        description="É uma pena, espero que volte um dia.",
        color = discord.Color.red()
        )
        embed.set_footer(text="Comprimentos do ADM")
        embed.set_author(name=f"{membro.name}", icon_url=avatar)
        embed.set_image(url=avatar)
        await tchau.send(embed=embed)
        
        await membro.remove_roles(freelancer)
        await ctx.send("Membro removido", ephemeral=True)

@freelance.command(name="message", description="Envia um embed de um canal para o outro  //ADM")
@discord.app_commands.describe(id="ID da mensagem", canal="ID do canal")
async def message(ctx: c.Context, id: str, canal: str = ""):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        if canal:
            if not await auxiliar.testingIntParam(ctx.interaction, canal):
                return False
            channel = bot.get_channel(int(canal))
        else: 
            channel = bot.get_channel(int(os.environ["MESSAGE_FREELANCE_CHANNEL"]))
        canal_jobs = bot.get_channel(int(os.environ["FREELANCER_CHANNEL"]))
        message = await canal_jobs.fetch_message(int(id))
        embedList = []
        for embed in message.embeds:
            embedList.append(embed)
        await channel.send(embeds=embedList)
        await ctx.send("Mensagem enviada", ephemeral=True)

@freelance.command(name="job", description="Adiciona um job oficial a lista de jobs do freelance  //ADM")
@discord.app_commands.describe(id="ID da mensagem do job")
async def job(ctx: c.Context, id:str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        notifyJob = await connector.getNotifyJobs(id)
        if not notifyJob:
            return await ctx.send("O trabalho não existe, tente de novo com um ID valido")
        await connector.insertJob(notifyJob, ctx.channel.id, bot)
        await ctx.send("Job inserido", ephemeral=True)

@bot.hybrid_group("add")
async def add(ctx):
    pass

@bot.tree.command(name="tabnews", description="Atualiza o chat Tab News")
@discord.app_commands.describe(link="Especifica o link do post")
async def tabnews(interaction: discord.Interaction, link: str=""):
    await interaction.response.defer(ephemeral=True)
    if await auxiliar.isAdmin(interaction):
        tab = TabReader(bot=bot, link=link)
        await tab.sendPost()
        await interaction.followup.send("Post feito", ephemeral=True)
    

@add.command(name="mensagemprojeto", description="Adiciona a mensagem para os interessados reagirem  //ADM")
@discord.app_commands.describe(id="ID da mensagem")
async def mensagemprojeto(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        await connector.connect()
        connector.cursor.execute(f"UPDATE projetos SET idMensagemProjeto = {id} WHERE idChannel = {int(message.channel.id)};")
        connector.con.commit()
        await ctx.send(f"Mensagem adicionada ao projeto!")

@add.command(name="liderprojeto", description="Seta ele como lider de projeto  //ADM")
@discord.app_commands.describe(id="ID do usuario")
async def liderprojeto(ctx: c.Context, id: str):
    await ctx.defer(ephemeral=True)
    if not await auxiliar.testingIntParam(ctx.interaction, id):
        return False
    
    if await auxiliar.isAdmin(ctx.interaction):
        guild = bot.get_guild(int(os.environ["CODE_COMPANY__ID"]))
        role = guild.get_role(int(os.environ["LIDER_DE_PROJETO_ROLE"]))
        member = guild.get_member(int(id))
        await member.add_roles(role)
        await connector.setLiderDeProjeto(int(id))
        await ctx.send("Lider de projeto escolhido!")

    