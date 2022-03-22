import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands
global turn


client = commands.Bot(command_prefix='+')
client.remove_command('help')




@client.event
async def on_ready():
    print("Ready to study!")

@client.command(pass_context=False)
async def help(ctx):
    await ctx.send("Commands:\nStart pomodoro:\t\t+pomodoro <time>\nStop pomodoro\t\t+stop")


@client.command()
async def pomodoro(ctx, args: int):
    global turn
    turn = 0
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        await ctx.send(str(args) + " minute pomodoro timer starting!")
        await asyncio.sleep(args*60)
        player = voice.play(FFmpegPCMAudio('sound.mp3'))
        turn += 1
        await study_break(ctx, voice, args)
    else:
        await ctx.send("Error: User not in voice channel")




@client.command(pass_context=False)
async def study_break(ctx, voice, args):
    global turn
    if turn % 4 == 0:
        await ctx.send("Starting long study break: 15 mins! Counter = " + str(turn))
        await asyncio.sleep(15*60)
        player = voice.play(FFmpegPCMAudio('sponge.mp3'))
        await continuePomodoro(ctx, args, voice)
    else:
        await ctx.send("Starting short study break: 5 mins! Counter = " + str(turn))
        await asyncio.sleep(5*60)
        player = voice.play(FFmpegPCMAudio('sponge.mp3'))
        await continuePomodoro(ctx, args, voice)


async def continuePomodoro(ctx, args, voice):
    global turn
    def check(m):
        return m.content == 'Y'

    await ctx.send("Ready to start next pomodoro? Type 'Y' to begin!")
    await client.wait_for('message', check=check)
    await ctx.send(str(args) + " minute timer starting now!")
    await asyncio.sleep(args*60)
    player = voice.play(FFmpegPCMAudio('sound.mp3'))
    turn += 1
    await study_break(ctx, voice, args)



@client.command(pass_context=True)
async def stop(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send('pomodoro over, counter reset to 0')
    else:
        await ctx.send('Error: Pomodoro is not running')



client.run('token')
