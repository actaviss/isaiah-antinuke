import discord
from discord.ext import commands
import datetime
import asyncio
from discord.ext.commands import MissingPermissions

class Moderation(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook
        
    
    

    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx,*, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Succesfully unbanned <@{user.id}>')
                return
            

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            mbed = discord.Embed(
                description=f'I sucessfully put {channel.name} on lockdown.'
            )
            await channel.edit(overwrites=overwrites)
            await ctx.send(embed=mbed)

        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            mbed = discord.Embed(
                description=f'I sucessfully put {channel.name} on lockdown.'
            )
            await ctx.send(embed=mbed)
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            mbed = discord.Embed(
                description=f'I sucessfully put {channel.name} off lockdown.'
            )
            await ctx.send(embed=mbed)
            
    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, count: int):
        if count>999:
            count = 999
        mbed = discord.Embed(
            description=f'Sucessfully purged {count} messages.', delete_after=4
        )
        await ctx.message.channel.purge(limit=count, bulk=True)
        await ctx.send(embed=mbed)
        await ctx.message.delete()
    
    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def purgeme(self, ctx):
        def is_me(m):
            return m.author == self.client.user
        await ctx.message.channel.purge(limit=999, check=is_me)
        mbed = discord.Embed(
            description=f'Sucessfully purged my own messages', delete_after=4
        )
        await ctx.send(embed=mbed)
        await ctx.message.delete()

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
            await user.ban(reason=reason)
            ban = discord.Embed(
                title=f"Sucessfully banned {user.name}!", description=f"**Reason:** {reason}\n**By**: {ctx.author.mention}"
                )
            await ctx.message.delete()
            await ctx.channel.send(embed=ban)
            await user.send(embed=ban)


    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
            await user.kick(reason=reason)
            kick = discord.Embed(
                title=f"Sucessfully kicked {user.name}!", description=f"**Reason:** {reason}\n**By**: {ctx.author.mention}"
                )
            await ctx.message.delete()
            await ctx.channel.send(embed=kick)
            await user.send(embed=kick)
