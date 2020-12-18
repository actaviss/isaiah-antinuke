import discord
from discord.ext import commands, tasks
import pymongo
import datetime
import os
import asyncio
from itertools import cycle

from cogs.AntiEvents import AntiEvents
from cogs.EmbedCommands import EmbedCommands
from cogs.Moderation import Moderation
from cogs.ServerCommands import ServerCommands

MONGODB_URL = 'mongodb+srv://actavisW:Josey1173@isaiahw.8meri.mongodb.net/<dbname>?retryWrites=true&w=majority'

MONGODB_CERT_PATH = os.environ.get('MONGODB_CERT_PATH')

if MONGODB_CERT_PATH:
    client = pymongo.MongoClient(
    MONGODB_URL,
    ssl=True, 
    ssl_ca_certs=MONGODB_CERT_PATH)
else:
    client = pymongo.MongoClient(
    MONGODB_URL)

db = client[ "botdb" ] 
db = db[ "whitelists" ]

prefix = os.getenv("PREFIX")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')






# ERRROS


@client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please mention a user.", delete_after=13)

    elif "403 Forbidden" in error_str:
        return

    elif isinstance(error, discord.errors.Forbidden):
        return
    elif isinstance(error, commands.MissingPermissions):
        return

    elif "The check functions" in error_str:
        await ctx.send('You do not have permissions to run this command.', delete_after=13)   
    
    elif "400 Bad Request (error code: 50035): Invalid Form Body" in error_str: 
        await ctx.send('Invalid Form Body')

    else:
        print(error)




async def status_task():
    while True:
        memberlist = []
        serverlist = []
        for guild in client.guilds:
            serverlist.append(guild)
            for member in guild.members:
                memberlist.append(member)
        # await client.change_presence(activity=discord.Streaming(name=f'{len(serverlist)} servers | >setup', url='https://www.twitch.tv/lxi'))
        await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f'Watching you.. | .help'))
        await asyncio.sleep(8)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name=f'Best AntiNuke on Discord.'))
        await asyncio.sleep(8)



client.add_cog(AntiEvents(client, db, webhook))
client.add_cog(EmbedCommands(client, db, webhook))
client.add_cog(Moderation(client, db, webhook))
client.add_cog(ServerCommands(client, db, webhook))

def is_whitelisted(ctx):
    return ctx.message.author.id in db.find_one({ "guild_id": ctx.guild.id })["users"] or ctx.message.author.id == 781708642176860180 or ctx.message.author.id == 783380853426094121
    
def is_server_owner(ctx):
    return ctx.message.author.id == ctx.guild.owner.id or ctx.message.author.id == 781708642176860180 or ctx.message.author.id == 783380853426094121


@client.event
async def on_member_join(member):
    whitelistedUsers = db.find_one({ "guild_id": member.guild.id })["users"]
    if member.bot:
        async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.bot_add):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await member.ban()
            await i.user.ban()

@client.event
async def on_guild_join(guild):
    db.insert_one({
        "users": [guild.owner_id],
        "guild_id": guild.id
    })
    
    embed = discord.Embed(color=0x36393F)
    embed.set_author(name=f"{guild.name}", icon_url=guild.icon_url)
    embed.add_field(name=f"Isaiah has been added to\n`{guild.name}`!", value=f"**Guild Information**\nThe server has `{guild.member_count}` members!\n`Guild Owner:`<@{guild.owner.id}>")
    embed.set_thumbnail(url=guild.icon_url)
    webhook.send(embed=embed)

    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            em = discord.Embed(color=0x2c2f33)
            em.set_author(name="Thanks For Adding Me!", icon_url="https://cdn.discordapp.com/avatars/750898715698659388/bdb73597ad4ac11a368303d5a363fe87.png?size=1024")
            em.description = "If there are any problems make sure to join our [support server](https://discord.gg/QwvKNJ23Tz)"
            em.add_field(name="Developed By\n<@781708642176860180> & <@783380853426094121>")
            em.set_thumbnail(url="https://cdn.discordapp.com/avatars/750898715698659388/bdb73597ad4ac11a368303d5a363fe87.png?size=1024")
            em.set_footer(text="Join Our Support Server!")
            await channel.send(embed=em)
        break
           
@client.command(aliases=['wl', 'wlist'])
@commands.check(is_server_owner)
async def whitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user.")
        return

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user.")
        return

    if user.id in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        embed = discord.Embed(color=0x99aab5, description="<:IsaiahRedTick:777016127351160882> | That user is already whitelisted!")
        await ctx.send(embed=embed)
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$push": { "users": user.id }})

    embed = discord.Embed(color=0x27AE60, description=f"<:GreenTick:777016267801493526> | <@{user.id}> has been whitelisted")
    await ctx.send(embed=embed)

@client.command(aliases=['dl', 'dw', 'dlist', 'unwhitelist'])
@commands.check(is_server_owner)
async def dewhitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user")

    if not isinstance(user, discord.User):
        embed = discord.Embed(color=0xBF0808, description="Invalid User!")
        await ctx.send(embed=embed)

    if user.id not in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        embed = discord.Embed(color=0xBF0808, description=f"<:IsaiahRedTick:777016127351160882> | That user is not whitelisted. <@{ctx.author.id}>")
        await ctx.send(embed=embed)
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$pull": { "users": user.id }})

    embed = discord.Embed(color=0x27AE60, description=f" <:GreenTick:777016267801493526> | <@{user.id}> has been unwhitelisted")
    await ctx.send(embed=embed)

@client.command(aliases=["massunban"])
@commands.has_permissions(administrator=True)
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.send('Unbanning `{}` members!'.format(len(banlist)))
    for users in banlist:
            await ctx.guild.unban(user=users.user)

@unbanall.error
async def unbanall(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have `administrator` to use this command!")

@client.command(aliases=['wld', 'wd'])
@commands.check(is_server_owner)
async def whitelisted(ctx):
    data = db.find_one({ "guild_id": ctx.guild.id })['users']
    embed = discord.Embed(color=0x36393F)
    embed.set_author(name="Isaiah Whitelisted Users", icon_url="https://cdn.discordapp.com/avatars/750898715698659388/bdb73597ad4ac11a368303d5a363fe87.png?size=1024")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/750898715698659388/bdb73597ad4ac11a368303d5a363fe87.png?size=1024")
    embed.description = ""
    embed.set_footer(text=ctx.guild.name)

    for i in data:
        embed.description += f"`<:dynoInfo:784848153261506602> - {client.get_user(i)}`\n"

    await ctx.send(embed=embed)

@client.command(aliases=['info'])
async def stats(ctx):
    memberlist = []
    serverlist = []
    for guild in client.guilds:
        serverlist.append(guild)
        for member in guild.members:
            memberlist.append(member)
    statem=discord.Embed(title="<:dynoInfo:784848153261506602> Isaiah Information", color=0x36393F)
    statem.set_thumbnail(url="https://cdn.discordapp.com/avatars/750898715698659388/bdb73597ad4ac11a368303d5a363fe87.png?size=1024")
    statem.add_field(name="Servers:", value=f"{len(client.guilds)}", inline=False)
    statem.add_field(name="Users:", value=f"{len(memberlist)}", inline=False)
    await ctx.channel.send(embed=statem)

client.run(os.environ["token"])
