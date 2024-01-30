import os
import random as rdm
import discord
from discord.ext import commands
import asyncio
from bot_BlackJack import BlackJack
from bot_Schere_Stein import schereStein as ss
import comm
from bot_gess_the_num import gess_the_num as gtn
from bot_TicTacToe import TicTacToeBoard

TOKEN = "MTE0MjAxMzY3MTQ2NDI1MTQyNg.GOnGQD.L6s7bsZatl1DC0Aa_TtO9q7cH4WaS6nQ7TkKKg"
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)


# Main function
@bot.command()
async def main(ctx):
    print("test")
    message = await comm.warte_auf_nachricht(bot, ctx)

@bot.command()
async def bj(ctx,bet):
    message = await BlackJack(ctx,bot,bet)

@bot.command()
async def schereStein(ctx):
    message = await ss(ctx,bot)

@bot.command()
async def gess_the_num(ctx):
    message = await gtn(ctx,bot)

@bot.command()
async def tic(ctx, member: discord.Member):
    board = TicTacToeBoard()
    runde = 0

    while True:
        runde +=1
        print(f"\n\ninput: {runde}")
        await board.send_board(ctx, ctx.channel)

        if board.Draw:
            break

        try:
                message = await bot.wait_for('message', timeout=20)   
        except:
            await ctx.channel.send(f'Du hast zu lange überlegt!', delete_after=10)
            await ctx
            break
        
        await ctx.channel.purge(limit=1)

        msg = message.content.split()
        print(msg)
        msg_User_ID = message.author.id

        """if msg_User_ID != bot.user.id and msg_User_ID != board.player_one and msg_User_ID != board.player_two:
                        await ctx.channel.send("Sie sind nicht in das Spiel eingeweit worden!!!", delete_after=5)
        
        else:"""
        await board.game_logic(ctx, member, msg_User_ID, msg)

# Run the bot
asyncio.run(bot.run(TOKEN))
