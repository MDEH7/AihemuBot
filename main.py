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

bot = commands.Bot(command_prefix=aihemuBotPrefix, intents=intents, case_insensitive=True)


@bot.command()
async def membercount(ctx):
    await ctx.send(f"Member count: {ctx.guild.member_count}") # Displays the total number of users, including other bots

@bot.command()
async def joindate(ctx, member: str = None): # Users can only input valid Discord IDs
    myGuild = bot.get_guild(726849822350508132)

    if member is None: # If the user doesn't input an ID
        discordMember = await MemberConverter().convert(ctx, ctx.author.name)
        await ctx.send(f"{ctx.author.name} `[{ctx.author.id}]` is a member of {myGuild}! :)\n"
                       f"You joined at `{discordMember.joined_at.strftime('%d/%m/%Y')}`")
        return


    elif not member.isdigit(): # Checking to see if the user did not input digits only
        await ctx.send(f"Invalid ID! ID can only contain numbers!\n"
                       f"`Usage: {bot.command_prefix}joindate [ID]`")
        return

    elif len(str(member)) > 19 or len(str(member)) < 15:
        await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!\n"
                       f"`Usage: {bot.command_prefix}joindate [ID]`")
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
                               f"`Usage: {bot.command_prefix}joindate [ID]`")
                return

    member_name = myGuild.get_member(int(member))



    # If a user is not a member of your server
    if member_name is None:
        await ctx.send(f"{discordMember.mention} `[{discordMember.id}]` is not a member of {myGuild}!\n"
                       f"Why not invite them here? ¯\\_(ツ)_/¯")
    else:
        await ctx.send(f"{discordMember.name} `[{discordMember.id}]` is a member of {myGuild}! :)\n"
                       f"They joined at `{discordMember.joined_at.strftime('%d/%m/%Y')}`")

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
        prefix = bot_prefix.readline()

    await ctx.send(f"The bot prefix is `{prefix}`")

@bot.command()
async def ban(ctx, user: str = None):

    if user is None:
        await ctx.send(f"Incorrect usage!\n"
                       f"Correct usage: `{bot.command_prefix}ban [userID]`")
        return

    elif not user.isdigit():
        await ctx.send(f"Invalid ID! ID can only contain numbers!\n"
                       f"`Usage: {bot.command_prefix}ban [userID]`")
        return

    elif len(user) > 19 or len(user) < 15:
        await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!\n"
                       f"`Usage: {bot.command_prefix}ban [userID]`")
        return


    try: # Trying to convert the user into a Member object
        bannedMember = await MemberConverter().convert(ctx, user)

    except discord.ext.commands.errors.MemberNotFound: # If the conversion fails i.e. the user being banned is not on the server
        try: # Try to convert the user into a User object to see if the user exists in Discord
            bannedMember = await UserConverter().convert(ctx, user)

        except discord.ext.commands.errors.UserNotFound:
            await ctx.send(f"Invalid ID! User with ID: `{user}` does not exist!\n"
                           f"`Usage: {bot.command_prefix}ban [userID]`")
            return

        await ctx.send(f"Ban failed! {bannedMember.mention} `{bannedMember.id}` is not a member of the server!")
        return


    await ctx.guild.ban(bannedMember)
    await ctx.send(f"{bannedMember.mention} `{bannedMember.id}` was banned by {ctx.author.name}!")


@bot.command()
async def unban(ctx, user: str = None):

    if user is None:
        await ctx.send(f"Incorrect usage!\n"
                       f"Correct usage: `{bot.command_prefix}unban [userID]`")
        return

    elif not user.isdigit():
        await ctx.send(f"Invalid ID! ID can only contain numbers!\n"
                       f"`Usage: {bot.command_prefix}unban [userID]`")
        return

    elif len(user) > 19 or len(user) < 15:
        await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!\n"
                       f"`Usage: {bot.command_prefix}unban [userID]`")
        return

    try:
        unbannedUser = await UserConverter().convert(ctx, user)
        await ctx.guild.unban(unbannedUser)

    except discord.ext.commands.errors.UserNotFound:
        await ctx.send(f"Invalid ID! User with ID: `{user}` does not exist!\n"
                       f"`Usage: {bot.command_prefix}unban [userID]`")
        return

    except discord.HTTPException: # If the user being unbanned is not banned
        await ctx.send(f"Unban failed! {unbannedUser.mention} `{unbannedUser.id}` is not banned from the server!")
        return

    await ctx.send(f"{unbannedUser.mention} `{unbannedUser.id}` was unbanned by {ctx.author.name}!")


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