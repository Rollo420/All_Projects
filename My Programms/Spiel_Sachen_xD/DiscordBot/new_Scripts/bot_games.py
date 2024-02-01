import discord
from discord.ext import commands
import random as rdm


TOKEN = "Bot_Token"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def test(ctx):

    title = "HTML Embed with Buttons"
    description = "This is an example of an Embed with HTML buttons."

    # Erstelle einen Button mit dem Label "Click me" und dem Stil "primary"
    button1 = discord.Button(label="Click me", style=discord.ButtonStyle.primary)
    
    embed = discord.Embed(title=title, description=description)
    embed.add_field(name="Buttons", value="", inline=False)

    embed.add_field(name="", value="", inline=True)
    
    await ctx.send(embed=embed)

bot.run(TOKEN)
