import youtube_dl
import discord
import validators
from youtube_search import YoutubeSearch

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "128"
    }]
}

ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
               'options': '-vn'}

forbidden = []

forbidden_mess = ""

queues = {}

queue_titles = {}


async def join_function(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel")
    else:
        await ctx.message.author.voice.channel.connect()


async def leave_function(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel")
    else:
        await ctx.guild.voice_client.disconnect()


async def create_source(URL):
    source = await discord.FFmpegOpusAudio.from_probe(URL, **ffmpeg_opts)
    return source


async def create_url(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        title = info.get("title", None)
        return URL, title


async def play_function(ctx, arg):
    voice_client = None
    if ctx.guild.voice_client:
        voice_client = ctx.guild.voice_client
    else:
        voice_client = await join_function(ctx)
        if voice_client is None:
            return

    if not validators.url(arg):
        arg = search_function(arg)

    URL, title = await create_url(arg)

    is_valid, position = check_string(title)
    if not is_valid:
        await ctx.send(forbidden[position] + forbidden_mess)
        return

    source = await create_source(URL)

    if voice_client.is_playing():
        await queue_function(ctx, arg)
        return

    await ctx.send(f'Now playing {title} - {arg}, requested by {ctx.author.mention}')
    voice_client.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))


async def pause_function(ctx, voice_clients):
    voice_client = discord.utils.get(voice_clients, guild=ctx.guild)
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send('There is no audio playing at the moment')


async def resume_function(ctx, voice_clients):
    voice_client = discord.utils.get(voice_clients, guild=ctx.guild)
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send('There is no audio paused at the moment')


async def stop_function(ctx, voice_clients):
    voice_client = discord.utils.get(voice_clients, guild=ctx.guild)
    voice_client.stop()


def search_function(arg):
    results = YoutubeSearch(arg, max_results=5).to_dict()
    # print(results[0]['title'])
    # msg = await bot.wait_for("message")
    return 'https://www.youtube.com' + results[0]['url_suffix']


def check_if_empty(ctx):
    if not queues[ctx.message.guild.id]:
        return True


async def queue_function(ctx, arg, is_source_url=False, title=None):
    if not is_source_url:
        if not validators.url(arg):
            arg = search_function(arg)
        arg, title = await create_url(arg)

    is_valid, position = check_string(title)
    if not is_valid:
        await ctx.send(forbidden[position] + forbidden_mess)
        return

    source = await create_source(arg)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)
        queue_titles[guild_id].append(title)
    else:
        queues[guild_id] = [source]
        queue_titles[guild_id] = [title]
    if title is not None:
        await ctx.send(
            f'Queued {title}, requested by {ctx.author.mention}. Position in queue: #{len(queues[guild_id])}')


def check_queue(ctx, guild_id):
    voice_client = ctx.guild.voice_client
    if not voice_client.is_playing():
        if queues[guild_id]:
            source = queues[guild_id].pop(0)
            title = queue_titles[guild_id].pop(0)
            # await ctx.send(f'Now playing "{title}" - {url}')
            voice_client.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))


async def play_track(url, voice_client):
    source = discord.FFmpegPCMAudio(url)
    voice_client.play(source)


async def skip_function(ctx, voice_clients):
    await stop_function(ctx, voice_clients)
    if check_if_empty(ctx):
        await ctx.send('Queue is empty')
        return
    await ctx.send("Skipped")
    check_queue(ctx, ctx.message.guild.id)


async def cls_playlist(ctx):
    global queues
    queues[ctx.message.guild.id] = []
    queue_titles[ctx.message.guild.id] = []
    await ctx.send('Cleared queue')


def check_string(str):
    str = str.lower()
    for i in range(len(forbidden)):
        if str.find(forbidden[i]) != -1:
            return False, i
    return True, -1


async def help_function(ctx, bot):
    help_embed = discord.Embed(title="Help Desk for Zgredek Bot", description="All commands for the bot.",
                               color=discord.Color.green())

    help_embed.set_author(name="Zgredek Bot", icon_url=bot.user.avatar)

    help_embed.add_field(name="!join, aliases: !j", value="Joins voice channel", inline=False)
    help_embed.add_field(name="!leave, aliases: !l", value="Leaves voice channel", inline=False)
    help_embed.add_field(name="!play <phrase or url>, aliases: !p", value="Plays audio from url or phrase ",
                         inline=False)
    help_embed.add_field(name="!pause", value="Pauses audio", inline=False)
    help_embed.add_field(name="!resume", value="Resumes audio", inline=False)
    help_embed.add_field(name="!replay, aliases: !r", value="Replays audio", inline=False)
    help_embed.add_field(name="!search <phrase>", value="Searches audio and returns url", inline=False)
    help_embed.add_field(name="!queue <phrase or url>, aliases: !q",
                         value="Adds audio to queue. With empty parameter shows queue.", inline=False)
    help_embed.add_field(name="!skip", value="Skips current playing audio", inline=False)
    help_embed.add_field(name="!clear_queue, aliases: !cq", value="Clears queue", inline=False)
    help_embed.add_field(name="!stop", value="Stops audio", inline=False)
    help_embed.add_field(name="!start", value="Starts random sound loop", inline=False)
    help_embed.add_field(name="!stop", value="Stops random sound loop", inline=False)
    help_embed.add_field(name="!sound <number>, aliases: !s, !track, !t",
                         value="Play available sounds. With empty parameter shows sound list",
                         inline=False)
    help_embed.set_footer(text=f'Requested by <@{ctx.author}>', icon_url=ctx.author.avatar)

    await ctx.send(embed=help_embed)


async def show_sounds(ctx, sounds, bot):
    help_embed = discord.Embed(title="Sounds list for Zgredek Bot",
                               description="All sounds that bot can play.",
                               color=discord.Color.blue())
    help_embed.set_author(name="Zgredek Bot", icon_url=bot.user.avatar)
    for i in range(len(sounds)):
        help_embed.add_field(name="!s " + str(i), value=sounds[i], inline=True)

    help_embed.set_footer(text=f'Requested by <@{ctx.author}>', icon_url=ctx.author.avatar)

    await ctx.send(embed=help_embed)

    if len(sounds) > 25:
        help_embed2 = discord.Embed(title="Sounds list continued", description="All sounds that bot can play.",
                                    color=discord.Color.blue())
        help_embed2.set_author(name="Zgredek Bot", icon_url=bot.user.avatar)
        for i in range(25, len(sounds)):
            help_embed2.add_field(name="!s " + str(i), value=sounds[i], inline=True)

        help_embed2.set_footer(text=f'Requested by <@{ctx.author}>', icon_url=ctx.author.avatar)

        await ctx.send(embed=help_embed2)


async def show_queue(ctx, bot):
    help_embed = discord.Embed(title="Queue", description="All tracks in queue",
                               color=discord.Color.blue())
    help_embed.set_author(name="Zgredek Bot", icon_url=bot.user.avatar)

    for i in range(len(queue_titles[ctx.message.guild.id])):
        help_embed.add_field(name="#" + str(i + 1), value=queue_titles[ctx.message.guild.id][i], inline=False)

    help_embed.set_footer(text=f'Requested by <@{ctx.author}>', icon_url=ctx.author.avatar)

    await ctx.send(embed=help_embed)
