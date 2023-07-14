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
import argparse
import shlex
from utils import Utils
from verifications import Verifications
from commandos import bot
from commandos import auxiliar
from methods import Methods

load_dotenv()
#starter = Scrapper(bot)
connector = Connection()
#comandos = Comandos(bot=bot)
utils = Utils(pessoa=bot)
verification = Verifications(pessoa=bot)

#executor = Executor(bot=bot)

@bot.event
async def on_ready():
    print(f"Entrei no servidor como {bot.user}.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("/help"))
    guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
    adm = guild.get_member(int(os.environ["ADM_ID"]))
    await Methods.init(bot)
    #await executor.run()
    
    
@bot.event
async def on_member_join(member):
    avatar_url = ""
    try:
        avatar_url = member.avatar.url
    except:
        avatar_url = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"
    
    guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))  
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

@bot.event
async def on_member_remove(member):
    avatar_url = ""
    try:
        avatar_url = member.avatar.url
    except:
        avatar_url = "https://www.ibimirim.pe.leg.br/imagens/semimagemavatar.png"
    tchau = bot.get_channel(1007645159938326548)
    servidor = bot.get_guild(1007633662847762503)
    embed = discord.Embed(
        title=f"{member} saiu do servidor",
        color = discord.Color.red()
    )
    embed.set_author(name=f"{member.name}", icon_url=avatar_url)
    embed.set_image(url=avatar_url)
    await tchau.send(embed=embed)
    await utils.desabilitingMember(member.id)

@bot.event
async def on_member_update(before, after):
    if before.name != after.name or before.discriminator != after.discriminator:
        await connector.refreshProfile(after.id, after.name, after.discriminator)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        idChannel = after.channel.id
        if await connector.existEvent(idChannel):
            await connector.addParticipanteEvent(member.id, idChannel)
    
@bot.event
async def on_raw_reaction_add(payload):
    for idMensagemProjeto in await connector.getIdMensagensProjetos():
        if idMensagemProjeto[0] == payload.message_id:
            idChannel = await connector.getIdChannelByIdMensagemProjetos(idMensagemProjeto[0])
            guild = bot.get_guild(int(os.environ["CODE_COMPANY_ID"]))
            user = guild.get_member(int(payload.user_id))
            content = utils.mensagensInteressadoProjeto[randint(0, len(utils.mensagensInteressadoProjeto)-1)].replace("@$bot", str(user.mention))
            channel = guild.get_channel(int(idChannel))
            projetos_channel = guild.get_channel(int(os.environ["PROJETOS_CHANNEL"]))
            mensagem = await projetos_channel.fetch_message(int(payload.message_id))
            await mensagem.remove_reaction(payload.emoji, user)#emoji, member
            await channel.send(content)


@bot.event
async def on_message(message):
    
    if "!clean" in message.content[0:6]:
        parser = argparse.ArgumentParser()

        parser.add_argument('-mI', type=int, help='Mensagem inicial')
        parser.add_argument('-mF', type=int, help='Mensagem final')
        parser.add_argument('-id', type=int, help='ID do canal')
        parser.add_argument('-l', type=int, help='Contagem de mensagens')

        command_split = shlex.split(message.content)

        # Analise a lista de palavras
        args = parser.parse_args(command_split[1:])

        id = args.id
        msgInicio = args.mI if args.mI != None else 0
        msgFinal = args.mF if args.mF != None else 0
        limit = args.l if args.l != None else 99
        
        #Pega o canal
        if id:
            channel = bot.get_channel(int(id))
        else:
            channel = bot.get_channel(int(message.channel.id))
        
        #Seta o starter do inicio
        if msgInicio:
            starter = False
        else:
            starter = True
        
        
        if await auxiliar.isAdminWithMessage(message=message):  
            
            try:
                async for msg in channel.history(limit=None):
                    if starter:
                        if int(msgFinal) == msg.id:
                            break
                        
                        if limit > 0 or limit == 99:
                            await msg.delete()
                            limit = limit - 1 if limit != 99 else limit
                        else:
                            break
                    else:
                        if int(msgInicio) == msg.id:
                            starter = True
            except Exception as erro:
                raise erro
            finally:
                
                try:
                    await message.delete()
                except:
                    pass
                
                canal_limpo = await message.channel.send("Canal limpo!")
                await asyncio.sleep(3)
                await canal_limpo.delete()

bot.run(str(os.environ["TOKEN"]))