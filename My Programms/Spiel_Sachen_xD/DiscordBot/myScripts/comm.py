import os
import random as rdm
import discord
from discord.ext import commands
import asyncio


async def warte_auf_nachricht(bot, ctx):
    try:
        message = await bot.wait_for('message', timeout=30)

        if message.content == 'hit':
            await ctx.send("Sie haben hit geschrieben")
        else:
            await ctx.send(f"Sie haben {message.content} geschrieben")
        return message
    except:
        await ctx.send(f'Du hast zu lange überlegt!')
        return 