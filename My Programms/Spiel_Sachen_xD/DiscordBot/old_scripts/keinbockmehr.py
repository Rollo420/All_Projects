import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

TOKEN = 'MTEyNzg4Mjk4NzE0MTM0MTIyNA.GK05TH.UOWSTmbnWmlx1cYZ38CX8yuA2rIcoKV9QgJhZ0'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

songs_queue = []

@bot.event
async def on_ready():
    print(f'Bot ist bereit. Eingeloggt als {bot.user.name}')

@bot.command()
async def play(ctx, url):
    channel = ctx.message.author.voice.channel
    voice_client = ctx.voice_client

    if voice_client is None:
        voice_client = await channel.connect()
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)

    songs_queue.append(url)

    if not voice_client.is_playing():
        await play_song(ctx)

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        songs_queue.clear()
        await voice_client.disconnect()


@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send('Nächstes Lied wird abgespielt...')
    else:
        await ctx.send('Es wird kein Lied abgespielt.')

@bot.command()
async def queue(ctx):
    if len(songs_queue) > 0:
        queue_list = '\n'.join(songs_queue)
        await ctx.send(f'In der Warteschlange befindet sich bisher:\n{queue_list}')
    else:
        await ctx.send('Die Warteschlange ist leer.')

@bot.command()
async def add(ctx, url):
    songs_queue.append(url)
    await ctx.send(f'Lied hinzugefügt: {url}')

@bot.command()
async def hilfe(ctx):
    await ctx.send(f"- Du kannst folgende Commands verwenden mit dem Prefix ""-"" : \n  \n - play  \n - skip \n - queue \n - add")

async def play_song(ctx):
    voice_client = ctx.voice_client

    if len(songs_queue) > 0:
        url = songs_queue[0]
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        voice_client.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: bot.loop.create_task(song_finished(ctx)))
        await ctx.send(f'Spiele ab: {url}')
        del songs_queue[0]
    else:
        await ctx.send('Die Warteschlange ist leer.')

async def song_finished(ctx):
    if len(songs_queue) > 0:
        await play_song(ctx)
    else:
        voice_client = ctx.voice_client
        await voice_client.disconnect()

bot.run(TOKEN)
