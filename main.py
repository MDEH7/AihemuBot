import datetime
import discord
from discord.ext import commands
from discord.ext.commands import BadUnionArgument, MissingRequiredArgument, MemberConverter, UserConverter, UserNotFound
from typing import Union
import asyncio

intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True

with open("bot_prefix.txt", "r") as bot_prefix_obj:
    aihemuBotPrefix = bot_prefix_obj.readline()

bot = commands.Bot(command_prefix=aihemuBotPrefix, intents=intents, case_insensitive=True)


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

@bot.command()
async def changeprefix(ctx, arg: Union[str, None]):
    if arg is None:
        await ctx.send(f"Are you trying to break this command? <:neutralexpr:1233524707110948884>\n"
                       f"This is the correct usage: `{bot.command_prefix}changeprefix [prefix]`")
        return

    with open("prefix_message.txt", "r") as prefix_msg:
        p_msg = prefix_msg.readline()

    before = bot.command_prefix
    with open("bot_prefix.txt", "w") as prefix_obj:
        prefix_obj.write(arg)

    with open("bot_prefix.txt", "r") as read_prefix:
        bot.command_prefix = read_prefix.readline()

    await ctx.send(f"You successfully changed the prefix from `{before}` to `{bot.command_prefix}`")
    if len(arg) > 1 and p_msg == "True":
        await asyncio.sleep(0.75)
        await ctx.send(f"-# Yes! The prefix can be longer than 1 character! Why? Because I'm generous!")



@bot.command()
async def enableprefixmessage(ctx):
    with open("prefix_message.txt", "r") as pref_msg:
        verify_enable = pref_msg.readline()
        if verify_enable == "True":
            await ctx.send(f"Prefix message is already enabled!")
            return

    with open("prefix_message.txt", "w") as prefix_message:
        prefix_message.write("True")
    await ctx.send("You enabled the prefix message!")


@bot.command()
async def disableprefixmessage(ctx):
    with open("prefix_message.txt", "r") as pre_msg:
        verify_disable = pre_msg.readline()
        if verify_disable == "False":
            await ctx.send(f"Prefix message is already disabled!")
            return


    with open("prefix_message.txt", "w") as p_message:
        p_message.write("False")
    await ctx.send("You disabled the prefix message!")


@bot.command()
async def botprefix(ctx):
    with open("bot_prefix.txt", "r") as bot_prefix:
        prefix = bot_prefix.read(1)

    await ctx.send(f"The bot prefix is `{prefix}`")

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