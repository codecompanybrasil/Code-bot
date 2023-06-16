from random import randint
import discord
import os
from dotenv import load_dotenv
import asyncio
import threading
from conn_db import Connection
import time
from datetime import datetime

class Utils:
    def __init__(self, pessoa=False):
        load_dotenv()
        self.pessoa = pessoa
        if self.pessoa:
            self.guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        self.connector = Connection()
        self.linguagens = {
            "python": {
                "channelId": 1007661768740454450
            }
        }
        
        '''
        N_INICIANTE=0
N_GAFANHOTO=150
N_JUNIOR=300
N_PLENO=500
N_SENIOR=700
N_WEBMASTER=1000
        '''
        self.ranking = {
            "N_INICIANTE": 'i',
            "N_GAFANHOTO": 'g',
            "N_JUNIOR": 'j',
            "N_PLENO": 'p',
            "N_WEBMASTER": 'w',
            "N_SENIOR": "s"
        }
        
        self.cargoList = {
            "react_icon": [1007666765892964442, "react"],
            "html_icon": [1007645794683334687, "HTML e CSS"],
            "css_icon": [1007645794683334687, "HTML e CSS"],
            "python_icon": [1007645678589186109, "python"],
            "js_icon": [1007645747719712768, "javascript"],
            "php_icon": [1007645637896061002, "php"],
            "cs_icon": [1007645892028932107, "C#"],
            "cplus_icon": [1007645941702070272, "C++"],
            "sql_icon": [1011484510333972562, "sql"],
            "windows_icon": 1007914490806939649,
            "linux_icon": 1007914480279224320,
            "mac_icon": 1007914566371512320,
            "🔵": 1014284598693335170,
            "🔴": 1014284532993753169,
            "🟣": 1014286037293482027,
            "certo_icon": True,
            "lampada_icon": True
        }

        self.mensagensGeral = [
            "Olha o membro novo! @$pessoa ta na área!",
            "Gente nova! @$pessoa chegou chegando, comprimentem ele!",
            "@$pessoa, sinta se em casa",
            "Oi @$pessoa! Esse é o chat geral, só não repara na bagunça ksks",
            "@$pessoa, aqui ta o povão, manda um Oi para todo mundo te conhecer melhor!",
            "Membro novo na area... @$pessoa, esse é chat geral, sinta se em casa",
            "Eai @$pessoa! Como vai cara? A galera quer te conhecer, fala um pouco sobre você"
        ]
        self.mensagensInteressadoProjeto = [
            "@$pessoa parece que você se interessou nesse projeto! Diz ai o que você achou mais legal!",
            "@$pessoa, gostou do projeto? Fala um pouco de você para os membros te conhecerem melhor!",
            "Lider de projeto, @$pessoa está interessado no projeto! Fica de olho",
            "Gente! @$pessoa também ta interessado no projeto ai! Manda uma mensagem no chat para animar ele a participar!"
        ]
        
        self.marcacoesLinguagem = [
            "@$pessoa, você é novo na em @$linguagem? Ou já é experiente? Qual foi seu ultimo projeto? Manda ai!",
            "Oi @$pessoa! Essa é a galera de @$linguagem, eles devem estar doidos para te conhecer, se apresenta ai!",
            "Eai @$pessoa, como vai? Essa é a turma de @$linguagem, manda um Oi para eles saberem que você chegou!",
            "Rapaziada... Chegou agora um cara que é da pesada... O nome dele é @$pessoa e ele tambem manja de @$linguagem, comprimentem ele!",
            "@$pessoa, não precisa ficar tímido! Você é de casa agora, manda um oi para galera!",
            "Eai @$pessoa! Tudo bem contigo cara? Essa é a galera de @$linguagem. Se apresenta para eles te conhecerem!"
        ]
    async def mensagemIniciacao(self, user, geral):
        mensagem = self.mensagensGeral[randint(0, len(self.mensagensGeral)-1)].replace("@$pessoa", user.mention)
        await geral.send(mensagem)

    async def mensagemIniciacaoLinguagem(self, pessoa, linguagem, channel):
        mensagem = self.marcacoesLinguagem[randint(0, len(self.marcacoesLinguagem)-1)].replace("@$pessoa", pessoa.mention).replace("@$linguagem", linguagem)
        await channel.send(mensagem)
        
    async def removeReaction(self, message, emoji, member, type="project"):
        if type == "project":
            await member.send("Sua solicitação de participar do projeto está sendo avaliada! Em breve o lider de projeto entrará em contato")
        await asyncio.sleep(2)
        await message.remove_reaction(emoji, member)

    async def sendMensagemBoasVindasDm(self, member):
        self.guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        boas_vindas = self.guild.get_channel(int(os.environ["BOAS_VINDAS_CHANNEL"]))
        conheca_channel = self.guild.get_channel(int(os.environ["CONHECA_CHANNEL"]))
        como_ganhar_pontos = self.guild.get_channel(int(os.environ["COMO_GANHAR_PONTOS_CHANNEL"]))
        comandos = self.guild.get_channel(int(os.environ["COMMAND_CHANNEL"]))
        cargos = self.guild.get_channel(int(os.environ["CARGOS_CHANNEL"]))
        adm = self.guild.get_member(int(os.environ["ADM_ID"]))
        embed = discord.Embed(
            title="Bem vindo a Code Company!",
            description='''
Espero que goste da nossa comunidade!
Caso saia do servidor, sua conta e seus dados permaneceram por no máximo 7 dias!
Se não retornar eles serão APAGADOS!
''',
            color=discord.Color.dark_blue()
        )

        embed.add_field(name="Conheça melhor nosso servidor pelo nosso canal:", value=f"{conheca_channel.mention}", inline=False)#"Descubra o servidor pelo nosso canal:"
        embed.add_field(name="Aprenda a ganhar bucks na comunidade", value=f"{como_ganhar_pontos.mention}", inline=False)
        embed.add_field(name="Ganhe cargos", value=f"{cargos.mention}", inline=False)

        embed2 = discord.Embed(
            title="Use esses comandos",
            color=discord.Color.dark_blue()
        )
        embed2.add_field(name="Chat de comandos", value=f"{comandos.mention}")
        embed2.add_field(name="/profile", value="Para ver seu perfil e ver seus bucks", inline=False)
        embed2.add_field(name="/ranking", value="Para ver o ranking de níveis do servidor, e em qual você está!", inline=False)
        embed2.add_field(name="/server info", value="Para ver informações do servidor", inline=False)
        embed2.add_field(name="/help", value="Para descobrir mais comandos disponíveis no Code Bot", inline=False)
        embed2.add_field(name="/ping", value="Responde Pong se o bot estiver vivo", inline=False)
        embed2.add_field(name="/bump", value="Para ajudar a comunidade a ser melhor rankiada no Disboard", inline=False)
        
        await member.send(embeds=[embed, embed2])
    
    async def isUpRanked(self, pontos, idUser):
        ranking = await self.whatRanking(pontos, type="complete")
        guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        idRole = int(os.environ[ranking + "_CARGO"])
        member = guild.get_member(int(idUser))
        for r in member.roles:
            if r.id == idRole:
                return False
                
        return idRole

    async def pointMessage(self, idUser, pontos, motivo):
        guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        pointChat = guild.get_channel(int(os.environ["PONTOS_ID"]))
        user = self.pessoa.get_user(int(idUser))
        atualPontos = await self.connector.getPontos(int(idUser))
        atualRanking = await self.connector.getRanking(int(idUser))
        atualRanking = await self.formatingRankingName(atualRanking, tipo="letter")
        embed = discord.Embed(
            title=f"{user.name} ganhou 🪙 {int(pontos)} Bucks!",
            description=motivo,
            color=discord.Color.gold()
        )
        embed.add_field(name="Seus bucks:", value=f"🪙 {int(atualPontos)} bucks")
        embed.add_field(name="Ranking:", value=f"🏅 {atualRanking}")
        
        await self.connector.setHistoricoPontos(idUser, pontos, motivo)
        await pointChat.send(str(user.mention), embed=embed)
    
    async def whatRanking(self, pontos, type="letter"):
        rankingList = [x for x in self.ranking]

        for c in range(0, len(rankingList)):
            r = rankingList[c]
            ranking = int(os.environ[r])
            if ranking == pontos:
                rankingUser = r

            elif ranking > pontos and int(os.environ[rankingList[c - 1]]) <= pontos:
                rankingUser = rankingList[c - 1]
            
            elif c == len(rankingList) - 1 and pontos >= int(os.environ[r]):
                rankingUser = rankingList[len(rankingList)-1]

        if type == "complete":
            return rankingUser
        else:
            return self.ranking[rankingUser]
    
    async def formatingRankingName(self, name, tipo="str"):
        if tipo == "str":
            name = str(name)[2:].capitalize()

        elif tipo == "letter":
            r = [x for x in self.ranking]
            for c in r:
                if self.ranking[c] == name:
                    name = str(c)[2:].capitalize()
        
        return name
    
    async def givingNivelCargo(self, idUser, pontos):
        nivel = await self.whatRanking(pontos, type="complete")
        guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        member = guild.get_member(idUser)
        role = guild.get_role(str(nivel) + "_CARGO")
        await member.add_roles(role)
        

    async def rankingMessage(self, idUser):
        guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        pointChat = guild.get_channel(int(os.environ["PONTOS_ID"]))
        user = self.pessoa.get_user(int(idUser))
        atualRanking = await self.connector.getRanking(int(idUser))
        atualRanking = await self.formatingRankingName(atualRanking, tipo="letter")
        embed = discord.Embed(
            title=f"{user.name} subiu de nível!",
            color=discord.Color.blue()
        )
        embed.add_field(name="Ranking:", value=f"🏅 {atualRanking}")

        if str(atualRanking).lower() != "iniciante":
            await pointChat.send(str(user.mention), embed=embed)
    
    async def setPoint(self, pontos, idUser):
        pontosAtual = await self.connector.getPoint(int(idUser))
        pontosAlterados = int(pontos) + int(pontosAtual)
        await self.checkingRanking(pontosAlterados, idUser)
        #await self.connector.setPoint(pontosAlterados, idUser)
        role = await self.isUpRanked(pontosAlterados, idUser)
        if role:
            await self.rankingMessage(idUser)
            guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
            member = guild.get_member(idUser)
            await member.add_roles(role)
            await self.removingOtherRolesRanking(role, member)
        
    async def removingOtherRolesRanking(self, role, member):
        for r in member.roles:
            for c in await self.connector.getRankingRolesId(self.ranking):
                if r.id == c and c != role.id:
                    await member.remove_roles(r)
        
    
    async def checkingRanking(self, pontos, idUser):
        await self.connector.setPoint(pontos, int(idUser))
        if await self.whatRanking(pontos) != await self.connector.getRanking(idUser):
            return await self.connector.setRanking(idUser, await self.whatRanking(pontos))
        return False

    async def dateAtual(self):
        now = datetime.now()

        atual = f"{now.day}/{now.month}/{now.year} {now.hour}:{now.minute}:{now.second}"

        d1 = datetime.strptime(atual, "%d/%m/%Y %H:%M:%S")
        return d1
    
    async def newMember(self, idUser, name, descriminator):
        await self.connector.connect()
        self.connector.cursor.execute(f"SELECT * FROM membros WHERE idUser = {idUser};")
        data = self.connector.cursor.fetchone()
        if data:
            data = list(data)
            self.connector.cursor.execute(f"UPDATE membros SET inativo = FALSE, dataInativo = NULL WHERE idUser = {int(data[0])};")
        else:
            self.connector.cursor.execute(f"INSERT INTO membros (idUser, name, descriminator) VALUES ({idUser}, '{name}', '{descriminator}');")
        
        self.connector.con.commit()
    
    async def desabilitingMember(self, idUser):
        await self.connector.connect()
        data = await self.dateAtual()
        self.connector.cursor.execute(f"UPDATE membros SET inativo = TRUE, dataInativo = '{str(data)}' WHERE idUser = {idUser};")
        self.connector.con.commit()
    
    async def excluingMember(self, idUser):
        await self.connector.connect()
        self.connector.cursor.execute(f"DELETE FROM membros WHERE idUser = {idUser};")
        self.connector.con.commit()

    async def createNotifyJob(self, job):
        await self.connector.connect()
        data = await self.get_date()
        self.connector.cursor.execute("INSERT INTO notifyJobs (nome, link, bids, proposal, bidTime, valor, skills, bidLink, client_cidade, client_pais, client_rate, client_date, created_at) VALUES ('{0}', '{1}', {2}, '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}');".format(await self.connector.bind_sqli(job["nome"]), job["link"], job["bids"], await self.connector.bind_sqli(job["proposal"]), job["bidTime"], job["valor"], job["skills"], job["bidLink"], job["client"]["cidade"], job["client"]["pais"], job["client"]["rate"], job["client"]["date"], data))
        self.connector.con.commit()
    
    async def deleteQuestionary(self, channelId):
        await self.connector.connect()
        self.connector.cursor.execute(f"DELETE FROM questionry WHERE channelId = {channelId};")
        self.connector.con.commit()

    async def cleanQuestionaryData(self, channelId):
        await self.connector.connect()
        self.connector.cursor.execute(f"DELETE FROM responseQuestionary WHERE questionaryId = {channelId};")
        self.connector.cursor.execute(f"DELETE FROM questionary WHERE channelId = {channelId};")
        self.connector.con.commit()

    async def autoDmChannelDelete(self, channel):
        await asyncio.sleep(5)
        await self.connector.deleteDmChannel(channel)
    
    async def formantandoHora(self, hora):
        if len(str(hora)) == 1:
            return f"0{hora}"
        return str(hora)
    
    async def ajeitandoFuso(self, hora):
        #tenho que fazer menos 3
        fuso = 3
        hora = int(hora)
        if hora - fuso > 0:
            return hora - fuso
        else:
            d = fuso - hora
            return 24 - d
    
    async def contatoPosFinalizacao(self, pessoa, user):
        await user.send("Sua proposta de freelance está sendo avaliada...")
    
    async def diferenca_dias(self, d1):
        if d1 != "":
            now = datetime.now()
            data = f"{await self.formantandoHora(now.day)}/{await self.formantandoHora(now.month)}/{await self.formantandoHora(now.year)} {await self.formantandoHora(await self.ajeitandoFuso(now.hour))}:{await self.formantandoHora(now.minute)}:{await self.formantandoHora(now.second)}"
            try:
                d1 = datetime.strptime(d1, "%d/%m/%Y %H:%M:%S")
                d2 = datetime.strptime(data, "%d/%m/%Y %H:%M:%S")
            except:
                print("2 opcao")
                d1 = datetime.strptime(d1, "%d/%m/%Y")
                d2 = datetime.strptime(data, "%d/%m/%Y")
            diferenca = (d2 - d1).days
            return diferenca
        return False
        
    async def just_get_hours(self):
        now = datetime.now()
        return f"{await self.formantandoHora(await self.ajeitandoFuso(now.hour))}:{await self.formantandoHora(now.minute)}"
    
    async def just_get_day(self):
        now = datetime.now()
        return f"{await self.formantandoHora(now.day)}/{await self.formantandoHora(now.month)}/{await self.formantandoHora(now.year)}"
    
    async def get_date(self):
        now = datetime.now()
        hour = "00" if await self.formantandoHora(now.hour) == "24" else await self.formantandoHora(now.hour)
        return f"{await self.formantandoHora(now.day)}/{await self.formantandoHora(now.month)}/{await self.formantandoHora(now.year)} {hour}:{await self.formantandoHora(now.minute)}:{await self.formantandoHora(now.second)}"

    async def mensagemInativo(self, member):
        self.guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
        geral = self.guild.get_channel(int(os.environ["GERAL_CHANNEL"]))
        embed = discord.Embed(
            title="A comunidade ta com saudade de você!",
            description='''
Eai cara, como você ta? Faz tempo que não manda mensagem lá na Code Company!
Vim dizer que a galera já ta com saudade de ti.

Manda um bom (dia, tarde ou noite) lá, hoje ta bom para bater um papo não é?
''',    
            color=discord.Color.dark_blue()
        )
        embed2 = discord.Embed(
            title="Para que toda essa distância?",
            description=f'''
Oi {member.name}! Tudo bem contigo?
A Code Company ta com saudade de você já cara!
Para que ficar todo esse tempo sem mandar mensagem? 😢
Faz o seguinte...
Vai lá no {geral.mention} e fala assim:
- Eai rapaziada!
Você vai ver como a galera tambem tava com saudade!
''',
            color=discord.Color.dark_blue()
        )
        embed3 = discord.Embed(
            title="Você está PERDENDO BUCKS!",
            description=f'''
Eai {member.name} como você ta?
Cuidado ai em cara, vim para te dar um toque.
Não é bom ficar muito tempo sem interagir na Code Company não,
Desse jeito a galera vai passar na sua frente!
Manda uma mensagem lá! Agora mesmo tem um monte de gente esperando para falar contigo!     
{geral.mention}             
''',
            color=discord.Color.dark_blue()
        )
        
        embed4 = discord.Embed(
            title="Eai rapaz, quanto tempo!",
            description=f'''
Aconteceu alguma coisa {member.name}? Como é que você ta cara!
Vim aqui porque vi que tu ta um tempo sem interagir na Code Company, o que houve?
A galera já ta com saudade de você! Manda uma mensagem lá
{geral.mention}
''',
            color=discord.Color.dark_blue()
        )
        
        embed5 = discord.Embed(
            title="Man, como tu ta?",
            description=f'''
Vi que você ta um tmepo sem interagir na Code Company, tudo bem contigo?
Não esqueçe da gente não! Da uma passada lá, a galera já deve estar com saudade.
Pode sumir assim não, pô!
{geral.mention}
'''
        )
        
        lista = [embed, embed2, embed3, embed4, embed5]
        random = lista[randint(0, len(lista)-1)]
        await member.send(embed=random)
    
    async def avisandoJobAdm(self, channelId, pessoa):
        informacoes = {}
        message_channel = pessoa.get_channel(int(os.environ["JOBS_FREELANCE_CHANNEL"]))
        responseQuestionary = await self.connector.getResponseQuestionary(channelId)
        for c in responseQuestionary:
            stage = int(c[3])
            if stage == 2:
                informacoes["preco"] = c[2]
                informacoes["channelId"] = c[1]
            elif stage == 3:
                informacoes["prazo"] = c[2]
            elif stage == 4:
                informacoes["proposal"] = c[2]
            elif stage == 5:
                informacoes["milestone"] = c[3]
        print(informacoes)
        questionary = await self.connector.getQuestion(informacoes["channelId"])
        member = pessoa.get_user(questionary[informacoes["channelId"]]["idUser"])
        idNotifyJob = questionary[informacoes["channelId"]]["idNotifyJob"]
        notifyJob = await self.connector.getNotifyJobs(idNotifyJob)
        embed = discord.Embed(
            title="Nova proposta de job!",
            description=f'Job em pendência!',
            color = discord.Color.blue(),
        )
        embed.set_author(name="Freelancer.com", icon_url="https://public.dm.files.1drv.com/y4mT79-C3qewZd_gISqDAGMaD_MKSJIz_f_J2RSCFdntZsobFRWWh-Dk6MgPy5OBVPrIPKcohE-txgAooe6OlVffuJcjRqHWjMT-ZfsbxH4xlpzpbxkZHNYswoxiHWJcHT1ptHeusIc4fA-fFAywTH6dF44bwFx4ggYUDODhWvdqdNAviei2IYmoFzLIUAr915bc4Uihnbt65Mm87u9QnpexLrMTzws7BspOrJxWRntENg?encodeFailures=1&width=1920&height=882")
        embed.set_footer(text="Freelancer.com", icon_url="https://public.dm.files.1drv.com/y4mT79-C3qewZd_gISqDAGMaD_MKSJIz_f_J2RSCFdntZsobFRWWh-Dk6MgPy5OBVPrIPKcohE-txgAooe6OlVffuJcjRqHWjMT-ZfsbxH4xlpzpbxkZHNYswoxiHWJcHT1ptHeusIc4fA-fFAywTH6dF44bwFx4ggYUDODhWvdqdNAviei2IYmoFzLIUAr915bc4Uihnbt65Mm87u9QnpexLrMTzws7BspOrJxWRntENg?encodeFailures=1&width=1920&height=882")

        embed.add_field(name="Responsável:", value=f"{member.name}#{member.discriminator}", inline=False)
        embed.add_field(name="Responsável ID:", value=f"{member.id}", inline=False)
        embed.add_field(name="Job Link:", value=f"{notifyJob[2]}", inline=False)
        embed.add_field(name="Preço:", value=f'{informacoes["preco"]}', inline=False)
        embed.add_field(name="Prazo:", value=f'{informacoes["prazo"]} dias', inline=False)
        embed.add_field(name="Proposta:", value=f'{informacoes["proposal"]}', inline=False)
        embed.add_field(name="Milestone:", value=f'{informacoes["milestone"]}', inline=False)
        embed.add_field(name="MessageID:", value=f'{notifyJob[13]}', inline=False)
        await message_channel.send(embed=embed)

if __name__ == "__main__":
    starter = Utils()
    print(asyncio.run(starter.formatingRankingName("l", tipo="letter")))
    # h = asyncio.run(starter.get_dia_atual())
    # print(len(h))
            