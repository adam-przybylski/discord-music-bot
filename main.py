import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import json
import random as rand
import messages as m
import commands as c

intents = discord.Intents().all()

bot = commands.Bot(command_prefix="!", intents=intents)

bot.remove_command("help")

load_dotenv()
TOKEN = os.getenv('DC_TOKEN')

last_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

sounds = []

sound_loop_sleep_time = 180

activity_status = "!help"

connection = None

counter = 0


@bot.event
async def on_ready():
    read_config()
    await bot.change_presence(activity=discord.Game(activity_status))


@bot.event
async def on_message(message):
    await m.message_filter(message, bot.user)
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        print('You do not have the correct role for this command.')
    print(error)


@bot.command(name="join", aliases=["j", "J"])
async def join(ctx):
    await c.join_function(ctx)


@bot.command(name="leave", aliases=["l", "L"])
async def leave(ctx):
    await c.leave_function(ctx)


@bot.command(name="play", aliases=["p", "P"])
async def play(ctx, *, arg):
    global last_url
    last_url = arg
    await c.play_function(ctx, arg)


@bot.command(name="pause")
async def pause(ctx):
    await c.pause_function(ctx, bot.voice_clients)


@bot.command(name="resume")
async def resume(ctx):
    await c.resume_function(ctx, bot.voice_clients)


# @bot.command(name="stop")
# async def stop(ctx):
#     await c.stop_command(ctx, bot.voice_clients)


@bot.command(name="replay", aliases=["r", "R"])
async def replay(ctx):
    await c.play_function(ctx, last_url)


@bot.command(name="search")
async def search(ctx, *, arg):
    result = c.search_function(arg)
    await ctx.send(result)


@bot.command(name="queue", aliases=["q", "Q"])
async def queue(ctx, *, arg=None):
    if arg is None:
        await c.show_queue(ctx, bot)
    await c.queue_function(ctx, arg)


@bot.command(name="skip")
async def skip(ctx):
    await c.skip_function(ctx, bot.voice_clients)


@bot.command(name="sound", aliases=["s", "track", "t", "S", "T"])
async def sound(ctx, arg=None):
    if arg is None:
        await c.show_sounds(ctx, sounds, bot)
        return
    voice_client = ctx.guild.voice_client
    await c.play_track('tracks/' + sounds[int(arg)] + ".mp3", voice_client)


# does not work
@bot.command(name='playlist', aliases=["pl"])
async def playlist(ctx, url):
    await c.playlist_function(ctx, url)


@bot.command(name="clear_queue", aliases=["cq"])
async def clear_queue(ctx):
    await c.cls_playlist(ctx)


# does not work
@bot.command(name="play_now")
async def play_now(ctx, *, arg):
    await c.play_now_function(ctx, arg, bot.voice_clients)


@bot.command(name="help", aliases=["h", "H"])
async def help(ctx):
    await c.help_function(ctx, bot)


async def random_clips_in_loop(ctx):
    while True:
        random = rand.choice(sounds)
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await c.play_track('tracks/' + random + ".mp3", voice_client)
        await asyncio.sleep(sound_loop_sleep_time)


@bot.command()
async def start(ctx):
    bot.loop.create_task(random_clips_in_loop(ctx))


@bot.command()
async def stop(ctx):
    bot.loop.cancel()


@bot.command()
async def random_sound(ctx):
    random = rand.choice(sounds)
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await c.play_track('tracks/' + random + ".mp3", voice_client)


def read_config():
    with open("config.json", mode="r", encoding="utf-8") as f:
        config = json.load(f)
        m.answers = config["answers"]
        global sounds
        sounds = config["sounds"]
        c.forbidden = config["forbidden"]
        c.forbidden_mess = config["forbidden_mess"]
        global sound_loop_sleep_time
        sound_loop_sleep_time = config["sound_loop_sleep_time"]
        global activity_status
        activity_status = config["activity_status"]


@bot.command()
async def load(ctx):
    read_config()


bot.run(TOKEN)
