import os
import random as rdm
import discord
from discord.ext import commands
import asyncio



async def gess_the_num(ctx,bot):
    number =  rdm.randint(0, 100)

    await ctx.send(f'Ich habe mir eine Zahl zwischen 0 und 100 überlegt. Rate mal!')

    while True:
    # Warte auf Benutzereingabe
        try:
            message = await bot.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            await ctx.send('Du hast zu lange gewartet.')
            return

        # Überprüfe die Benutzereingabe
        guess = int(message.content)
        if guess == number:
            await ctx.send(f'Richtig! Die Zahl war: {number}.' )
            break
        elif guess < number:
            await ctx.send(f'Die gesuchte Zahl ist größer. ⇧')
        elif guess > number:
            await ctx.send(f'Die gesuchte Zahl ist kleiner. ⇩')