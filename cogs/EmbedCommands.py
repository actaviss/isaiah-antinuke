import discord
from discord.ext import commands
import datetime
import os
import dotenv

prefix = os.getenv("PREFIX")

class EmbedCommands(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook


    @commands.command()
    async def help(self, ctx):
        if category is None:
        embed = discord.Embed(colour=0xEF663E)
        embed.add_field(name=f"Categories! (3)", value=f"`MOD`\n`ANTI`\n`SERVER`", inline=False)
        embed.add_field(name=f"Usage!", value=f"`{prefix}help <CATEGORY>`", inline=False)
        embed.set_author(name="Isaiah!", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.avatar_url)
        embed.set_footer(text=f"Join Our Support Server")
        await ctx.send(embed=embed)

        elif category.lower() == 'mod':
        embed = discord.Embed(colour=0xEF663E,
            description=f"`{^prefix}BAN <user> `\n`{prefix}BAN <user> `{prefix}UNBAN <USER>`\n`{prefix}LOCKDOWN`\n`{prefix}PURGE`\n`{prefix}PURGEME`\n`{prefix}MASSUNBAN`",
      )
        embed.add_field(name=f"Usage!", value=f"`{prefix}[COMMAND]`", inline=False)
        embed.set_author(name="Commands! (5)", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.avatar_url)      
        embed.set_footer(text=f"Category: Mod")
        await ctx.send(embed=embed)

        elif category.lower() == 'anti':
        embed = discord.Embed(colour=0xEF663E,
            description=f"Welcome to the Antinuke Category\n\nTo ensure that you are well protected, move the `ISAIAH` role above everyone\n\nCommands Info\n\n`{prefix}WHITELIST <USER>`\n<:dynoInfo:784848153261506602>Allows the user to bypass isaiah\n\n`{prefix}WHITELISTED`\n<:dynoInfo:784848153261506602>Shows all whitelisted users\n\n`{prefix}DEWHITELIST`\n<:dynoInfo:784848153261506602>Removes a user from the whitelisted database",
      )
        embed.add_field(name=f"Usage!", value=f"`{prefix}[COMMAND]`", inline=False)
        embed.set_author(name="Commands! (3)", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.avatar_url)     
        embed.set_footer(text=f"Category: Anti")
        await ctx.send(embed=embed)

        elif category.lower() == 'server':
        embed = discord.Embed(colour=0xEF663E,
            description=f"`{prefix}ICON`\n`{prefix}BANNER`\n`{prefix}MEMBERCOUNT`\n`{prefix}AVATAR`\n`{prefix}SNIPE`\n`{prefix}NUKE`\n`{prefix}WHOIS`",
      )
        embed.add_field(name=f"Usage!", value=f"`{prefix}[COMMAND]`", inline=False)
        embed.set_author(name="Commands! (7)", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.avatar_url)      
        embed.set_footer(text=f"Category: Server")
        await ctx.send(embed=embed)         

    @commands.command(aliases=['antihelp'])
    async def setup(self, ctx):
        embed = discord.Embed(color=0x66CDAA
        )
        embed.set_author(name="Isaiah Antinuke Help", icon_url=ctx.guild.icon_url)
        embed.add_field(name="Isaiah will be updated throughout time to ensure that your server is well protected!", value=f"To set up the antinuke, you must have isaiah **ABOVE** everyone, this makes sure that not even your staff can do anything risky.\n\nafter, whitelist your **TRUSTED** staff {prefix}`WHITELIST <@USER>`, only the guild owner is able to whitelist and unwhitelist! - by whitelisting a user, you allow them to have access to bypass anything that isaiah protects.\n\nif you ever wish to remove someone from the whitelist database, simple do {prefix}`UNWHITELIST <@USER>`\n\nto view the whitelisted users, do {prefix}`WHITELISTED`")
        embed.set_footer(text=f"{ctx.guild.name}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['invite'])
    async def add(self, ctx):
        embed = discord.Embed(color=0x36393F
        )
        embed.set_author(name="Isaiah Invite Request", icon_url=ctx.guild.icon_url)
        embed.description = "[Click This Link To Add Isaiah To Your Server](https://discord.com/oauth2/authorize?client_id=750898715698659388&scope=bot&permissions=8)"
        embed.set_footer(text=f"{ctx.guild.name}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed) 
