from discord.ext import commands
import discord
import io

def bot_owner(ctx):
    return ctx.message.author.id == 773630445933166612 or 669334915963158538

class Fun(commands.Cog):
    def __init__(self, client, db, webhook):
        self.client = client
        self.db = db
        self.webhook = webhook


def setup(bot):
    bot.add_cog(Fun(bot))
def setup(bot):
    bot.add_cog(Fun(bot))
