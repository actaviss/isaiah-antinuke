import discord
from discord.ext import commands
import datetime

class AntiEvents(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        whitelistedUsers = self.db.find_one({ "guild_id": guild.id })["users"]
        async for i in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.ban):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
            
            await guild.ban(i.user, reason="Banned a member")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        whitelistedUsers = self.db.find_one({ "guild_id": member.guild.id })["users"]
        guild = member.guild
        async for i in member.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.kick):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return
                
            if i.target.id == member.id:
                await guild.ban(i.user, reason="Kicked a member")
                return
    

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        whitelistedUsers = self.db.find_one({ "guild_id": role.guild.id })["users"]
        guild = role.guild
        async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_create):
            if i.user.bot:
                return
            
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await guild.ban(i.user, reason="Created a role")
            return

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        whitelistedUsers = self.db.find_one({ "guild_id": role.guild.id })["users"]
        async for i in role.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_delete):
            if i.user.bot:
                return

            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await guild.ban(i.user, reason="Deleted a role")
            return

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild = after.guild
        whitelistedUsers = self.db.find_one({ "guild_id": after.guild.id })["users"]
        async for i in after.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.role_update):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            if not before.permissions.ban_members and after.permissions.ban_members:
                await guild.ban(i.user, reason="Added ban premission to a role")
                await after.edit(permissions=1166401)
                return

            if not before.permissions.kick_members and after.permissions.kick_members:
                await guild.ban(i.user, reason="Added kick premission to a role")
                await after.edit(permissions=1166401)
                return

            if not before.permissions.administrator and after.permissions.administrator:
                await guild.ban(i.user, reason="Added administrator premission to a role")
                await after.edit(permissions=1166401)
                return

            if i.target.id == before.guild.id:
                if after.permissions.kick_members or after.permissions.ban_members or after.permissions.administrator or after.permissions.mention_everyone or after.permissions.manage_roles:
                    await guild.ban(i.user, reason="Added dangerous premission to a role")
                    await after.edit(permissions=1166401)
                    
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        whitelistedUsers = self.db.find_one({ "guild_id": channel.guild.id })["users"]
        async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_delete):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await guild.ban(i.user, reason="Deleted a channel")
            await guild.user(i.user, reason="Was banned by an unwhitelisted user.")
            return

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        whitelistedUsers = self.db.find_one({ "guild_id": channel.guild.id })["users"]
        async for i in channel.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.channel_create):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await guild.ban(i.user, reason="Created a channel")
            await channel.delete(reason="Channel creation without being whitelisted")
            return

    @commands.Cog.listener()
    async def on_webhook_update(self, webhook):
        guild = webhook.guild
        whitelistedUsers = self.db.find_one({ "guild_id": webhook.guild.id })["users"]
        async for i in webhook.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 2), action=discord.AuditLogAction.webhook_create):
            if i.user.id in whitelistedUsers or i.user in whitelistedUsers:
                return

            await guild.ban(i.user, reason="Updated a webhook")
            await i.target.delete()
            return
