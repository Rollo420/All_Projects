import discord
from discord.ext import commands
import asyncio
import subprocess

TOKEN = 'Bot_Token' 
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def run_subprocess(ctx, process_name):
   try:
       process = await asyncio.create_subprocess_exec(
           'python', '.\Testoderso.py',
           stdout=asyncio.subprocess.PIPE,
           stderr=asyncio.subprocess.PIPE
       )

       while True:
           output = await process.stdout.readline()
           if not output:
               break

           output = output.decode().strip()
           await ctx.send(f"{process_name}: {output}")

       await process.wait()

   except Exception as e:
       print(f"{process_name}: Error while executing the script: {e}")
       await ctx.send(f"{process_name}: Error: {e}")
       # Here you can add logging to a file or another logging system

@bot.event
async def on_ready():
    print(f'Bot ist bereit. Eingeloggt als {bot.user.name}')

@bot.command()
async def start_process(ctx, process_name ):
    await asyncio.create_task(run_subprocess( ctx, process_name))

bot.run(TOKEN)
