import discord
from discord.ext import commands as c
from conn_db import Connection
import os
from dotenv import load_dotenv
import asyncio
#from commandos import Comandos
from random import randint
#from executor import Executor
#from freelancer import Scrapper
from utils import Utils
from verifications import Verifications
from commandos import bot as pessoa
from methods import Methods

load_dotenv()
#starter = Scrapper(pessoa)
connector = Connection()
#comandos = Comandos(pessoa=pessoa)
utils = Utils(pessoa=pessoa)
verification = Verifications(pessoa=pessoa)

#executor = Executor(pessoa=pessoa)

@pessoa.event
async def on_ready():
    print(f"Entrei no servidor como {pessoa.user}.")
    await pessoa.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    guild = pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
    adm = guild.get_member(int(os.environ["ADM_ID"]))
    await Methods.init(pessoa)
    #await executor.run()
    
    
@pessoa.event
async def on_member_join(member):
    avatar_url = ""
    try:
        avatar_url = member.avatar.url
    except:
        avatar_url = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"
    
    guild = pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))  
    boas_vindas = guild.get_channel(1007645035447201923)
    conheca_comunidade = guild.get_channel(int(os.environ["CONHECA_CHANNEL"]))
    geral = guild.get_channel(int(os.environ["GERAL_CHANNEL"]))
    cargos = guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
    embed = discord.Embed(
        title=f"🎆 Sejá bem vindo {member.name}!",
        description="A Code Company agradeçe em ter você como membro. Da uma passada no chat de conheça-a-comunidade! Tem umas coisas interessantes por lá",
        color = discord.Color.green()
    )
    embed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=avatar_url)
    embed.set_image(url=avatar_url)
    embed.add_field(name="Responda as perguntas no chat de cargos!", value=f"Assim poderemos saber mais sobre você!\n{cargos.mention}")
    embed.add_field(name="Conheça a comunidade!", value=f"Da uma passada no chat:\n{conheca_comunidade.mention}\n para saber melhor o que cada canal faz!")
    embed.add_field(name="Os membros estão loucos para te conhecer!", value=f"Se apresenta lá no chat geral, a galera daqui é bacana.\n{geral.mention}")
    await boas_vindas.send(member.mention ,embed=embed)
    #await utils.mensagemIniciacao(member, geral)
    await utils.newMember(member.id, member.name, member.discriminator)

    notificacao = guild.get_role(1063667765099106356)
    await member.add_roles(notificacao)
    
    embed = discord.Embed(
        title=f"Olá, bem vindo à Code Company!",
        description='''
Espero que você goste!

Antes de começar sujiro que responda o chat de cargos dentro da comunidade, para adquirir seus cargos e funções.
''',
        color=discord.Color.blue()
    )
    #embed.add_field(name="Como funciona o sistema de Bucks?", value="", inline=False)
    embed.add_field(name="OBS...", value="caso você saia da comunidade, seus buscks e perfil continuarão salvo em até 7 dias! Se não retornar dentro do prazo, sua conta será perdida.", inline=False)

    await utils.sendMensagemBoasVindasDm(member)

@pessoa.event
async def on_member_remove(member):
    avatar_url = ""
    try:
        avatar_url = member.avatar.url
    except:
        avatar_url = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"
    tchau = pessoa.get_channel(1007645159938326548)
    servidor = pessoa.get_guild(1007633662847762503)
    embed = discord.Embed(
        title=f"{member} saiu do servidor",
        color = discord.Color.red()
    )
    embed.set_author(name=f"{member.name}", icon_url=avatar_url)
    embed.set_image(url=avatar_url)
    await tchau.send(embed=embed)
    await utils.desabilitingMember(member.id)
    #await questionary.startQuestion(member.id, "outFeedback", pessoa=pessoa, channel=member, idUser=member.id) #Só descomentar que incia questionary de feedback

@pessoa.event
async def on_member_update(before, after):
    if before.name != after.name or before.discriminator != after.discriminator:
        await connector.refreshProfile(after.id, after.name, after.discriminator)

@pessoa.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        idChannel = after.channel.id
        if await connector.existEvent(idChannel):
            await connector.addParticipanteEvent(member.id, idChannel)

# @pessoa.event
# async def on_raw_reaction_remove(payload):
#     server = pessoa.get_guild(1007633662847762503)
    
#     cargo = await verification.onEmojiReact(payload.emoji.name, server, utils.cargoList)
#     if payload.message_id == 1011466075143163914: #Mensagem emprego
#         if cargo == True:
#             cargo = server.get_role(1007917610727387176)
            
#     elif payload.message_id == 1011466741454475315: #Mensagem Profissionais
#         if cargo == True:
#             cargo = server.get_role(1011458921120153620)
    
