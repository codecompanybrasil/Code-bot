import asyncio
import os
from dotenv import load_dotenv
import discord
from conn_db import Connection
from utils import Utils

class Verifications:
    def __init__(self, pessoa=False):
        self.pessoa = pessoa
        self.connector = Connection()
        self.last_bumped = None
        self.utils = Utils(pessoa=self.pessoa)
        load_dotenv()

    # async def bumpVerification(self, message):
    #     if message.channel.id == int(os.environ["BUMP_CHANNEL"]):
    #         print("=-"*20 + "\n")
    #         print("V1")
    #         print(str(message.content))
    #         print(message.type)
    #         print(message.author)
    #         print(message.raw_mentions)
    #         if "/bump" in str(message.content):
    #             self.last_bumped = message.author
    #             print("Peguei o autor")
    #         if message.embeds != []:
    #             print("V2")
    #             if message.author.id == int(os.environ["DISBOARD_ID"]):
    #                 print("V3")
    #                 embed = message.embeds[0]
    #                 if "Bump done" in str(embed.description):
    #                     print("V4")
    #                     await self.utils.setPoint(10, self.last_bumped.id)
    #                     await self.utils.pointMessage(self.last_bumped.id, 10, "Fez um Bump no servidor!")
    
    # async def diaryMessageVerification(self, message):
    #     if not await self.connector.getDiaryMessage(message.author.id):
    #         await self.connector.addOfensiva(message.author.id)
    #         ofensiva = int(await self.connector.getOfensiva(message.author.id))
    #         await self.connector.setDiaryMessage(message.author.id)
    #         if ofensiva == 1:
    #             pontos = 5
    #             await self.utils.setPoint(pontos, message.author.id)
    #             await self.utils.pointMessage(message.author.id, pontos, f"Parabéns! Está iniciando a sua 🔥 ofensiva!\nEnvie mensagens todo o dia para ganhar mais pontos! \nParticipe regularmente! 🎉")
    #         elif ofensiva % 5 == 0:
    #             pontos = ofensiva
    #             await self.utils.setPoint(pontos, message.author.id)
    #             await self.utils.pointMessage(message.author.id, pontos, f"Parabéns! Completou seu {ofensiva}º dia de 🔥 ofensiva!\n Daqui 5 ofensivas, você ganhará 5 pontos como bônus  🎉")
    
    async def boostMessageVerification(self, message):
        if message.type == discord.MessageType.premium_guild_subscription:
            if message.raw_mentions != []:
                guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
                channel = guild.get_channel(int(os.environ["RESPOSTAS_CARGO_CHANNEL"]))
                await channel.send(f"Recebi boost, começando processo de dar os bucks! (teve message.raw_mentions na mensagem)")
                
                idUser = int(message.raw_mentions[0])
                member = self.pessoa.get_user(idUser)
                await self.utils.setPoint(50, idUser)
                await self.utils.pointMessage(idUser, 50, "Você deu um Boost na comunidade! Obrigado pelo voto de confiança!")
            else:
                guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
                channel = guild.get_channel(int(os.environ["RESPOSTAS_CARGO_CHANNEL"]))
                await channel.send(f"Recebi um Boost de alguem, mas a mensagem não teve menção de ninguem!")
    
    # async def onEmojiReact(self, emoji, server, cargosId, userId=None):
    #     self.guild = self.pessoa.get_guild(int(os.environ["CODE_COMPANY_ID"]))
    #     if userId:
    #         member = self.guild.get_member(int(userId))
    #     for cargo in cargosId:
    #         if emoji == cargo:
    #             if cargosId[cargo] == True:
    #                 return True
                
    #             elif type(cargosId[cargo]) == list:
    #                 cargoServer = server.get_role(int(cargosId[cargo][0]))
    #                 if await self.timeMemberReactionPermitionVerification(str(member.joined_at)):
    #                     await self.utils.mensagemIniciacaoLinguagem(self.pessoa.get_user(int(userId)), cargosId[cargo][1], int(cargosId[cargo][0]))
    #                 return cargoServer
    #             else:
    #                 cargoServer = server.get_role(int(cargosId[cargo]))
    #                 return cargoServer
    #     return None

    # async def timeMemberReactionPermitionVerification(self, time):
    #     #member.created_at
    #     time = str(time).split(" ")[0]
    #     time = str(time).split("-")
    #     d1 = f"{time[2]}/{time[1]}/{time[0]}"
    #     diferenca = await self.utils.diferenca_dias(d1)
    #     if int(diferenca) > 1:
    #         return False
    #     else:
    #         return True

if __name__ == "__main__":
    starter = Verifications()
    print(asyncio.run(starter.timeMemberVerification("2022-08-12")))
        
        
        
             
        