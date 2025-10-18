import discord
from discord.ext import commands
from typing import Union
import asyncio


intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True
intents.moderation = True

with open("../bot_prefix.txt", "r") as bot_prefix_obj:
    aihemuBotPrefix = bot_prefix_obj.readline()

bot = commands.Bot(command_prefix=aihemuBotPrefix, intents=intents, case_insensitive=True)


class BotConfig(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def changeprefix(self, ctx, arg: Union[str, None]):
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

    @commands.command()
    async def enableprefixmessage(self, ctx):
        with open("prefix_message.txt", "r") as pref_msg:
            verify_enable = pref_msg.readline()
            if verify_enable == "True":
                await ctx.send(f"Prefix message is already enabled!")
                return

        with open("prefix_message.txt", "w") as prefix_message:
            prefix_message.write("True")
        await ctx.send("You enabled the prefix message!")

    @commands.command()
    async def disableprefixmessage(self, ctx):
        with open("prefix_message.txt", "r") as pre_msg:
            verify_disable = pre_msg.readline()
            if verify_disable == "False":
                await ctx.send(f"Prefix message is already disabled!")
                return

        with open("prefix_message.txt", "w") as p_message:
            p_message.write("False")
        await ctx.send("You disabled the prefix message!")

    @commands.command()
    async def botprefix(self, ctx):
        with open("bot_prefix.txt", "r") as bot_prefix:
            prefix = bot_prefix.readline()

        await ctx.send(f"The bot prefix is `{prefix}`")

async def setup(bot):
    await bot.add_cog(BotConfig(bot))