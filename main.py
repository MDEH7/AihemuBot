import datetime
import discord
from discord.ext import commands
from typing import Union
from discord.ext.commands import BadUnionArgument, MissingRequiredArgument

intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, case_insensitive=True)


@bot.command()
async def membercount(ctx):
    await ctx.send(f"Member count: {ctx.guild.member_count}") # Displays the total number of users, including other bots

@bot.command()
async def joindate(ctx, member: str):
    try:
        memberID_int = int(member)
    except ValueError:
        await ctx.send(f"Invalid input!\n"
                       f"ID can only be numbers.\n"
                       f"`Usage: $joindate [ID]`")

    except MissingRequiredArgument:
        await ctx.send(f"Missing ID!\n"
                       f"`Usage: $joindate [ID]`")


    # If the user supplied ID is not 18 digits long
    if len(str(memberID_int)) != 18:
        await ctx.send(f"Invalid ID!\n"
                       f"ID must be 18 digits long.\n"
                       f"`Usage: $joindate [ID]`")
        return


    else:
        myGuild = bot.get_guild(726849822350508132)
        member_name = myGuild.get_member(memberID_int)


    # If a user is not a member of your server
    if member_name is None:
        await ctx.send(f"<@{member}> `[{member}]` is not a member of {myGuild}!\n"
                       f"Why not invite them here? ¯\\_(ツ)_/¯")
    else:
        await ctx.send(f"{member_name} `[{member}]` is a member of {myGuild}! :)")



@bot.event
async def on_ready():
    print(f'Login as {bot.user} successful!')

@bot.event
async def on_connect():
    print(f"{bot.user} has successfully connected to Discord!")

@bot.event
async def on_disconnect():
    print(f"{bot.user} has disconnected from Discord!")

bot.run("Bot_Token_Here")