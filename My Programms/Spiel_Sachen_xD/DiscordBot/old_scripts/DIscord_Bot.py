import discord
from discord.ext import commands
import asyncio

TOKEN = 'Bot_Token'
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
TARGET_USER_ID = 538367233739587611
i = 0




@client.event
async def on_ready():
    print("Bot online!")

@client.command()
async def löwi_sad(ctx):

    #gif datei auslesen und senden 

    print("test1")
    user=  await client.fetch_user(TARGET_USER_ID)
    print("test2")
    await user.send('👀')
    print("test3")

@client.command()
async def baum(ctx,*,zahl):
   # while(i < int(zahl)):
        print(zahl)
        print("test4")
        user=  await client.fetch_user(TARGET_USER_ID)
        print("test5")
        await user.send_friend_request()
        await user.send('hallo')
        print("test6")
        i +1    

client.run(TOKEN)
