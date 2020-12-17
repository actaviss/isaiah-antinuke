import discord
from discord.ext import commands
import datetime

class BotCommands(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook


    @commands.guild_only()
    @commands.command(aliases=['nk'])
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            isaiah = channel.position
            await ctx.send(f"now nuking `{ctx.channel.name}`...")
            newchannel = await channel.clone(reason=f"Nuked by {ctx.author}")
            await channel.delete()
            await newchannel.edit(position=isaiah, sync_permissions=True)
            embed = discord.Embed(color=0x2c2f33)
            embed.description = f"`CHANNEL HAS BEEN NUKED BY`: <@{ctx.author.id}>"
            embed.set_image(url="https://media.discordapp.net/attachments/773644221449371698/776654450105253938/image0.gif?width=319&height=180")
            await newchannel.send(embed=embed)
            return

        except:
            pass

    @commands.guild_only()
    @commands.command(aliases=['latency'])
    async def ping(self, ctx):
        await ctx.message.delete()
        pping=discord.Embed(title=f"Bot Ping: `{round(self.client.latency * 1000)}ms`", color=0x36393F)
        await ctx.channel.send(embed=pping)



    @commands.guild_only()
    @commands.command(aliases=["userinfo"])
    async def whois(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author  
        roles = [role for role in member.roles]
        embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at)
        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{member}")
        embed.add_field(name="**ID:**", value=member.id)
        embed.add_field(name="**NickName:**", value=member.display_name)
        embed.add_field(name="**Created On:**", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="**Joined Server On:**", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name="**Roles:**", value="".join([role.mention for role in roles]))
        embed.add_field(name="**Highest Role:**", value=member.top_role.mention)
        roles = [role.mention for role in member.roles[1:]]
        await ctx.send(embed=embed)


    @commands.guild_only()
    @commands.command(aliases=["massunban"])
    @commands.has_permissions(administrator=True)
    async def unbanall(self, ctx):
        guild = ctx.guild
        banlist = await guild.bans()
        await ctx.send('Unbanning `{}` members!'.format(len(banlist)))
        for users in banlist:
                await ctx.guild.unban(user=users.user, reason=f"Responsible User: {ctx.author}")
