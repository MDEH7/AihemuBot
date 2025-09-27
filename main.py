import datetime
import discord
from discord.ext import commands
from discord.ext.commands import BadUnionArgument,UserConverter, UserNotFound
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
        await ctx.send(f"{ctx.author.name} `[{ctx.author.id}]` is a member of {myGuild}! :)")
        return

    else:
        if not member.isdigit(): # Checking to see if the user did not input digits only
            await ctx.send(f"Invalid ID! ID can only contain numbers!\n"
                           f"`Usage: $joindate [ID]`")
            return

        else:
            if len(str(member)) > 19 or len(str(member)) < 15:
                await ctx.send(f"Invalid ID! ID must between 15 to 19 numbers long inclusive!\n"
                               f"`Usage: $joindate [ID]`")
                return

            try:
                discordMember = await UserConverter().convert(ctx, member)
            except UserNotFound:
                await ctx.send(f"Invalid ID! User with ID: `{member}` was not found!\n"
                               f"`Usage: $joindate [ID]`")
                return

        member_name = myGuild.get_member(int(member))



    # If a user is not a member of your server
    if member_name is None:
        await ctx.send(f"{discordMember.mention} `[{discordMember.id}]` is not a member of {myGuild}!\n"
                       f"Why not invite them here? ¯\\_(ツ)_/¯")
    else:
        await ctx.send(f"{discordMember.name} `[{discordMember.id}]` is a member of {myGuild}! :)")

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