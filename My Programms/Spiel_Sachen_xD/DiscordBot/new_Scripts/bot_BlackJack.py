import os
import random as rdm
import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def BlackJack(ctx, bet):
    print(f'Blakjack from {ctx.author}')
 

    if int(bet) > 1000:
        print(f'{ctx.author} hat ein zuhohen Wetteinsatz angegeben von: {bet}')
        await ctx.send(f'{ctx.author} hat ein zuhohen Wetteinsatz angegeben')
        return
    else:

        konto = 1000
        konto = konto - int(bet)

        await ctx.send(f'Wilkommen bei Black Jack ihr Kontostand liegt bei {konto}')
        
        dealerHand = rdm.randint(2, 11)
        playerHand = rdm.randint(2, 11)

        while True:

            await ctx.send(f"\tDealer:\n\t{dealerHand}\n\n{ctx.author}:\n\t{playerHand}\n\n- Schreibe:\n ""-"" Hit um noch eine Karte zu bekommen\n ""-"" Stand um zu Passen\n ""-"" Dopple um noch eine karte zu bekommen und dein einsatz zu verdopplen")

            try:
                message = await bot.wait_for('message', timeout=30)
            except:
                await ctx.send(f'Du hast zu lange überlegt!')
                return


            action = message.content

        
            if action == 'exit':
                print(f"{ctx.author} Exit")
                await ctx.send(f'Schüss {ctx.author}')
                break

            elif action == 'hit':
                print(f"{ctx.author} Hit")

                playerHand = playerHand + rdm.randint(2, 11)

                if playerHand > 21:
                    print(f'{ctx.author} hat das Spiel verloren')

                    await ctx.send(f"\tDealer:\n\t{dealerHand}\n\n{ctx.author}:\n\t{playerHand}\n\n- Schreibe:\n ""-"" Hit um noch eine Karte zu bekommen\n ""-"" Stand um zu Passen\n ""-"" Dopple um noch eine karte zu bekommen und dein einsatz zu verdopplen")
                    print(f'{ctx.author} hat das Spiel verloren')
                    await ctx.send(f'{ctx.author} hat das Spiel verloren')
                    return
                elif playerHand == 21:
                    print(f'{ctx.author} hat mit 21 Punkten gewonnen')

            elif action == 'Stand':

                while True:

                    if dealerHand <= 17:                        
                        print(f'Dealer hat {dealerHand} Punkte')
                        dealerHand = dealerHand + rdm.randint(2,11)

                    else:
                        print(f'Dealer hat mehr als 17 Punkte')

                        if dealerHand > playerHand:
                            print(f'Dealer hat mit {dealerHand} mehr Punkte als Player({ctx.author} mit {playerHand})')

                            await ctx.send(f'\tDealer:\n\t{dealerHand}\n\n{ctx.author}:\n\t{playerHand}\n\nDer Dealer hat mit {dealerHand} Punkten gewonnen')
                            return
                        else:
                            print(f'{ctx.author} hat mit {playerHand} Punkten gegen Dealer mit {dealerHand} Punkten gewonnen.')

                            await ctx.send(f'\tDealer:\n\t{dealerHand}\n\n{ctx.author}:\n\t{playerHand}\n\n{ctx.author} hat das Spiel mit {playerHand} Punkten gewonnen.')
                            return
                        

