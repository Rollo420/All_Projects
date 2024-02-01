from typing import Optional
import discord
from discord.ext import commands
from discord.ui import View, Button, button

TOKEN = 'Bot_Token'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


class ColorButtons(View):
    def __init__(self):
        super().__init__()
        self.selected_color = None

    @button(label="Red", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "Red"
        await interaction.response.send_message(f"You selected the color: {self.selected_color}", ephemeral=True)

    @button(label="Green", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "Green"
        await interaction.response.send_message(f"You selected the color: {self.selected_color}", ephemeral=True)

    @button(label="Blue", style=discord.ButtonStyle.primary)
    async def blue_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "Blue"
        await interaction.message.send_message(f"You selected the color: {self.selected_color}", ephemeral=True)
    
    @button(label="Funktion", style=discord.ButtonStyle.secondary)
    async def funk_button(self, interaction: discord.Interaction, button: Button):
        self.selected_color = "noch was testen"
        await interaction.response.send_message(f"You selected the color: {self.selected_color}", ephemeral=False)


class GameField(View):
    def __init__(self):
        super().__init__()
        self.object_x = 0
    
    def get_embed(self):
        embed = discord.Embed(title="Game Field", color=discord.Color.green())
        print(self.object_x)

        embed.remove_field(index=0)
        
        embed.add_field(name="Object", value=f"x: {self.object_x}")
        
        return embed
    
    @button(label="Green", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction, button: Button):
        self.object_x += 1
        await interaction.response.edit_message(content=f"Object position: {self.object_x}", view=self)
        self.get_embed()


@bot.event
async def on_ready():
    print("Bot online!")


@bot.command()
async def btn(ctx: commands.Context):
    view = ColorButtons()
    await ctx.send("Choose a color:", view=view)

@bot.command()
async def btn01(ctx):
    btntest = GameField()
    await ctx.send("Click button", view=btntest)

@bot.command()
async def btn02(ctx: commands.Context):
    view = GameField()
    await ctx.send(embed=view.get_embed(), view=view)



bot.run(TOKEN)
