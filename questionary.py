import discord
from utils import Utils
from conn_db import Connection
import asyncio

class Questionary:
    def __init__(self):
        self.connection = Connection()
        self.utils = Utils()
        self.questions = {
            "interessadoJob": self.interessadoJob,
            "contaBancaria": self.contaBancaria
            #"outFeedback": self.outFeedback
        }
    
    async def recibeResponse(self, response, channelId, pessoa=None, channel=None):
        #print("Recebi uma resposta!")
        self.channels = await self.connection.getQuestion(channelId)
        #print(self.channels)
        funcao = self.questions[self.channels[channelId]["question"]]
        await funcao(int(self.channels[channelId]["stage"]), channelId, response, pessoa, channel)
    
    async def getChannels(self):
        await self.connection.connect()
        self.connection.cursor.execute(f"SELECT channelId FROM questionary;")
        fetch = self.connection.cursor.fetchall()
        if len(fetch) == 0:
            return []
        else:
            return list(fetch)
    
    async def finsishQuestion(self, stage, channel, messageEdit, content):
        pass
    
    async def closeCanal(self, channelId, pessoa):
        channel = pessoa.get_channel(channelId)
        await self.connection.deleteDmChannel(channel)
        #await self.connection.connect()
        #self.connection.cursor.execute(f"DELETE FROM responseQuestionary WHERE questionaryId = {channel.id};")
        #self.connection.cursor.execute(f"DELETE FROM questionary WHERE channelId = {channel.id})")
        #self.connection.con.commit()
        await channel.send("Fechando o canal!")
        await asyncio.sleep(2)
        await channel.delete()
        

    async def startQuestion(self, channelId, question, idNotifyJob=None, pessoa=None, channel=None, idUser=None, message=None):
        if str(idUser) == "None":
            idUser = "NULL"
        if str(idNotifyJob) == "None":
            idNotifyJob = "NULL"
        await self.connection.connect()
        self.connection.cursor.execute(f"INSERT INTO questionary (channelId, question, idNotifyJob, idUser) VALUES ({channelId}, '{question}', {idNotifyJob}, {idUser});")
        self.connection.con.commit()
        callback = self.questions[question]
        if (question == "interessadoJob" or question == "outFeedback"):
            await callback(0, channelId, pessoa=pessoa, channel=channel)
        else:
            await callback(0, channelId)
    
    async def contaBancaria(self, conta):
        print("Pego a conta bancaria")
    
    async def outFeedback(self, stage, user, response=None,  pessoa=None, channel=None):
        user = pessoa.get_user(user)
        feedback = pessoa.get_channel(1024097312139653180)
        if stage == 0:
            await user.send("Oi, vi que você saiu do servidor. Poderia me dar um feedback do porque? Iremos usar sua dica para melhor a experiência da Code Company (envie em apenas uma mensagem).\nObrigado por contribuir")
            await self.connection.updateQuestion(stage + 1, user.id)
        elif stage == 1:
            if str(type(response)) == "<class 'discord.message.Message'>":
                #await self.connection.insertResponseQuestionary(user, await self.connection.bind_sqli(response.content), stage)
                embed = discord.Embed(
                    title=f"{user}",
                    description=f"{response.content}",
                    color=discord.Color.red()
                )
                await feedback.send(f"{user} disse que:\n{response.content}")
                await feedback.send("Obrigado pelo feedback, caso queira voltar estamos sempre de portas abertas!\nhttps://discord.gg/ddScwkYryg")
                await self.utils.deleteQuestionary(user.id)

    async def interessadoJob(self, stage, channelId, response=None,  pessoa=None, channel=None):
        question = await self.connection.getQuestion(channelId)
        guild = pessoa.get_guild(1007633662847762503)
        certo = discord.utils.get(guild.emojis, name="certo_icon")
        errado = discord.utils.get(guild.emojis, name="errado_icon")
        change = True
        if stage == 0:
            await self.connection.connect()
            self.connection.cursor.execute(f"SELECT * FROM dmChannel WHERE idChannel={channelId}")
            member = list(self.connection.cursor.fetchall())[0][0]
            self.connection.cursor.execute(f"SELECT * FROM jobs WHERE responsavel = {member};")

            await channel.send("|" + ("-="*20) + "|")
            await channel.send("Parece que você está interessado em um freelance")
            trabalho = await channel.send(":construction_worker: - Você possui as habilidades para realizar o trabalho?")
            await trabalho.add_reaction(certo)
            await trabalho.add_reaction(errado)

        elif stage == 1: #discord.raw_models.RawReactionActionEvent - <class 'discord.message.Message'>
            if str(type(response)) == "<class 'discord.raw_models.RawReactionActionEvent'>":
                if response.emoji.name == "certo_icon":
                    await channel.send(":money_with_wings: - Qual é o seu preço? (envie por escrito na mesma moeda descrita no job)")
                else:
                    await channel.send("Procure outro job que você possua as habilidades!")
                    change = False
                    await asyncio.sleep(2)
                    await self.closeCanal(channelId, pessoa)
        elif stage == 2:
            if str(type(response)) == "<class 'discord.message.Message'>":
                await self.connection.insertResponseQuestionary(channelId, await self.connection.bind_sqli(response.content), stage)
                await channel.send("Quanto tempo (em dias) você precisa para finalizar o freelance? (Máximo: 7 dias)")
        elif stage == 3:
            if str(type(response)) == "<class 'discord.message.Message'>":
                try:
                    response = int(response.content)
                except:
                    await channel.send("Tempo invalido! Envie apenas o número. EX: 5")
                    change = False
                else:
                    if response > 7:
                        await channel.send("O tempo maximo para finalização são 7 dias!")
                        await channel.send("Se você não consegue realizar o trabalho nesse prazo. Não envie nada, pois este canal se encerrará sozinho. Procure outro job!")
                        await channel.send("Caso consiga realizar o trabalho, envie o prazo novamente!")
                        change = False
                    else:
                        await self.connection.insertResponseQuestionary(channelId, response, stage)
                        await channel.send("Sua proposta deve ser um texto bem redigído que diz porque você deve pegar esse trabalho, e o que pode fazer pelo cliente. (Aspas e alguns caracters especiais serão retirados)\nEnvie aqui:")
        elif stage == 4:
            if str(type(response)) == "<class 'discord.message.Message'>":
                if len(response.content) < 10 or len(response.content) > 255:
                    await channel.send("Sua resposta deve ter entre 100 e 255 caracteres!\nEnvia de novo mais caprichado!")
                    change = False
                else:
                    await self.connection.insertResponseQuestionary(channelId, await self.connection.bind_sqli(response.content), stage)
                    await channel.send("Agora mande um passo a passo dizendo como você vai executar a tarefa: (Aspas e alguns caracters especiais serão retirados)")
        elif stage == 5:
            if str(type(response)) == "<class 'discord.message.Message'>":
                if len(response.content) < 10 or len(response.content) > 255:
                    await channel.send("Sua resposta deve ter entre 10 e 255 caracteres!\nEnvia de novo mais caprichado!")
                    change=False
                else:
                    await self.connection.insertResponseQuestionary(channelId, await self.connection.bind_sqli(response.content), stage)
                    await channel.send("Sua proposta será enviada e avaliada pelo ADM, ele deverá te enviar uma mensagem dizendo como foi\nDesde já... Obrigado contribuir com a Code Company")
                    await channel.send("Esse canal será encerrado!")
                    user = pessoa.get_user(response.author.id)
                    await self.utils.contatoPosFinalizacao(pessoa, user)
                    await self.utils.avisandoJobAdm(channelId, pessoa)
                    await self.utils.cleanQuestionaryData(channelId)
                    await self.closeCanal(channelId, pessoa)
            
        if change:
            await self.connection.updateQuestion(stage + 1, channelId)

if __name__ == "__main__":
    starter = Questionary()
    channels = asyncio.run(starter.getChannels())
    print(channels)
    #asyncio.run(starter.interessadoJob(0, None, 1017619600600485910))