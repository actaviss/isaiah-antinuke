import discord
from discord.ext import commands
import datetime
import asyncio

def bot_owner(ctx):
    return ctx.message.author.id == 783380853426094121 or 781708642176860180

class ServerCommands(commands.Cog):
    def __init__(self, client, db):
        self.client = client
        self.db = db

    @commands.command(aliases=['av', 'pfp'])
    async def avatar(self, ctx, txt: str = None):
        if txt:
            try:
                user = ctx.message.mentions[0]
            except IndexError:
                user = ctx.guild.get_member_named(txt)
            if not user:
                user = ctx.guild.get_member(int(txt))
            if not user:
                user = ctx.guild.get_user(int(txt))
            if not user:
                await ctx.send('Could not find user.')
                return
        else:
            user = ctx.message.author

        try:
            avi = user.avatar_url.rsplit("?", 1)[0]
        except Exception:
            avi = user.avatar_url_as(static_format='png')
        try:
            em = discord.Embed(colour=0x2c2f33)
            em.set_author(name=f"{user.name}#{user.discriminator}", icon_url=avi)
            em.set_image(url=avi)
            await ctx.send(embed=em)
        except Exception:
            await ctx.send(avi)

    @commands.command(aliases=['mc', 'mcount', 'members'])
    async def membercount(self, ctx):
        membercount = str(ctx.guild.member_count)
        embed = discord.Embed(title="Members", color=0x76D7C4, timestamp=ctx.message.created_at)
        embed.description =membercount
        await ctx.send(embed=embed)

    @commands.command(aliases=['icon', 'serverpfp', 'servericon'])
    async def servergif(self, ctx):
        icon = str(ctx.guild.icon_url)
        name = str(ctx.guild.name)
        embed = discord.Embed(color=0x76D7C4, timestamp=ctx.message.created_at)
        embed.set_author(name=name, icon_url=icon)
        embed.set_image(url=icon)
        await ctx.send(embed=embed)

    @commands.command(aliases=['banner'])
    async def serverbanner(self, ctx):
        banner = str(ctx.guild.banner_url)
        name = str(ctx.guild.name)
        embed = discord.Embed(color=0x76D7C4, timestamp=ctx.message.created_at)
        embed.set_author(name=name, icon_url=banner)
        embed.set_image(url=banner)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["bye", 'goodbye'])
    @commands.check(bot_owner)
    async def leaveserver(self, ctx):
        if ctx.message.author.id == 781708642176860180 or 783380853426094121:
            await ctx.send(f"isaiah is now leaving `{ctx.guild}`, bye bye!")
            await ctx.message.guild.leave()
        else:
            await ctx.send("You cannot use this command.")
