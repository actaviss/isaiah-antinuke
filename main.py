import discord
import pymongo
import os
import asyncio
import datetime

from cogs.AntiEvents import AntiEvents
from cogs.EmbedCommands import EmbedCommands
from cogs.Moderation import Moderation
from cogs.ServerCommands import ServerCommands

MONGODB_URL = 'mongodb+srv://actavis:<Josey1173>@isaiah.8meri.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'

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

prefix = os.getenv("prefix")

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')

client.add_cog(AntiEvents(client, db))
client.add_cog(EmbedCommands(client, db))
client.add_cog(Moderation(client, db))
client.add_cog(ServerCommands(client, db))

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

@client.command()
@commands.check(is_whitelisted)
async def whitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user.")
        return

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user.")
        return

    if user.id in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        await ctx.send("That user is already in the whitelist.")
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$push": { "users": user.id }})

    await ctx.send(f"{user} has been added to the whitelist.")

@client.command()
@commands.check(is_whitelisted)
async def dewhitelist(ctx, user: discord.User):
    if not user:
        await ctx.send("You need to provide a user")

    if not isinstance(user, discord.User):
        await ctx.send("Invalid user")

    if user.id not in db.find_one({ "guild_id": ctx.guild.id })["users"]:
        await ctx.send("That user is not in the whitelist.")
        return

    db.update_one({ "guild_id": ctx.guild.id }, { "$pull": { "users": user.id }})

    await ctx.send(f"{user} has been removed from the whitelist.")

@client.command()
@commands.check(is_whitelisted)
async def whitelisted(ctx):
    data = db.find_one({ "guild_id": ctx.guild.id })['users']

    embed = discord.Embed(title=f"Whitelist for {ctx.guild.name}", description="")

    for i in data:
        embed.description += f"{client.get_user(i)} - {i}\n"

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