#     if cargo and type(cargo) != bool:
#         membro = server.get_member(payload.user_id)
#         await membro.remove_roles(cargo)
    
@pessoa.event
async def on_raw_reaction_add(payload):
    # for c in await questionary.getChannels():
    #     c = c[0]
    #     member = pessoa.get_user(payload.user_id)
    #     if payload.channel_id == c and not member.bot:
    #         await questionary.recibeResponse(payload, c, pessoa=pessoa, channel=pessoa.get_channel(payload.channel_id))

    # if payload.channel_id == int(os.environ["FREELANCER_CHANNEL"]) and payload.user_id != int(os.environ["FREELANCER_BOT_ID"]) and payload.user_id != 1008576934445322270 and payload.emoji.name == "freelancer_icon":
    #     channel = pessoa.get_channel(payload.channel_id)
    #     guild = pessoa.get_guild(1007633662847762503)
    #     member = guild.get_member(payload.user_id)
    #     dmId = await connector.getDmChannel(payload.user_id)
    #     if not dmId:
    #         overwrite = {
    #             guild.get_member(member.id): discord.PermissionOverwrite(read_messages=True),
    #             guild.default_role: discord.PermissionOverwrite(read_messages=False, view_channel=False)
    #         }
    #         private = await guild.create_text_channel(member.name, position=2, reason="canal pessoal para envio de dados do job", overwrites=overwrite, default_auto_archive_duration=60)
    #         await private.send(f":bell: {member.mention} :bell:")
    #         await private.send("O canal se encerra sozinho em 10 minutos. Responda as perguntas dentro desse tempo!")
    #         await connector.setDmChannel(payload.user_id, private.id, f"{member.name}#{member.discriminator}", await utils.dateAtual())
    #         try:
    #             idNotifyJob = await connector.getIdNotifyJobs(payload.message_id)
    #         except:
    #             await private.send("Desculpe, ocorreu um erro no servidor do discord. Reaga a mensagem de novo!")
    #             await questionary.closeCanal(private.id, pessoa)
    #         freelancer_channel = pessoa.get_channel(int(os.environ["FREELANCER_CHANNEL"]))
    #         message = await freelancer_channel.fetch_message(payload.message_id) #a mesagem específica
    #         notifyJob = await connector.getNotifyJobs(idNotifyJob)
    #         notifyJob = list(notifyJob)
    #         del notifyJob[0]
    #         await connector.updateUserNotifyJob(payload.user_id, notifyJob)
    #         await questionary.startQuestion(private.id, "interessadoJob", idNotifyJob=idNotifyJob, pessoa=pessoa, channel=private, idUser=payload.user_id, message=message)
    #     else:
    #         dm = pessoa.get_channel(dmId)
    #         await dm.send(f":bell: {member.mention} :bell:")
    #         await channel.send(f"{member.name} já tem um canal bacanudo")
        
    #Teste para saber se é uma mensagem do chat de projetos!
    for idMensagemProjeto in await connector.getIdMensagensProjetos():
        if idMensagemProjeto[0] == payload.message_id:
            idChannel = await connector.getIdChannelByIdMensagemProjetos(idMensagemProjeto[0])
            guild = pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
            user = guild.get_member(int(payload.user_id))
            content = utils.mensagensInteressadoProjeto[randint(0, len(utils.mensagensInteressadoProjeto)-1)].replace("@$pessoa", str(user.mention))
            channel = guild.get_channel(int(idChannel))
            projetos_channel = guild.get_channel(int(os.environ["PROJETOS_CHANNEL"]))
            mensagem = await projetos_channel.fetch_message(int(payload.message_id))
            await mensagem.remove_reaction(payload.emoji, user)#emoji, member
            await channel.send(content)

# @pessoa.event
# async def on_message(message):
#     Se for resposta de questionario direciona
#     for c in await questionary.getChannels():
#         c = c[0]
#         if message.channel.id == c and not message.author.bot:
#             await questionary.recibeResponse(message, c, pessoa=pessoa, channel=message.channel)
#         if message.author.id == c:
#             await questionary.recibeResponse(message, c, pessoa=pessoa, channel=message.channel)

#     Se for comandos executa
    
#     for c in list(comandos.commandos.keys()):
#         if str(c) in message.content:
#             try:
#                 await message.delete()
#             except:
#                 pass
#             callback = comandos.commandos[c]["callback"]
#             if comandos.commandos[c]["admin"]:
#                 if await connector.isAdmin(int(message.author.id)):
#                     await callback(message, pessoa)
#                 else:
#                     await message.channel.send("Você não tem permissões administradoras para executar esse comando!")
#             else:
#                 await callback(message, pessoa) 
    
#     Verifications
#     await verification.bumpVerification(message)

pessoa.run(str(os.environ["TOKEN"]))