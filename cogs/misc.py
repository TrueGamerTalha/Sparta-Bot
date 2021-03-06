import asyncio
import discord
from discord.ext import commands


class Miscellaneous(commands.Cog):
    def __init__(self, bot, theme_color):
        self.bot = bot
        self.theme_color = theme_color

        PREFIX = self.bot.command_prefix
        THEME_COLOR = self.theme_color

        misc_embed = discord.Embed(title="Misc. Help", color=THEME_COLOR)
        misc_embed.add_field(
            name=f"`{PREFIX}help <category>`", value="Displays command help")
        misc_embed.add_field(
            name=f"`{PREFIX}hello`", value="Say hello to the bot")
        misc_embed.add_field(name=f"`{PREFIX}info`",
                             value="Displays the bot's information")
        misc_embed.add_field(
            name=f"`{PREFIX}clear <count>`", value="Deletes messages")
        misc_embed.add_field(name=f"`{PREFIX}nuke`",
                             value="Deletes all messages in a channel")
        misc_embed.add_field(name=f"`{PREFIX}invite`",
                             value="Get the link to invite Sparta Bot to your server")
        misc_embed.add_field(name=f"`{PREFIX}github`",
                             value="Get the link to the GitHub Repository")
        misc_embed.add_field(name=f"`{PREFIX}support`",
                             value="Get an invite to the Sparta Bot Support Server")

        server_settings_embed = discord.Embed(
            title="Server Settings Commands Help", color=THEME_COLOR)
        server_settings_embed.add_field(
            name=f"`{self.bot.command_prefix}welcomemessage <message>`", value="Change the default Welcome Message. Use `[mention]` to mention the user, and mention any channel to show it in the message")
        server_settings_embed.add_field(
            name=f"`{PREFIX}joinrole <role>`", value="Gives this role to all new members who join the server")
        server_settings_embed.add_field(
            name=f"`{PREFIX}serverinfo`", value="Displays server information")
        server_settings_embed.add_field(
            name=f"`{PREFIX}userinfo <user>`", value="Displays user information")
        server_settings_embed.add_field(
            name=f"`{PREFIX}enablerespects`", value="Enables Respects (press f)")
        server_settings_embed.add_field(
            name=f"`{PREFIX}disablerespects`", value="Disables Respects")

        mod_embed = discord.Embed(title="Moderator Help", color=THEME_COLOR)
        mod_embed.add_field(name=f"`{PREFIX}warn <user> <reason>`",
                            value="Warn a user for doing something")
        mod_embed.add_field(name=f"`{PREFIX}clearwarn <user>`",
                            value="Clear a user's warns")
        mod_embed.add_field(name=f"`{PREFIX}warncount <user>`",
                            value="Displays how many times a user has been warned")
        mod_embed.add_field(name=f"`{PREFIX}mute <user> <time>`",
                            value="Mutes a user. You can optionally provide a time as well. Ex: 5s, 4m, 2h")
        mod_embed.add_field(
            name=f"`{PREFIX}unmute <user>`", value="Unmutes a user")
        mod_embed.add_field(name=f"`{PREFIX}ban <user> <reason>`",
                            value="Bans a user from the server")
        mod_embed.add_field(name=f"`{PREFIX}unban <username with #number> <reason>`",
                            value="Unbans a user from the server")
        mod_embed.add_field(name=f"`{PREFIX}kick <user> <reason>`",
                            value="Kicks a user from the server")
        mod_embed.add_field(name=f"`{PREFIX}lockchannel <channel>`",
                            value="Locks a channel so only Administrators can use it")
        mod_embed.add_field(name=f"`{PREFIX}unlockchannel <channel>`",
                            value="Unlocks a channel so every server member can use it")

        auto_embed = discord.Embed(
            title="Auto Moderator Help", color=THEME_COLOR)
        auto_embed.add_field(name=f"`{PREFIX}activateautomod`",
                             value="Turns on Automod in your server")
        auto_embed.add_field(name=f"`{PREFIX}stopautomod`",
                             value="Turns off Automod in your server")
        auto_embed.add_field(name=f"`{PREFIX}whitelistuser <user>`",
                             value="Make a user immune to Auto Mod (Administrators are already immune)")
        auto_embed.add_field(name=f"`{PREFIX}whitelisturl <url>`",
                             value="Allow a specific url to bypass the Auto Mod")
        auto_embed.add_field(name=f"`{PREFIX}whitelistchannel <channel>`",
                             value="Allow a specific channel to bypass the Auto Mod")
        auto_embed.add_field(name=f"`{PREFIX}automodstatus`",
                             value="Displays the status of AutoMod in your server")

        programming_embed = discord.Embed(
            title="Programming Commands Help", color=THEME_COLOR)
        programming_embed.add_field(
            name=f"`{PREFIX}eval <code in codeblocks>`", value="Allows you to run Python3 code in Discord")

        fun_embed = discord.Embed(title="Fun Commands Help", color=THEME_COLOR)
        fun_embed.add_field(name=f"`{PREFIX}coinflip`", value="Flip a coin")
        fun_embed.add_field(name=f"`{PREFIX}roll`", value="Roll a dice")
        fun_embed.add_field(name=f"`{PREFIX}avatar <user>`",
                            value="Display a users avatar")

        self.help_index = 0
        self.current_help_msg = None
        self.current_help_user = None
        self.all_help_embeds = [misc_embed, server_settings_embed,
                                mod_embed, auto_embed, programming_embed, fun_embed]
        self.help_control_emojis = ["⬅️", "➡️"]

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        if reaction.message.id == self.current_help_msg and user.id != 731763013417435247:
            if user.id == self.current_help_user:
                channel: discord.TextChannel = reaction.message.channel

                if reaction.emoji == self.help_control_emojis[0]:
                    self.help_index -= 1

                if reaction.emoji == self.help_control_emojis[1]:
                    self.help_index += 1

                if self.help_index < 0:
                    self.help_index = len(self.all_help_embeds) - 1
                elif self.help_index >= len(self.all_help_embeds):
                    self.help_index = 0

                message: discord.Message = await channel.fetch_message(self.current_help_msg)
                await message.edit(embed=self.all_help_embeds[self.help_index])
                await message.remove_reaction(reaction.emoji, user)

    @commands.command(name="help")
    async def _help(self, ctx):
        msg: discord.Message = await ctx.send("Here is the command help:", embed=self.all_help_embeds[self.help_index])

        for emoji in self.help_control_emojis:
            await msg.add_reaction(emoji)

        self.current_help_msg = msg.id
        self.current_help_user = ctx.author.id

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send("Hi, I am Sparta Bot!")

    @commands.command(name="info")
    async def info(self, ctx):
        embed = discord.Embed(title="Bot Information", color=self.theme_color)
        ping = round(self.bot.latency * 1000)
        guild_count = len(self.bot.guilds)
        member_count = 0

        for guild in self.bot.guilds:
            member_count += guild.member_count

        embed.add_field(name="Ping", value=f"{ping}ms")
        embed.add_field(name="Servers", value=guild_count)
        embed.add_field(name="Total Users", value=member_count)

        await ctx.send(content=None, embed=embed)

    @commands.command(name="invite")
    async def invite(self, ctx):
        invite_url = "https://discord.com/oauth2/authorize?client_id=731763013417435247&permissions=8&scope=bot"
        embed = discord.Embed(
            title="Click here to invite Sparta Bot!", url=invite_url, color=self.theme_color)
        await ctx.send(content=None, embed=embed)

    @commands.command(name="github")
    async def github(self, ctx):
        repo_url = "https://github.com/MysteryCoder456/Sparta-Bot"
        embed = discord.Embed(
            title="Click here to go to the GitHub Repository!", url=repo_url, color=self.theme_color)
        await ctx.send(content=None, embed=embed)

    @commands.command(name="support")
    async def support(self, ctx):
        invite_url = "https://discord.gg/RrVY4bP"
        embed = discord.Embed(
            title="Click here to get an invite to the Sparta Bot Support Server!", url=invite_url, color=self.theme_color)
        await ctx.send(content=None, embed=embed)

    @commands.command(name="clear")
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, count: int = None):
        if count is None:
            await ctx.send("Insufficient arguments.")
        else:
            await ctx.channel.purge(limit=count+1)
            await ctx.send(f"Cleared the last {count} message(s)!")
            await asyncio.sleep(3)
            await ctx.channel.purge(limit=1)

    @commands.command(name="nuke")
    @commands.has_guild_permissions(manage_messages=True)
    async def nuke(self, ctx):
        temp_channel = await ctx.channel.clone()
        await temp_channel.edit(position=ctx.channel.position)
        await ctx.channel.delete(reason="Nuke")
        await ctx.send("Nuked this channel!")
