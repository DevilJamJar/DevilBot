# -*- coding: utf-8 -*-

import json
import discord
from discord.ext import commands
from .utils import checks


def getallcustoms(object_):
    dicted = {}
    for i in dir(object_):
        if not str(i).startswith('_') and not str(getattr(object_, i)).startswith('<') and not str(getattr(object_, i)).startswith('(') and not str(i) == 'overwrites' and 'status' not in str(i).lower() and 'activity' not in str(i).lower():
            dicted[i] = str(getattr(object_, i))
    return dicted


class loggingCog(commands.Cog):
    """Logging commands"""

    def __init__(self, bot):
        self.bot = bot
        self.db_conn = bot.db_conn
        self.colour = 0xff9300
        self.events = [
            "message_delete",
            "message_edit",
            "reaction_add",
            "reaction_remove",
            "reaction_clear",
            "channel_delete",
            "channel_create",
            "channel_edit",
            "channel_pin",
            "channel_webhook",
            "guild_integration",
            "member_join",
            "member_leave",
            "member_edit",
            "member_ban",
            "member_unban",
            "role_create",
            "role_delete",
            "role_edit",
            "emoji_edit",
            "invite_create",
            "invite_delete"
        ]
        with open('logging.json', 'r') as f:
            self.logging_dict = json.load(f)

    @commands.Cog.listener(name="on_message_delete")
    async def logging_message_delete(self, message):
        if not message.guild:
            return
        if message.is_system:
            return
        if str(message.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(message.guild.id)]
        if not logging_dict["message_delete"]:
            return
        if message.author == message.guild.me and len(message.embeds) > 0:
            return
        try:
            logging_channel = message.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:wastebasket: Message sent by {message.author.mention} deleted in {message.channel.mention}.**',
            timestamp=message.created_at
        )
        if message.guild.me.guild_permissions.view_audit_log:
            entry = await message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.description = f'{embed.description}\n{message.content[:1900]}'
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text=f'{message.guild.name} • Message created')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_message_edit")
    async def logging_message_edit(self, before, after):
        if not after.guild:
            return
        if str(after.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(after.guild.id)]
        if not logging_dict["message_edit"]:
            return
        if after.author == after.guild.me and len(after.embeds) > 0:
            return
        if before.content == after.content:
            return
        try:
            logging_channel = after.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:pencil: Message sent by {after.author.mention} edited in {after.channel.mention}.** [Jump to message]({after.jump_url})',
            timestamp=after.created_at
        )
        embed.add_field(name='Old', value=before.content, inline=False)
        embed.add_field(name='New', value=after.content, inline=False)
        embed.set_author(name=after.author, icon_url=after.author.avatar_url)
        embed.set_footer(text=f'{after.guild.name} • Message created')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_reaction_add")
    async def logging_reaction_add(self, reaction, user):
        message = reaction.message
        if not message.guild:
            return
        if str(message.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(message.guild.id)]
        if not logging_dict["reaction_add"]:
            return
        try:
            logging_channel = message.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:inbox_tray: Reaction added by {user.mention} in {message.channel.mention}.** [Jump to message]({message.jump_url})\n{reaction.emoji}',
            timestamp=message.created_at
        )
        embed.set_author(name=user, icon_url=user.avatar_url)
        embed.set_footer(text=f'{message.guild.name} • Message created')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_reaction_remove")
    async def logging_reaction_remove(self, reaction, user):
        message = reaction.message
        if not message.guild:
            return
        if str(message.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(message.guild.id)]
        if not logging_dict["reaction_remove"]:
            return
        try:
            logging_channel = message.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:outbox_tray: Reaction by {user.mention} removed in {message.channel.mention}.** [Jump to message]({message.jump_url})\n{reaction.emoji}',
            timestamp=message.created_at
        )
        embed.set_author(name=user, icon_url=user.avatar_url)
        embed.set_footer(text=f'{message.guild.name} • Message created')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_reaction_clear")
    async def logging_reaction_clear(self, message, reactions):
        if not message.guild:
            return
        if str(message.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(message.guild.id)]
        if not logging_dict["reaction_clear"]:
            return
        try:
            logging_channel = message.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:x: Message by {message.author.mention} had reactions cleared in {message.channel.mention}.** [Jump to message]({message.jump_url})',
            timestamp=message.created_at
        )
        embed.set_author(name=message.author, icon_url=message.author.avatar_url)
        embed.set_footer(text=f'{message.guild.name} • Message created')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_channel_delete")
    async def logging_channel_delete(self, channel):
        if not channel.guild:
            return
        if str(channel.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(channel.guild.id)]
        if not logging_dict["channel_delete"]:
            return
        try:
            logging_channel = channel.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:wastebasket: Guild channel \'{channel.name}\' was deleted.**'
        )
        if channel.guild.me.guild_permissions.view_audit_log:
            entry = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{channel.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_channel_create")
    async def logging_channel_create(self, channel):
        if not channel.guild:
            return
        if str(channel.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(channel.guild.id)]
        if not logging_dict["channel_create"]:
            return
        try:
            logging_channel = channel.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:writing_hand: Guild channel {channel.mention} was created.**'
        )
        if channel.guild.me.guild_permissions.view_audit_log:
            entry = await channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{channel.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_webhooks_update")
    async def logging_channel_webhook(self, channel):
        if not channel.guild:
            return
        if str(channel.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(channel.guild.id)]
        if not logging_dict["channel_webhook"]:
            return
        try:
            logging_channel = channel.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:pencil: Guild channel {channel.mention} had its webhooks updated.**'
        )
        embed.set_footer(text=f'{channel.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_channel_update")
    async def logging_channel_edit(self, before, after):
        if not after.guild:
            return
        if str(after.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(after.guild.id)]
        if not logging_dict["channel_edit"]:
            return
        try:
            logging_channel = after.guild.get_channel(logging_dict["channel"])
        except:
            return
        before_dir = getallcustoms(before)
        after_dir = getallcustoms(after)
        changes = {}
        for x, y in after_dir.items():
            if y not in list(before_dir.values()):
                changes[x] = y
        if not len(list(changes.keys())):
            return
        changesstr = ''
        for a, b in changes.items():
            changesstr += f'**• {str(a).replace("_", " ").title()} was** {getattr(before, a)} **now** {b}\n'
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:pencil: Guild channel {after.mention} was edited.**'
        )
        embed.add_field(name='Changes', value=changesstr)
        if after.guild.me.guild_permissions.view_audit_log:
            entry = await after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{after.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_channel_pins_update")
    async def logging_channel_pin(self, channel, last_pin):
        if not channel.guild:
            return
        if str(channel.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(channel.guild.id)]
        if not logging_dict["channel_pin"]:
            return
        try:
            logging_channel = channel.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:pushpin: Guild channel {channel.mention} had its pins updated.**'
        )
        embed.set_footer(text=f'{channel.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_integrations_update")
    async def logging_guild_integration(self, guild):
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["guild_integration"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:globe_with_meridians: Guild integrations updated.**'
        )
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_member_join")
    async def logging_member_join(self, member):
        if not member.guild:
            return
        if str(member.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(member.guild.id)]
        if not logging_dict["member_join"]:
            return
        try:
            logging_channel = member.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:heavy_plus_sign: Member {member.mention} just joined the guild.**'
        )
        embed.set_footer(text=f'{member.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_member_remove")
    async def logging_member_leave(self, member):
        if not member.guild:
            return
        if str(member.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(member.guild.id)]
        if not logging_dict["member_leave"]:
            return
        try:
            logging_channel = member.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:heavy_minus_sign: Member {member.mention} "{member}" just left the guild.**'
        )
        embed.set_footer(text=f'{member.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_member_update")
    async def logging_member_edit(self, before, after):
        if not after.guild:
            return
        if str(after.guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(after.guild.id)]
        if not logging_dict["member_edit"]:
            return
        try:
            logging_channel = after.guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:pencil: Member {after.mention} was edited.**'
        )
        before_dir = getallcustoms(before)
        after_dir = getallcustoms(after)
        changes = {}
        for x, y in after_dir.items():
            if y not in list(before_dir.values()):
                changes[x] = y
        if not len(list(changes.keys())):
            return
        changesstr = ''
        for a, b in changes.items():
            changesstr += f'**• {str(a).replace("_", " ").title()} was** {getattr(before, a)} **now** {b}\n'
        embed.add_field(name='Changes', value=changesstr)
        embed.set_footer(text=f'{after.guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_member_ban")
    async def logging_member_ban(self, guild, user):
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["member_ban"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:no_entry: User {user} just got banned.**'
        )
        if guild.me.guild_permissions.view_audit_log:
            entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
                ban = await guild.bans()
                ban = ban[0]
                embed.add_field(name='Reason', value=ban.reason)
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_member_unban")
    async def logging_member_unban(self, guild, user):
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["member_unban"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:wrench: User {user} just got unbanned.**'
        )
        if guild.me.guild_permissions.view_audit_log:
            entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.unban).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_role_create")
    async def logging_role_create(self, role):
        guild = role.guild
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["role_create"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:loudspeaker: Role {role.mention} just got created.**'
        )
        if guild.me.guild_permissions.view_audit_log:
            entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_role_delete")
    async def logging_role_delete(self, role):
        guild = role.guild
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["role_delete"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:name_badge: Role "{role.name}" just got deleted.**'
        )
        if guild.me.guild_permissions.view_audit_log:
            entry = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_role_update")
    async def logging_role_edit(self, before, after):
        guild = after.guild
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["role_edit"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:pencil2: Role {after.mention} just got edited.**'
        )
        before_dir = getallcustoms(before)
        after_dir = getallcustoms(after)
        changes = {}
        for x, y in after_dir.items():
            if y not in list(before_dir.values()):
                changes[x] = y
        if not len(list(changes.keys())):
            return
        changesstr = ''
        for a, b in changes.items():
            changesstr += f'**• {str(a).replace("_", " ").title()} was** {getattr(before, a)} **now** {b}\n'
        embed.add_field(name='Changes', value=changesstr)
        if after.guild.me.guild_permissions.view_audit_log:
            entry = await after.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update).flatten()
            if len(entry) > 0:
                entry = entry[0]
                embed.description = f'{embed.description[:-3]} by {entry.user.mention}.**'
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_guild_emojis_update")
    async def emoji_edit(self, guild, before, after):
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["emoji_edit"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:symbols: Emojis just got updated.**'
        )
        changesstr = ''
        for emoji in before:
            if emoji not in after:
                changesstr += f'**• Emoji "{emoji.name}" got deleted.**\n'
        for emoji in after:
            if emoji not in before:
                changesstr += f'**• Emoji {emoji} got created.**\n'
        if not len(changesstr) > 0:
            return
        embed.add_field(name='Changes', value=changesstr)
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_invite_create")
    async def logging_invite_create(self, invite):
        guild = invite.guild
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["invite_create"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:wave: Invite {invite.code} for {invite.channel.mention} just got created by {invite.inviter.mention}.**'
        )
        embed.add_field(name='Usage', value=f'**• Max uses - {invite.max_uses if invite.max_uses != 0 else "Unlimited"}**\n**• Minutes until expiration - {round(invite.max_age / 60) if invite.max_age != 0 else "Permanent"}**')
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.Cog.listener(name="on_invite_delete")
    async def logging_invite_delete(self, invite):
        guild = invite.guild
        if not guild:
            return
        if str(guild.id) not in list(self.logging_dict.keys()):
            return
        logging_dict = self.logging_dict[str(guild.id)]
        if not logging_dict["invite_delete"]:
            return
        try:
            logging_channel = guild.get_channel(logging_dict["channel"])
        except:
            return
        embed = discord.Embed(
            colour=self.colour,
            description=f'**:door: Invite {invite.code} for {invite.channel.mention} just got deleted.**'
        )
        embed.set_footer(text=f'{guild.name}')
        await logging_channel.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=['log'])
    @checks.check_admin_or_owner()
    async def logging(self, ctx):
        """Logging command group, see subcommands for setup. Requires administrator."""
        await ctx.send_help(ctx.command)

    @logging.group(invoke_without_command=True, aliases=['modes', 'mode'])
    @checks.check_admin_or_owner()
    async def settings(self, ctx):
        """Displays settings for current logger. Use settings toggle to change settings."""
        if str(ctx.guild.id) not in list(self.logging_dict.keys()):
            raise commands.BadArgument("This guild does not have logging set up.")

        log_dict = self.logging_dict[str(ctx.guild.id)]
        logstr = ''
        for name, option in log_dict.items():
            if name != 'channel':
                logstr += f'• {name} — **{"On" if option else "Off"}**\n'
        embed = discord.Embed(
            colour=self.colour,
            description=logstr,
            title='Event Log Filter Settings'
        )
        embed.set_footer(text=ctx.guild.name)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.reply(embed=embed)

    @settings.command(aliases=['set', 'change'])
    @checks.check_admin_or_owner()
    async def toggle(self, ctx, setting):
        """Toggles specified log setting for your guild."""
        if str(ctx.guild.id) not in list(self.logging_dict.keys()):
            raise commands.BadArgument("This guild does not have logging set up.")

        setting = setting.replace(' ', '_').lower()

        if self.logging_dict[str(ctx.guild.id)].get(setting) is None:
            raise commands.BadArgument('Couldn\'t find a setting with that name')

        if not self.logging_dict[str(ctx.guild.id)][setting]:
            self.logging_dict[str(ctx.guild.id)][setting] = True
            result = 'on'
        else:
            self.logging_dict[str(ctx.guild.id)][setting] = False
            result = 'off'

        with open('logging.json', 'w') as f:
            json.dump(self.logging_dict, f, indent=4)

        await ctx.reply(f'{setting} is now turned {result}.')

    @settings.command(aliases=['alltrue'])
    @checks.check_admin_or_owner()
    async def allon(self, ctx):
        """Turns every log filter on"""
        if str(ctx.guild.id) not in list(self.logging_dict.keys()):
            raise commands.BadArgument("This guild does not have logging set up.")

        for x, y in self.logging_dict[str(ctx.guild.id)].items():
            if x != 'channel':
                self.logging_dict[str(ctx.guild.id)][x] = True

        with open('logging.json', 'w') as f:
            json.dump(self.logging_dict, f, indent=4)

        await ctx.reply('Enabled all log filters.')

    @settings.command(aliases=['allfalse'])
    @checks.check_admin_or_owner()
    async def alloff(self, ctx):
        """Turns every log filter on"""
        if str(ctx.guild.id) not in list(self.logging_dict.keys()):
            raise commands.BadArgument("This guild does not have logging set up.")

        for x, y in self.logging_dict[str(ctx.guild.id)].items():
            if x != 'channel':
                self.logging_dict[str(ctx.guild.id)][x] = False

        with open('logging.json', 'w') as f:
            json.dump(self.logging_dict, f, indent=4)

        await ctx.reply('Disabled all log filters.')

    @logging.command(aliases=['start', 'make'])
    @checks.check_admin_or_owner()
    async def create(self, ctx, logging_channel: discord.TextChannel):
        """Initialize logging"""
        if str(ctx.guild.id) in list(self.logging_dict.keys()):
            raise commands.BadArgument("This guild already has logging set up.")

        self.logging_dict[str(ctx.guild.id)] = {
            "channel": logging_channel.id,
            "message_delete": True,
            "message_edit": True,
            "reaction_add": False,
            "reaction_remove": False,
            "reaction_clear": True,
            "channel_delete": True,
            "channel_create": True,
            "channel_edit": True,
            "channel_pin": False,
            "channel_webhook": False,
            "guild_integration": False,
            "member_join": True,
            "member_leave": True,
            "member_edit": False,
            "member_ban": True,
            "member_unban": True,
            "role_create": True,
            "role_delete": True,
            "role_edit": True,
            "emoji_edit": False,
            "invite_create": False,
            "invite_delete": False
        }

        with open('logging.json', 'w') as f:
            json.dump(self.logging_dict, f, indent=4)

        await ctx.reply(f'Initiated logging in {logging_channel.mention}.')

    @logging.command(aliases=['quit', 'cancel', 'quit', 'stop'])
    @checks.check_admin_or_owner()
    async def close(self, ctx):
        """Stop logging"""
        if str(ctx.guild.id) not in list(self.logging_dict.keys()):
            raise commands.BadArgument("This guild does not have logging set up.")

        self.logging_dict.pop(str(ctx.guild.id))

        with open('logging.json', 'w') as f:
            json.dump(self.logging_dict, f, indent=4)

        await ctx.reply(f'Stopped logging.')


def setup(bot):
    bot.add_cog(loggingCog(bot))
