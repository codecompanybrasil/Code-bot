import mysql.connector
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime

class Connection:
    def __init__(self):
        load_dotenv()
        asyncio.run(self.connect())
    
    async def connect(self):
        while True:
            try:
                self.con = mysql.connector.connect(
                    user=os.environ["DB_USER"],
                    password=os.environ["DB_PASSWORD"],
                    host=os.environ["DB_HOST"],
                    port=os.environ["DB_PORT"],
                    database=os.environ["DB_DATABASE"]
                )

                self.cursor = self.con.cursor()
            except:
                await asyncio.sleep(2)
            else:
                break
            
    
    async def gettingChannelFreelanceByClient(self, client):
        await self.connect()
        self.cursor.execute(f"SELECT idChannel FROM jobs WHERE client = 'pontos{self.bind_sqli(client)}'")

    async def getFlag(self, nomeUs):
        await self.connect()
        self.cursor.execute(f"SELECT flag FROM paises WHERE nomeUs = '{self.bind_sqli(nomeUs)}';")
        fetch = self.cursor.fetchall()
        if fetch != 0:
            return list(fetch[0])[0]
        else:
            return ""
    
    async def insertQuestion(self, channelId, stage, question):
        await self.connect()
        self.cursor.execute(f"INSERT INTO questionary (channelId, stage, question) VALUES ({channelId}, {stage}, '{question}');")
        self.con.commit()
    
    async def getPontos(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT pontos FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return list(data)[0]
        return False
    
    async def getRanking(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT ranking FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return list(data)[0]
        return False

    async def getOfensiva(self, idUser, reverse=False):
        await self.connect()
        if reverse:
            self.cursor.execute(f"SELECT ofensivaReverse FROM membros WHERE idUser = {idUser};")
        else:
            self.cursor.execute(f"SELECT ofensiva FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return list(data)[0]
        return None
    
    async def addOfensiva(self, idUser, zerar=False, reverse=False):
        await self.connect()
        if reverse:
            ofensiva = int(await self.getOfensiva(idUser, reverse=True))
            sub = "ofensivaReverse"
        else:
            ofensiva = int(await self.getOfensiva(idUser))
            sub = "ofensiva"
            
        if zerar:
            self.cursor.execute(f"UPDATE membros SET {sub} = 0 WHERE idUser = {idUser};")
        else:
            self.cursor.execute(f"UPDATE membros SET {sub} = {ofensiva + 1} WHERE idUser = {idUser};")
        self.con.commit()
    
    async def setRanking(self, idUser, ranking):
        await self.connect()
        self.cursor.execute(f"UPDATE membros SET ranking = '{ranking}' WHERE idUser = {idUser};")
        self.con.commit()
    
    async def isAdmin(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM admin WHERE id = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return True
        return None
    
    async def setPoint(self, pontos, idUser):
        await self.connect()
        self.cursor.execute(f"UPDATE membros SET pontos = {pontos} WHERE idUser = {idUser};")
        self.con.commit()

    async def getPoint(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT pontos FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return list(data)[0]
        return None

    async def getProjectByChannel(self, idChannel):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM projetos WHERE idChannel = {idChannel};")
        data = self.cursor.fetchone()
        if data:
            return list(data)
        return None
    
    async def getQuestion(self, channelId):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM questionary WHERE channelId = {channelId}")
        response = list(self.cursor.fetchall())
        if response != []:
            response = response[0]
        return {
            response[0]: {
                "stage": response[1],
                "question": response[2],
                "idNotifyJob": response[3],
                "idUser": response[4]
            }
        }
    
    async def getDiaryMessage(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT diaryMessage FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return list(data)[0]
        return None
    
    async def setHistoricoPontos(self, idUser, pontos, motivo):
        await self.connect()
        self.cursor.execute(f"INSERT INTO historicoPontos (idUser, pontos, motivo) VALUES ({idUser}, {pontos}, '{motivo}');")
        self.con.commit()

    async def setDiaryMessage(self, idUser, value=True):
        await self.connect()
        self.cursor.execute(f"UPDATE membros SET diaryMessage = {str(value).upper()} WHERE idUser = {idUser};")
        self.con.commit()

    async def existeProject(self, idChannel):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM projetos WHERE idChannel = {idChannel};")
        data = self.cursor.fetchone()
        if data:
            return True
        return None
    
    async def isLiderDeProjeto(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT isLiderDeProjeto FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if list(data):
            return True
        return False

    async def addMensagemProjeto(self, idMessage, idChannel):
        await self.connect()
        self.cursor.execute(f"UPDATE projetos SET idMensagemProjeto = {idMessage} WHERE idChannel = {idChannel};")
        self.con.commit()

    async def getIdMensagensProjetos(self):
        await self.connect()
        self.cursor.execute(f"SELECT idMensagemProjeto FROM projetos;")
        data = self.cursor.fetchall()
        if data:
            return list(data)
        return None
    
    async def getIdChannelByIdMensagemProjetos(self, idMensagemProjeto):
        await self.connect()
        self.cursor.execute(f"SELECT idChannel FROM projetos WHERE idMensagemProjeto = {idMensagemProjeto};")
        data = self.cursor.fetchone()
        if data:
            return data[0]
        return None

    async def setRoleProjetos(self, idRole, idChannel):
        await self.connect()
        self.cursor.execute(f"UPDATE projetos SET idRole = {idRole} WHERE idChannel = {idChannel};")
        self.con.commit()
        
    async def setLiderDeProjeto(self, idUser, status=True):
        await self.connect()
        self.cursor.execute(f"UPDATE membros SET isLiderProjeto = {str(status).upper()} WHERE idUser = {idUser};")
        self.cursor.execute(f"UPDATE projetos SET idLiderProjeto = {idUser};")
        self.con.commit()
    
    async def insertTaskProject(self, task, idUser, idProjeto):
        await self.connect()
        self.cursor.execute(f"INSERT INTO taskProjetos (task, idUser, idProjeto) VALUES ('{task}', {idUser}, {idProjeto});")
        self.con.commit()

    async def insertNewProject(self, name, idChannel, githubLink=None):
        print("INserted")
        await self.connect()
        if githubLink:
            self.cursor.execute(f"INSERT INTO projetos (name, githubLink, idChannel) VALUES ('{name}', '{githubLink}', {idChannel});")
        else:
            self.cursor.execute(f"INSERT INTO projetos (name, idChannel) VALUES ('{name}', {idChannel});")
        self.con.commit()

    async def updateQuestion(self, stage, channelId):
        await self.connect()
        self.cursor.execute(f"UPDATE questionary SET stage = {stage} WHERE channelId = {channelId};")
        self.con.commit()

    async def getDmChannel(self, userId):
        print(userId)
        await self.connect()
        self.cursor.execute(f"SELECT * FROM dmChannel WHERE idUser = {userId};")
        dm = self.cursor.fetchall()
        print(dm)
        if len(dm) != 0:
            return dm[0][1]
        return False
    
    async def deleteProjectByChannelId(self, idChannel):
        await self.connect()
        self.cursor.execute(f"DELETE FROM projetos WHERE idChannel = {idChannel};")
        self.con.commit()
    
    async def deleteMembroProjectByChannelId(self, idChannel):
        await self.connect()
        self.cursor.execute(f"DELETE FROM projetos WHERE idChannel = {idChannel};")
        self.con.commit()
    
    async def getMembroProjectByChannelId(self, idChannel):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM membroProjeto WHERE idChannel = {idChannel};")
        data = self.cursor.fetchall()
        if data:
            return list(data)
        return None
    
    async def getProfile(self, idUser):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM membros WHERE idUser = {idUser};")
        data = self.cursor.fetchone()
        if data:
            return list(data)
        return None
    
    async def getRankingRolesId(self, ranking):
        roles = []
        for r in [x for x in ranking]:
            roles.append(int(os.environ[str(r + "_CARGO")]))
        
        return roles
            
    
    async def refreshProfile(self, idUser, name, descriminator):
        await self.connect()
        self.cursor.execute("UPDATE membros SET name = '{name}', descriminator = '{descriminator}' WHERE idUser = {idUser};")
        self.con.commit()
    
    async def getDmChannelByName(self, name, purpose):
        await self.connect()
        self.cursor.execute(f"SELECT idUser, idChannel FROM dmChannel WHERE nome = '{name}' AND purpose = '{purpose}';")
        result = list(self.cursor.fetchall()[0])
        print(f"ListCHannel: {result}")
        return result

    async def existEvent(self, idChannel):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM eventos WHERE idChannel = {idChannel};")
        if self.cursor.fetchone():
            return True
        return False
    
    async def addParticipanteEvent(self, idUser, idChannel):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM participantesEvento WHERE idUser = {idUser};")
        if not self.cursor.fetchone():
            self.cursor.execute(f"INSERT INTO participantesEvento (idUser, idChannel) VALUES ({idUser}, {idChannel});")
            self.con.commit()
    
    async def isEvent(self):
        await self.connect()
        self.cursor.execute(f"SELECT idChannel FROM eventos;")
        data = self.cursor.fetchone()
        if data:
            return list(data)
        return None

    async def getParticipantesEvent(self, idChannel):
        await self.connect()
        self.cursor.execute("SELECT * FROM participantesEvento;")
        data = self.cursor.fetchall()
        if data:
            return list(data)
        return None

    async def excluingEvent(self, idChannel):
        await self.connect()
        self.cursor.execute(f"DELETE FROM eventos WHERE idChannel = {idChannel};")
        self.con.commit()
    
    async def deleteDmChannel(self, channel):
        await self.connect()
        self.cursor.execute(f"DELETE FROM dmChannel WHERE idChannel = {channel.id};")
        self.con.commit()
    
    async def setDmChannel(self, idUser, idChannel, nome, created_at, purpose=False):
        await self.connect()
        if purpose:
            self.cursor.execute(f"INSERT INTO dmChannel (idUser, idChannel, nome, created_at, purpose) VALUES ({idUser}, {idChannel}, '{nome}', '{created_at}', '{purpose}');")
        else:
            self.cursor.execute(f"INSERT INTO dmChannel (idUser, idChannel, nome, created_at) VALUES ({idUser}, {idChannel}, '{nome}', '{created_at}');")
        self.con.commit()
    
    async def bind_sqli(self, string):
        string = str(string)
        characters = ["'", '"', "union", ">", "<", "(", ")", "--", "select", "$", "{", "}", "://"]
        for c in characters:
            while string.find(c) != -1:
                string = string.replace(c, "")
        return string

    async def existeJob(self, link):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM jobs WHERE link = '{link}';") #mysql.connector.errors.OperationalError
        if len(self.cursor.fetchall()) != 0:
            return False
        return True
    
    async def insertJob(self, data, idChannel, client): #SEM PRAZO ASYNC DEFINIDO
        await self.connect()
        self.cursor.execute("INSERT INTO jobs (nome, link, responsavel, proposal, bidTime, valor, skills, bidLink, notifyId, idChannel, client) VALUES ('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', {}, {}, '{}')".format(data[1], data[2], data[14], data[4], data[5], data[6], data[7], data[8], data[0], idChannel, client))
    
    async def insertMessageClient(self, message, horario, idChannel, clientSend, sender=None):
        await self.connect()
        if clientSend == "True":
            print(f"INSERT INTO freelanceMessage (mensagem, horarioMensagem, sender, idChannel, clientSend) VALUES ('{message}', '{horario}', '{sender}', {idChannel}, {clientSend});")
            self.cursor.execute(f"INSERT INTO freelanceMessage (mensagem, horarioMensagem, sender, idChannel, clientSend) VALUES ('{message}', '{horario}', '{sender}', {idChannel}, {clientSend});")
        else:
            self.cursor.execute(f"INSERT INTO freelanceMessage (mensagem, horarioMensagem, idChannel, clientSend) VALUES ('{message}', '{horario}', {idChannel}, {clientSend});")
        self.con.commit()

    async def getJobByLink(self, link):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM jobs WHERE link = '{str(link)}';")
        data = self.cursor.fetchall()
        if data != []:
            return data
        return False

    async def updateNotifyJob(self, messageId, job=None):
        await self.connect()
        self.cursor.execute("UPDATE notifyJobs SET messageId = {} WHERE nome='{}' AND link='{}' AND bids={} AND proposal='{}' AND bidTime='{}' AND valor='{}';".format(messageId, self.bind_sqli(job["nome"]), job["link"], job["bids"], self.bind_sqli(job["proposal"]), job["bidTime"], job["valor"]))
        self.con.commit()
    
    async def getNotifyJobByLink(self, link):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM notifyJobs WHERE link = '{str(link)}';")
        result = self.cursor.fetchall()
        if result != []:
            return list(result[0])
        return False

    async def updateUserNotifyJob(self, userId, job=None):
        await self.connect()
        self.cursor.execute("UPDATE notifyJobs SET idUser = {} WHERE nome='{}' AND link='{}' AND bids={} AND proposal='{}' AND bidTime='{}' AND valor='{}';".format(userId, self.bind_sqli(job[0]), job[1], job[2], self.bind_sqli(job[3]), job[4], job[5]))
        self.con.commit()
    
    async def getAllNotifyJobs(self):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM notifyJobs;")
        data = self.cursor.fetchall()
        if data != []:
            return data[0]
        else:
            return False

    async def deleteNotifyJobDate(self, id):
        await self.connect()
        self.cursor.execute(f"DELETE FROM notifyJobs WHERE id = {id};")
        self.con.commit()

    async def getIdNotifyJobs(self, messageId):
        await self.connect()
        self.cursor.execute(f"SELECT id FROM notifyJobs WHERE messageId = {messageId};")
        data = self.cursor.fetchall()
        if data != []:
            return data[0][0]
        else:
            return False
    
    async def getNotifyJobs(self, id):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM notifyJobs WHERE id = {id};")
        return self.cursor.fetchall()[0]
    
    async def insertResponseQuestionary(self, questionaryId, response, stage):
        await self.connect()
        self.cursor.execute(f"INSERT INTO responseQuestionary (questionaryId, response, stage) VALUES ({questionaryId}, '{response}', {stage});")
        self.con.commit()
    
    async def getResponseQuestionary(self, questionaryId):
        await self.connect()
        self.cursor.execute(f"SELECT * FROM responseQuestionary WHERE questionaryId = {questionaryId};")
        return self.cursor.fetchall()
    
    async def deleteResponseQuestionary(self, questionaryId):
        await self.connect()
        self.cursor.execute(f"DELETE FROM responseQuestionary WHERE questionaryId = {questionaryId};")
        self.con.commit()

if __name__ == "__main__":
    starter = Connection()
    #print(asyncio.run(starter.getOfensiva(810894152795553863)))