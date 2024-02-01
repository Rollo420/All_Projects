import discord
from discord.ext import commands
from discord.ui import View, Button, button
from itertools import combinations
import os

TOKEN = 'Bot_Token'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


class TicTacToeBoard:

    global print_board

    def __init__(self):
        self.board = [[' ']*3 for _ in range(3)]
        self.message = None 
        self.player_one = None
        self.player_two = None
        self.print_board = 0
        self.player_Status = True
        self.sybol = None
        self.set_player = True
        self.Draw = False
        self.player_one_history = []
        self.player_two_history = []
        self.all_player_history = []
        self.winning_combinations = []


    def display_board(self):
        formatted_board = ""
        for row in self.board:
            formatted_board += f" {row[0]} ║ {row[1]} ║ {row[2]} \n"
            if row != self.board[-1]:
                formatted_board += "═══╬═══╬═══\n"

        return formatted_board
    
    async def send_board(self, ctx, channel):
        if not self.message:
            self.message = await channel.send(f"Geben Sie die Koordienaten so 1 1 (für die Mitte) an." +
                                              f"\nPlayer: {ctx.author.mention} beginnt!")  # Erste Nachricht senden
            
        print(f"print_board: {self.print_board}")

        if self.print_board != 0:

            formatted_board = self.display_board()
            await self.message.edit(content=f"```\n{formatted_board}```")  # Nachricht bearbeiten

        self.print_board = 1

    def make_move(self, row, col, symbol):
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            self.board[row][col] = symbol
            return True
        else:
            return False
    
    def generate_winning_combinations(self):
        all_coordinates = [(i, j) for i in range(3) for j in range(3)]
        possible_combinations = list(combinations(all_coordinates, 3))
    
        return possible_combinations
    
    def winner(self, ply_hist):

        #3 x Zeilen
        if ['0', '0'] in ply_hist and ['0', '1'] in ply_hist and ['0', '2'] in ply_hist:
            return True
        elif ['1', '0'] in ply_hist and ['1', '1'] in ply_hist and ['1', '2'] in ply_hist:
            return True
        elif ['2', '0'] in ply_hist and ['2', '1'] in ply_hist and ['2', '2'] in ply_hist:
            return True
        #3 x Spalten
        elif ['0', '0'] in ply_hist and ['1', '0'] in ply_hist and ['2', '0'] in ply_hist:
            return True
        elif ['0', '1'] in ply_hist and ['1', '1'] in ply_hist and ['2', '1'] in ply_hist:
            return True
        elif ['0', '2'] in ply_hist and ['1', '2'] in ply_hist and ['2', '2'] in ply_hist:
        #2 x Diagonalen
            return True
        elif ['0', '0'] in ply_hist and ['1', '1'] in ply_hist and ['2', '2'] in ply_hist:
            return True
        elif ['0', '2'] in ply_hist and ['1', '1'] in ply_hist and ['2', '0'] in ply_hist:
            return True            
        
        return False

        #print(f"Ply One: {self.player_one_history}\nPly Two: {self.player_two_history}")

    async def game_logic(self, ctx, member, msg_User_ID: int, msg):

        if self.set_player == True:
            self.player_one = msg_User_ID
            self.player_two = member.id 
            self.set_player = False

        print(f"msg_User_ID: {msg_User_ID} \nvar player_one: {self.player_one} \nvar player 02: " +
              f"{self.player_two} \nctx author: {ctx.author} \nBot ID: {bot.user.id}")
        
        if not [msg[0], msg[1]] in self.all_player_history: 
            if msg_User_ID == self.player_one:
                if self.player_Status:
                    board.make_move(int(msg[0]), int(msg[1]), "X")

                    self.player_one_history.append([msg[0], msg[1]])
                    self.all_player_history.append([msg[0], msg[1]])

                    if len(self.all_player_history) == 9:
                        await ctx.send("Draw")
                        self.Draw = True

                    elif self.winner(self.player_one_history):
                        await ctx.send(f"Player One hat gewonnen!")
                        
                    self.player_Status = False
                else:
                    await ctx.send("Player Two ist am zug", delete_after=3)
                    
            elif msg_User_ID == self.player_two:
                if self.player_Status == False:
                    board.make_move(int(msg[0]), int(msg[1]), "O")
                
                    self.player_two_history.append([msg[0], msg[1]])
                    self.all_player_history.append([msg[0], msg[1]])

                    if len(self.all_player_history) == 9:
                        await ctx.send("Draw")
                        self.Draw = True

                    elif self.winner(self.player_two_history):
                        await ctx.send("Player Two hat gewonnen!")

                    self.player_Status = True
                else:
                    await ctx.send("Player One ist am zug", delete_after=3)
                
        else:
            await ctx.send(f"{msg[0], msg[1]} ist schon belegt. \nVersuche es nochmal", delete_after=3)
            
board = TicTacToeBoard()

@bot.command()
async def greet(ctx, member: discord.Member):

    if ctx.author == member:
        await ctx.channel.send(f"Hallo {member.mention}!")

@bot.command()
async def tic(ctx, member: discord.Member):
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

        
    
       
bot.run(TOKEN)
