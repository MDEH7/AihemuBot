import discord
from discord.ext import commands
from discord.ext.commands import UserConverter, UserNotFound, MemberConverter, MemberNotFound


intents = discord.Intents.default() # All intents except presences are enabled
intents.message_content = True
intents.messages = True
intents.members = True
intents.moderation = True



with open("../bot_prefix.txt", "r") as bot_prefix_obj:
    aihemuBotPrefix = bot_prefix_obj.readline()

bot = commands.Bot(command_prefix=aihemuBotPrefix, intents=intents, case_insensitive=True)


class moderatorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, user: str = None):

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

        try:  # Trying to convert the user into a Member object
            bannedMember = await MemberConverter().convert(ctx, user)

        except discord.ext.commands.errors.MemberNotFound:  # If the conversion fails i.e. the user being banned is not on the server
            try:  # Try to convert the user into a User object to see if the user exists in Discord
                bannedMember = await UserConverter().convert(ctx, user)

            except discord.ext.commands.errors.UserNotFound:
                await ctx.send(f"Invalid ID! User with ID: `{user}` does not exist!\n"
                               f"`Usage: {bot.command_prefix}ban [userID]`")
                return

            await ctx.send(f"Ban failed! {bannedMember.mention} `{bannedMember.id}` is not a member of the server!")
            return

        await ctx.guild.ban(bannedMember)
        await ctx.send(f"{bannedMember.mention} `{bannedMember.id}` was banned by {ctx.author.name}!")

    @commands.command()
    async def unban(self, ctx, user: str = None):

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

        except discord.HTTPException:  # If the user being unbanned is not banned
            await ctx.send(f"Unban failed! {unbannedUser.mention} `{unbannedUser.id}` is not banned from the server!")
            return

        await ctx.send(f"{unbannedUser.mention} `{unbannedUser.id}` was unbanned by {ctx.author.name}!")


async def setup(bot):
    await bot.add_cog(moderatorCommands(bot))