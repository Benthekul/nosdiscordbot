import discord
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = ".")
status = cycle(['My prefix is "."', 'Put on your facemask.', 'Corona time.', 'Mr. Costello is watching you.'])

@client.event
async def on_ready():
    change_status.start()
    print('Bot initiated.')

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.event
async def on_member_join(member):
    channel = client.get_channel(687763780217602156)
    textchannel = client.get_channel(687755657041936454)
    await channel.send(f'{member.mention} has joined the server. Please read the rules and configure your rank in {textchannel.mention}.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')

@client.command()
async def ping(ctx):
    await ctx.send(f'**Pong!** {round(client.latency * 1000)} ms')

@client.command()
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_role(687756468585627718)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@client.command()
@commands.has_role(687756468585627718)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
@commands.has_role(687756468585627718)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify a user to ban.')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify a user to unban.')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify a user to kick.')

client.run('Njg4Nzg5Nzc4OTc1NDI0NTE4.Xm5i0g.wxCoP1BECYUiux4VXL0gz784Dfw')
