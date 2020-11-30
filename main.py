# bot.py
import os
import Broker as BR
import discord

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = 'NzQ4Mjc5NjU1MTc3NTE5MjA2.X0bHvA.unYGeGcLidO0MlZXR_YdMnIuMGQ'
print(TOKEN)
client = discord.Client()
BRService = None
BRServiceList = []

@client.event
async def on_ready():
  global BRService
  BRService = BR.Broker(userName = 'natan132', password = 'Gottachangethisagain1!')
  # BRService = BR.Broker(userName = 'tug58366@temple.edu', password = 'Ethiopian44')
  BRServiceList.append(BRService)
  response = BRService.login()
  print('\n', response, '\n')
  print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    global BRService

    if message.author == client.user:
        return

    #split message into command and data
    messageList = message.content.split(' ')

    #if the command is add Account create a new thread that will handle a single acc
    if messageList[0] == 'login':
      BRService = BR.Broker(userName = messageList[1], password = messageList[2])
      response = BRService.login()
      await message.channel.send(str(response))
    elif messageList[0] == 'logout':
      response = BRService.logout()
      await message.channel.send(str(response))
    elif messageList[0] == '.buy':
      response = BRService.buyOption(messageList)
      await message.channel.send(str(response))
    elif messageList[0] == '.sell':
      response = BRService.sellOption(messageList[1])
      await message.channel.send(str(response))
    elif messageList[0] == 'buyStock':
      response = BRService.buyStock(messageList)
      await message.channel.send(str(response))
    elif messageList[0] == 'sellStock':
      response = BRService.sellStock(messageList)
      await message.channel.send(str(response))
    elif messageList[0] == '.options':
      response = BRService.getAllOptionOrders()
      await message.channel.send(str(response))
    elif messageList[0] == 'stocks':
      response = BRService.getAllStockOrders()
      await message.channel.send(str(response))
    elif messageList[0] == 'help':
      response = BRService.help()
      await message.channel.send(str(response))
    elif messageList[0] == 'test':
      response = BRService.getDayTradeLimit()
      await message.channel.send(str(response))
    else:
      raise discord.DiscordException

    # getOpenOptionOrders
# getBuyingPower
client.run(TOKEN)