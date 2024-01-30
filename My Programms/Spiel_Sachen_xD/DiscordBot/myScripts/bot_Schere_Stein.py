import os
import random as rdm
import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View

global botHandName
global playerHandName

def cls():
    os.system('cls')
        
async def numBOTName(botWahl):
    
    if botWahl == 5:
        botHandName = 'Spock'
    
    elif botWahl == 4:
        botHandName = 'Echse'
        
    elif botWahl == 3:
        botHandName = 'Papier'
        
    elif botWahl == 2:
        botHandName = 'Stein'
    
    elif botWahl == 1:
        botHandName = 'Schere'
        
    return botHandName

async def numPLAYERName(action):
    
    if action == '5':
        playerHandName = 'Spock'
    
    elif action == '4':
        playerHandName = 'Echse'
        
    elif action == '3':
        playerHandName = 'Papier'
        
    elif action == '2':
        playerHandName = 'Stein'
    
    elif action == '1':
        playerHandName = 'Schere'
        
    return playerHandName
        
async def Schere(ctx, botWahl, action):
    
    if botWahl == 4 or botWahl == 3:
        await Win(ctx, botWahl, action)
    elif botWahl == 2 or botWahl == 5:
        await Lose(ctx, botWahl, action)
    elif action == botWahl:
        await Equal(ctx, botWahl, action)
         
async def Stein(ctx, botWahl, action):
    
    if botWahl == 1 or botWahl == 4:
        await Win(ctx, botWahl, action)
    elif botWahl == 3 or botWahl == 5:
        await Lose(ctx, botWahl, action)
    else:
        await Equal(ctx, botWahl, action)

async def Papier(ctx, botWahl, action):
    
    if botWahl == 2 or botWahl == 5:
        await Win(ctx, botWahl, action)
    elif botWahl == 1 or botWahl == 4:
        await Lose(ctx, botWahl, action)    
    else:
        await Equal(ctx, botWahl, action)
        
async def Echse(ctx, botWahl, action):

    if botWahl == 5 or botWahl == 3:
        await Win(ctx, botWahl, action)
    elif botWahl == 1 or botWahl == 2:
        await Lose(ctx, botWahl, action)            
    else:
        await Equal(ctx, botWahl, action)
        
async def Spock(ctx, botWahl, action):

    if botWahl == 1 or botWahl == 2:
        await Win(ctx, botWahl, action)
    elif botWahl == 3 or botWahl == 4:
        await Lose(ctx, botWahl, action)    
    else:
        await Equal(ctx, botWahl, action) 
    
async def Win(ctx, botWahl, action):
        botHandName = await numBOTName(botWahl)
        playerHandName = await numPLAYERName(action)
        
        await ctx.send(f'{ctx.author} gewinnt mit {playerHandName} gegen {botHandName}')

async def Lose(ctx, botWahl, action):
        botHandName = await numBOTName(botWahl)
        playerHandName = await numPLAYERName(action)
        
        await ctx.send(f'{ctx.author} verliert mit {playerHandName} gegen {botHandName}')

async def Equal(ctx, botWahl, action):
        botHandName = await numBOTName(botWahl)
        playerHandName = await numPLAYERName(action)
        
        await ctx.send(f'{ctx.author} spielt mit {playerHandName} gegen {botHandName}. Unentschieden!')
        

async def schereStein(ctx,bot):
    
    #Var
    botWahl = rdm.randint(1, 5)
    
    spielregeln = (
        "\n Willkommen zu Schere, Stein, Papier, Echse, Spock. "
        "\n Die Spielregeln lauten: "
        "\n Schere schneidet Papier, Papier bedeckt Stein, "
        "\n Stein zerquetscht Echse, Echse vergiftet Spock, "
        "\n Spock zertrümmert Schere, Schere köpft Echse, "
        "\n Echse frisst Papier, Papier widerlegt Spock, "
        "\n Spock verdampft Stein und Stein bricht Schere."
    )
    auswahl = "-------------------------- \n Wähle aus: \n <1> Schere \n <2> Stein \n <3> Papier \n <4> Echse \n <5> Spock \n"
    
    print(f'Botwahl ist: {botWahl}')
    
    await ctx.send(f'{spielregeln} \n {auswahl}')
    
    try:
        spielerEingabe = await bot.wait_for('message', timeout=30)#
        #print(spielerEingabe)
    except:
        await ctx.send(f'Du hast zu lange überlegt!')
        return
    
    action = spielerEingabe.content.lower()
    
    if action == '1':
        await Schere(ctx, botWahl,action)
    
    elif action == '2':
        await Stein(ctx, botWahl, action)
    
    elif action == '3':
        await Papier(ctx, botWahl, action)    
    
    elif action == '4':
        await Echse(ctx, botWahl, action)    
    
    elif action == '5':
        await Spock(ctx, botWahl, action)
        
