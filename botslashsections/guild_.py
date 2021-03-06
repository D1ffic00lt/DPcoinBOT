import discord

from discord.ext import commands
from discord.utils import get
from dislash import slash_command, Option, OptionType
from typing import Union

from botsections.texts import need_settings
from database.db import Database
from botsections.helperfunction import divide_the_number, logging


class GuildSlash(commands.Cog, Database, name='guild module'):
    @logging
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__("server.db")
        self.bot = bot
        self.found: bool
        self.admin: Union[discord.TextChannel, int]
        self.casino_channel: Union[discord.TextChannel, int]
        self.role: Union[discord.Role, int]
        self.auto: int
        self.category: Union[discord.CategoryChannel, int]
        self.emb: discord.Embed

        print("Guild Slash connected")

    @slash_command(
        name="auto_setup", description="авто-настройка каналов бота на сервере",
    )
    async def __cat_create_slash(self, ctx: commands.context.Context) -> None:
        if ctx.author.guild_permissions.administrator or ctx.author.id == 401555829620211723:
            guild = ctx.message.guild
            if self.checking_for_guild_existence_in_table(ctx.guild.id):
                self.admin, self.casino_channel, self.role, self.auto, self.category = self.get_guild_settings(
                    ctx.guild.id
                )
                self.admin = self.bot.get_channel(self.admin)
                self.casino_channel = self.bot.get_channel(self.casino_channel)
                self.role = get(guild.roles, id=self.role)
                if self.casino_channel is not None:
                    await self.casino_channel.delete()
                if self.admin is not None:
                    await self.admin.delete()
                if self.role is not None:
                    await self.role.delete()
                if self.auto == 1:
                    self.found = False
                    for category in guild.categories:
                        if category.id == self.category:
                            self.category = category
                            self.found = True
                            break
                    if self.found:
                        await self.category.delete()

            self.category = await guild.create_category("DPcoinBOT")
            self.casino_channel = await guild.create_text_channel(name=f'Casino', category=self.category)
            self.admin = await guild.create_text_channel(name=f'shop_list', category=self.category)
            self.role = await guild.create_role(name="Coin Manager", colour=discord.Colour.from_rgb(255, 228, 0))
            self.delete_from_server(ctx.guild.id)
            self.insert_into_server(ctx.guild.id, self.role.id, self.admin.id, self.casino_channel.id, self.category.id)
            await self.admin.set_permissions(guild.default_role, read_messages=False, send_messages=False)
            self.emb = discord.Embed(title="Канал для казино")
            self.emb.add_field(
                name=f'Развлекайтесь!',
                value='Да будет анархия!',
                inline=False)
            await self.casino_channel.send(embed=self.emb)
            self.emb = discord.Embed(title="Канал для заказов")
            self.emb.add_field(
                name=f'Настройте его, пожалуйста🥺',
                value='Разрешите каким-то холопам просматривать этот канал, если конечно же хотите:D',
                inline=False)
            await self.admin.send(embed=self.emb)
            self.emb = discord.Embed(title="Категория создана")
            self.emb.add_field(
                name=f'Требуется дополнительная настройка!',
                value=need_settings.format(self.casino_channel.mention, self.admin.mention, self.role.mention),
                inline=False)
            await ctx.send(embed=self.emb)

    @slash_command(
        name="start_money", description="стартовый баланс",
        options=[
            Option("arg", "аргумент (set)", OptionType.STRING, required=False),
            Option("cash", "число, на которое Вы ставите", OptionType.INTEGER, required=False)
        ]
    )
    async def __start_money_slash(self, ctx: commands.context.Context, arg: str = None, cash: int = None) -> None:
        if ctx.author.guild_permissions.administrator or ctx.author.id == 401555829620211723:
            if arg == "set":
                if await self.cash_check(ctx, cash, max_cash=1000000) or cash == 0:
                    if not self.checking_for_guild_existence_in_table(ctx.guild.id):
                        await ctx.send(
                            f"{ctx.author.mention}, сервер ещё не настроен! "
                            f"Сперва проведите настройку сервера!(auto_setup)"
                        )
                    else:
                        self.set_start_cash(cash, ctx.guild.id)
                        await ctx.message.add_reaction('✅')
            elif arg is None:
                if not self.checking_for_guild_existence_in_table(ctx.guild.id):
                    await ctx.send(
                        f"{ctx.author.mention}, сервер ещё не настроен! "
                        f"Сперва проведите настройку сервера!(auto_setup)"
                    )
                else:
                    await ctx.send(
                        f"На данный момент при входе дают "
                        f"**{divide_the_number(self.get_start_cash(ctx.guild.id))}** DP коинов"
                    )
