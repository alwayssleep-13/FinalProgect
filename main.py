import discord
import typing

from discord import FFmpegPCMAudio

from my_classes.counter import CounterBot, Counter
from my_classes.connect_to_youtube import *
from discord.ext import commands

config = {
    'token': 'MTEwMDgzOTM2MTM3MDY2MDkxNA.GGaEZq.wiehupRgGtfwZR1S2L345YMTszU9nIUqJbQ-RM',
    'prefix': '=',
}

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or(config['prefix']), intents=intents)
sec_bot = CounterBot()



@sec_bot.command()
async def counter(ctx: commands.Context):
    """Starts a counter for pressing."""
    await ctx.send('Press!', view=Counter())


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='Eliot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send(f'Yes, Eliot is cool.')


@bot.command()
async def my_id(ctx):
    await ctx.send(ctx.author.id)


@bot.command()
async def guild_id(ctx):
    await ctx.send(ctx.guild.id)


@bot.command(name="join")
async def join(ctx):
    global voice
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    voice = await channel.connect()


@bot.command(name="leave")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command(pass_context=True)
async def play(ctx, url):
    voice.play(FFmpegPCMAudio(url))
    # try:
    #     server = ctx.message.guild
    #     voice_channel = server.voice_client
    #
    #     async with ctx.typing():
    #         filename = await YTDLSource.from_url(url, loop=bot.loop)
    #         voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg-6.0-essentials_build/bin/ffmpeg.exe", source=filename))
    #     await ctx.send(f'**Now playing:** {filename}')
    # except:
    #     await ctx.send("The bot is not connected to a voice channel.")


@bot.command(name="stop")
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


# @bot.command(pass_context=True)
# async def stop(ctx):
#     voice.stop()


bot.run(config["token"])
# sec_bot.run(config['token'])
