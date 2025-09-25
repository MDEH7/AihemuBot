import datetime
import discord
from discord.ext import commands
from discord.ext.commands import BadUnionArgument, MissingRequiredArgument, MemberConverter, UserConverter, UserNotFound
from typing import Union

intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents, case_insensitive=True)


@bot.command()
async def membercount(ctx):
    await ctx.send(f"Member count: {ctx.guild.member_count}") # Displays the total number of users, including other bots

@bot.command()
async def joindate(ctx, member: Union[discord.User, str] = None):
    myGuild = bot.get_guild(726849822350508132)
    discordUserID = 0
    userID = 0
    member_name = 0

    if member is None: # If the user doesn't input an ID
        authorID = ctx.author.id
        authorName = ctx.author.name
        await ctx.send(f"{authorName} `[{authorID}]` is a member of {myGuild}! :)")
        return

    elif isinstance(member, discord.User):
        discordUserID = member.id
        member_name = myGuild.get_member(userID or discordUserID or member)


    else:
        try:
            userID = await commands.UserConverter().convert(ctx, member)
            member_name = myGuild.get_member(userID.id)
            if len(str(userID)) > 19 or len(str(userID)) < 15:
                await ctx.send(f"Invalid ID!\n"
                               f"`Usage: $joindate [ID]`")
                return
        except ValueError:
            await ctx.send(f"Invalid input! "
                           f"ID can only be numbers.\n"
                           f"`Usage: $joindate [ID]`")
            return

        except discord.ext.commands.errors.UserNotFound:
            await ctx.send(f"Invalid ID!\n"
                           f"`Usage: $joindate [ID]`")


    # If a user is not a member of your server
    if member_name is None:
        await ctx.send(f"{member.mention} `[{member.id}]` is not a member of {myGuild}!\n"
                       f"Why not invite them here? ¯\\_(ツ)_/¯")
    else:
        await ctx.send(f"{member.name} `[{member.id}]` is a member of {myGuild}! :)")



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