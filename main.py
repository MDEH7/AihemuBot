import datetime
import discord
from discord.ext import commands
from discord.ext.commands import BadUnionArgument, UserConverter, UserNotFound, MemberConverter, MemberNotFound
from typing import Union
import asyncio

intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True


with open("bot_prefix.txt", "r") as bot_prefix_obj:
    aihemuBotPrefix = bot_prefix_obj.readline()

# bot = commands.Bot(command_prefix=aihemuBotPrefix, intents=intents, case_insensitive=True)

class Aihemu(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix=aihemuBotPrefix, intents=intents, case_insensitive=True)


    async def on_ready(self):
        print(f'Login as {self.user} successful!')
        # await self.load_extension("cogs.moderation")
        await self.load_extension("cogs.botconfig")



AihemuBot = Aihemu()
# AihemuBot.run("Bot_Token_Here")

# @AihemuBot.command() is a decorator that registers the commands below to the bot
# Aihemu class must be instantiated before you can use the decorator
@AihemuBot.command()
async def membercount(ctx):
    await ctx.send(f"Member count: {ctx.guild.member_count}") # Displays the total number of users, including other bots


@AihemuBot.command()
async def joindate(ctx, member: str = None): # Users can only input valid Discord IDs
    myGuild = AihemuBot.get_guild(726849822350508132)

    if member is None: # If the user doesn't input an ID
        discordMember = await MemberConverter().convert(ctx, ctx.author.name)
        await ctx.send(f"{ctx.author.name} `[{ctx.author.id}]` is a member of {myGuild}! :)\n"
                       f"You joined at `{discordMember.joined_at.strftime('%d/%m/%Y')}`")
        return


    elif not member.isdigit(): # Checking to see if the user did not input digits only
        await ctx.send(f"Invalid ID! ID can only contain numbers!\n"
                       f"`Usage: {AihemuBot.command_prefix}joindate [ID]`")
        return

    elif len(str(member)) > 19 or len(str(member)) < 15:
        await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!\n"
                       f"`Usage: {AihemuBot.command_prefix}joindate [ID]`")
        return

    else:
        try:
            discordMember = await MemberConverter().convert(ctx, member) # Trying to convert the user into a Member object
        except discord.ext.commands.errors.MemberNotFound:
            try:
                discordMember = await UserConverter().convert(ctx, member) # Trying to convert the user into a User object
                await ctx.send(f"{discordMember.mention} `[{discordMember.id}]` is not a member of {myGuild}!\n"
                               f"Why not invite them here? ¯\\_(ツ)_/¯")
                return
            except discord.ext.commands.errors.UserNotFound: # If the inputted ID does not belong to any user of the Discord app
                await ctx.send(f"Invalid ID! User with ID: `{member}` does not exist!\n"
                               f"`Usage: {AihemuBot.command_prefix}joindate [ID]`")
                return

    member_name = myGuild.get_member(int(member))



    # If a user is not a member of your server
    if member_name is None:
        await ctx.send(f"{discordMember.mention} `[{discordMember.id}]` is not a member of {myGuild}!\n"
                       f"Why not invite them here? ¯\\_(ツ)_/¯")
    else:
        await ctx.send(f"{discordMember.name} `[{discordMember.id}]` is a member of {myGuild}! :)\n"
                       f"They joined at `{discordMember.joined_at.strftime('%d/%m/%Y')}`")

"""@bot.event
async def on_ready():
    print(f'Login as {bot.user} successful!')

@bot.event
async def on_connect():
    print(f"{bot.user} has successfully connected to Discord!")

@bot.event
async def on_disconnect():
    print(f"{bot.user} has disconnected from Discord!")
"""

# AihemuBot = Aihemu()
AihemuBot.run("Bot_Token_Here")