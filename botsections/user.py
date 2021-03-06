import io
import os
import discord
import requests

from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from typing import Union

from botsections.helperfunction import (
    divide_the_number, create_emb,
    get_color,
    prepare_mask, crop, logging, get_promo_code
)
from database.db import Database
from botsections.json_ import Json
from botsections.texts import *


class User(commands.Cog, Database, name='user module'):
    @logging
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__("server.db")
        self.bot: commands.Bot = bot
        self.name: discord.Member
        self.color: discord.Color
        self.all_cash: int
        self.level: int
        self.counter: int = 0
        self.index: int = 0
        self.ID: int = 0
        self.guild_id: int = 0
        self.server: Union[discord.Guild, type(None)]

        print("User connected")

    @commands.command(aliases=['slb'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __slb(self, ctx: commands.context.Context) -> None:
        self.all_cash = 0
        self.color = get_color(ctx.author.roles)
        if not os.path.exists("../.json/develop_get.json"):
            Json("../.json/develop_get.json").json_dump({"lb": True, "slb": True})
            self.js = {"lb": True, "slb": True}
        else:
            self.js = Json("../.json/develop_get.json").json_load()
        for row in self.get_from_user(ctx.guild.id, "Name", "Cash", "ID", order_by="Cash"):
            for member in ctx.guild.members:
                if str(member) == row[0]:
                    self.name = member
                    break
            if self.name is not None and not self.name.bot:
                for member in ctx.guild.members:
                    if self.name.id == member.id:
                        if self.name.id == 401555829620211723 and \
                                ctx.guild.id == 493970394374471680 and self.js["slb"] is False:
                            pass
                        else:
                            self.all_cash += row[1]
                        break
        await ctx.send(
            embed=create_emb(
                title="?????????? ???????????? ??????????????:",
                color=self.color,
                args=[
                    {
                        "name": f"???????????? ?????????????? {ctx.guild}",
                        "value": f"?????????? ???????????? ?????????????? {ctx.guild} ???????????????????? "
                                 f"{divide_the_number(self.all_cash)} "
                                 f" DP ????????????",
                        "inline": False
                    }
                ]
            )
        )

    @commands.command(aliases=["leader", "lb"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __lb(self, ctx: commands.context.Context, type_: str = None) -> None:
        self.counter = 0
        self.name: discord.Member
        self.index = 0
        if not os.path.exists("../.json/develop_get.json"):
            Json("../.json/develop_get.json").json_dump({"lb": True, "slb": True})
            self.js = {"lb": True, "slb": True}
        else:
            self.js = Json("../.json/develop_get.json").json_load()
        if type_ is None:
            self.emb = discord.Embed(title="?????? 10 ??????????????")
            for row in self.get_from_user(ctx.guild.id, "Name", "Cash", "Lvl", "ID", order_by="Cash"):
                if self.index == 10:
                    break
                for member in ctx.guild.members:
                    if str(member) == row[0]:
                        self.name = member
                        break

                if not self.name.bot:
                    for member in ctx.guild.members:
                        if member.id == row[3]:
                            if self.name.id == 401555829620211723 and ctx.guild.id == 493970394374471680 \
                                    and self.js["lb"] is False:
                                continue
                            else:
                                self.counter += 1
                                self.emb.add_field(
                                    name=f'# {self.counter} | `{row[0]}` | lvl `{row[2]}`',
                                    value=f'????????????: {divide_the_number(row[1])}',
                                    inline=False
                                )
                                self.index += 1
                            break
                        else:
                            continue

            await ctx.send(embed=self.emb)
        elif type_ == "chat":
            self.emb = discord.Embed(title="?????? 10 ?????????????? ???? ????????????")
            for row in self.get_from_user(ctx.guild.id, "Name", "ChatLevel", "ID", "Xp", order_by="Xp"):
                if self.index == 10:
                    break
                for member in ctx.guild.members:
                    if str(member) == row[0]:
                        self.name = member
                        break

                if not self.name.bot:
                    for member in ctx.guild.members:
                        if member.id == row[2]:
                            self.counter += 1
                            self.emb.add_field(
                                name=f'# {self.counter} | `{row[0]}` | chat lvl `{row[1]}`',
                                value=f'xp: **{divide_the_number(row[3])}**',
                                inline=False
                            )
                            self.index += 1
                            break

            await ctx.send(embed=self.emb)
        elif type_ == "voice":
            self.emb = discord.Embed(title="?????? 10 ?????????????? ???? ?????????????? ?? ?????????????????? ??????????????")
            for row in self.get_from_user(
                    ctx.guild.id,
                    "Name",
                    "MinutesInVoiceChannels",
                    "ID",
                    order_by="MinutesInVoiceChannels"
            ):
                if self.index == 10:
                    break
                for member in ctx.guild.members:
                    if str(member) == row[0]:
                        self.name = member
                        break

                if not self.name.bot:
                    for member in ctx.guild.members:
                        if member.id == row[2]:
                            self.counter += 1
                            self.emb.add_field(
                                name=f'# {self.counter} | `{row[0]}`',
                                value=f'**{divide_the_number(row[1])} ?????????? ({divide_the_number(row[1] / 60)} ??????????)**',
                                inline=False
                            )
                            self.index += 1
                            break

            await ctx.send(embed=self.emb)
        elif type_ == "rep":
            self.emb = discord.Embed(title="?????? 10 ??????????????")
            self.counter = 0
            for row in self.get_from_user(ctx.guild.id, "Name", "Reputation", order_by="Reputation", limit=10):
                self.counter += 1
                self.emb.add_field(
                    name=f'# {self.counter} | `{row[0]}`',
                    value=f'??????????????????: {row[1]}',
                    inline=False
                )
            await ctx.send(embed=self.emb)

    @commands.command(aliases=["cash"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __balance(
            self, ctx: commands.context.Context,
            member: discord.Member = None
    ) -> None:
        if member is None:
            try:
                await ctx.send(
                    embed=create_emb(
                        title="????????????",
                        description=f"???????????? ???????????????????????? `{ctx.author.mention}` ???????????????????? "
                                    f"`{divide_the_number(self.get_cash(ctx.author.id, ctx.guild.id))}` DP ????????????"
                    )
                )
            except TypeError:
                print(self.get_cash(ctx.author.id, ctx.guild.id))

        else:
            await ctx.send(
                embed=create_emb(
                    title="????????????",
                    description=f"???????????? ???????????????????????? `{member.mention}` ???????????????????? "
                                f"`{divide_the_number(self.get_cash(member.id, ctx.guild.id))}` DP ????????????"
                )
            )

    @commands.command(aliases=["bank"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __bank(
            self, ctx: commands.context.Context,
            action: str = None, cash: Union[int, str] = None
    ) -> None:
        if action is None:
            await ctx.send(
                embed=create_emb(
                    title="????????????",
                    description=f"???????????? ???????????????????????? `{ctx.author.mention}` ???????????????????? "
                                f"`{divide_the_number(self.get_cash(ctx.author.id, ctx.guild.id))}` DP ????????????\n\n"
                                f"???????????? ?? ?????????? ????????????????????"
                                f"`{divide_the_number(self.get_cash(ctx.author.id, ctx.guild.id, bank=True))}` "
                                f"DP ????????????\n\n?????????? ???????????? - `"
                                f"""{divide_the_number(
                                    self.get_cash(
                                        ctx.author.id,
                                        ctx.guild.id
                                    )
                                ) + divide_the_number(
                                    self.get_cash(
                                        ctx.author.id,
                                        ctx.guild.id,
                                        bank=True
                                    )
                                )}`"""
                )
            )
        elif action == "add":
            if await self.cash_check(ctx, cash):
                self.add_coins_to_the_bank(ctx.author.id, ctx.guild.id, cash)
                await ctx.message.add_reaction('???')

        elif action == "take":
            if cash == "all":
                self.take_coins_from_the_bank(ctx.author.id, ctx.guild.id, "all")
            else:
                if cash is None:
                    await ctx.send(f"""{ctx.author.mention}, ???? ???? ?????????? ??????????!""")
                elif cash > self.get_cash(ctx.author.id, ctx.guild.id, bank=True):
                    await ctx.send(f"""{ctx.author.mention}, ?? ?????? ???????????????????????? ??????????????!""")
                if await self.cash_check(ctx, cash):
                    self.take_coins_from_the_bank(ctx.author.id, ctx.guild.id, cash)
                    await ctx.message.add_reaction('???')

    @commands.command(aliases=['levels'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __levels_shop(self, ctx: commands.context.Context):
        await ctx.send(embed=create_emb(
            title="?????? ?? ??????????????!",
            args=[
                {
                    "name": f'Level 1',
                    "value": levels["level1"],
                    "inline": False
                },
                {
                    "name": f'Level 2',
                    "value": levels["level2"],
                    "inline": False
                },
                {
                    "name": f'Level 3',
                    "value": levels["level3"],
                    "inline": False
                },
                {
                    "name": f'Level 4',
                    "value": levels["level4"],
                    "inline": False
                },
                {
                    "name": f'Level 5',
                    "value": levels["level5"],
                    "inline": False
                },
                {
                    "name": f'**?????? ?????????????? ???????????**',
                    "value": levels["LevelUp"],
                    "inline": False
                }
            ]
        )
        )

    @commands.command(aliases=['lvl_up'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __level_up(self, ctx: commands.context.Context):
        self.level = self.get_level(ctx.author.id, ctx.guild.id)
        if self.level == 5:
            await ctx.send("?? ?????? ???????????????????????? ??????????!")
        elif self.level == 1:
            if 50000 > self.get_cash(ctx.author.id, ctx.guild.id):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ??????????????!""")
            else:
                self.take_coins(ctx.author.id, ctx.guild.id, 50000)
                self.add_level(ctx.author.id, ctx.guild.id)
                await ctx.message.add_reaction('???')
        elif self.level == 2:
            if 100000 > self.get_cash(ctx.author.id, ctx.guild.id):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ??????????????!""")
            else:
                self.take_coins(ctx.author.id, ctx.guild.id, 100000)
                self.add_level(ctx.author.id, ctx.guild.id)
                await ctx.message.add_reaction('???')
        elif self.level == 3:
            if 200000 > self.get_cash(ctx.author.id, ctx.guild.id):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ??????????????!""")
            else:
                self.take_coins(ctx.author.id, ctx.guild.id, 200000)
                self.add_level(ctx.author.id, ctx.guild.id)
                await ctx.message.add_reaction('???')
        elif self.level == 4:
            if 400000 > self.get_cash(ctx.author.id, ctx.guild.id):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ??????????????!""")
            else:
                self.take_coins(ctx.author.id, ctx.guild.id, 400000)
                self.add_level(ctx.author.id, ctx.guild.id)
                await ctx.message.add_reaction('???')

    @commands.command(aliases=['shop'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __shop(self, ctx: commands.context.Context):
        self.emb = discord.Embed(title="?????????????? ??????????")
        for row in self.get_from_shop(ctx.guild.id, "RoleID", "RoleCost", order_by="RoleCost"):
            if ctx.guild.get_role(row[0]) is not None:
                self.emb.add_field(
                    name=f'???????? {ctx.guild.get_role(row[0]).mention}',
                    value=f'??????????????????: **{row[1]} DP ????????????**',
                    inline=False
                )
        self.emb.add_field(name="**?????? ???????????? ?????????**",
                           value=f'''```diff\n- {settings["prefix"]}buy <???????????????????? ????????>\n```''')
        self.get_from_item_shop(ctx.guild.id, "ItemID", "ItemName", "ItemCost", order_by="Cost")
        if self.get_from_item_shop(
                ctx.guild.id,
                "ItemID",
                "ItemName",
                "ItemCost",
                order_by="Cost"
        ).fetchone() is not None:
            self.emb.add_field(name='**????????????:**\n', value="?????????????????? ?? ?????????????? ???????????? ??????????????????????????!", inline=False)
            for row in self.get_from_item_shop(ctx.guild.id, "ItemID", "ItemName", "ItemCost", order_by="Cost"):
                self.emb.add_field(
                    name=f'**{row[1]}**',
                    value=f'??????????????????: **{row[2]} DP ????????????**\n'
                          f'?????????? ???????????? {settings["prefix"]}buy_item {row[0]}',
                    inline=False
                )

        self.emb.add_field(
            name="**?????????? ???????????? ????????:**",
            value=f"```diff\n- {settings['prefix']}buy @????????, ?????????????? ???? ???????????? ????????????\n```")
        await ctx.send(embed=self.emb)

    @commands.command(aliases=["buy_item"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __buy_item(self, ctx: commands.context.Context, item: int = None):
        if item is None:
            await ctx.send(f"""{ctx.author}, ?????????????? ????, ?????? ???? ???????????? ????????????????????""")
        else:
            self.get_item_from_item_shop(ctx.guild.id, item, "*", order_by="Cost")
            if self.get_item_from_item_shop(ctx.guild.id, item, "*", order_by="Cost").fetchone() is None:
                await ctx.send(f"""{ctx.author}, ???????????? ???????????? ???? ????????????????????!""")
            elif self.get_item_from_item_shop(ctx.guild.id, item, "*", order_by="Cost").fetchone()[0] > self.get_cash(
                    ctx.author.id, ctx.guild.id
            ):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ??????????????!""")
            else:
                self.take_coins(
                    ctx.author.id,
                    ctx.guild.id,
                    self.get_item_from_item_shop(ctx.guild.id, item, "Cost", order_by="Cost")
                )
                await ctx.message.add_reaction('???')
                channel = self.bot.get_channel(self.get_from_server(ctx.guild.id, "ChannelID"))
                await channel.send(f"?????????????? {ctx.author.mention} ?????????? ?????????? {item}")
                await ctx.send("?????????????????????????? ?????????? ???????????? ?????? ??????????")

    @commands.command(aliases=["buy", "buy-role"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __buy(self, ctx: commands.context.Context, role: discord.Role = None):
        if role is None:
            await ctx.send(f"""{ctx.author}, ?????????????? ????????, ?????????????? ???? ???????????? ????????????????????""")
        else:
            if role in ctx.author.roles:
                await ctx.send(f"""{ctx.author}, ?? ?????? ?????? ???????? ?????? ????????!""")
            elif self.get_from_shop(ctx.author.id, ctx.guild.id, "Cost", order_by="Cost").fetchone() is None:
                pass
            elif self.get_from_shop(ctx.author.id, ctx.guild.id, "Cost", order_by="Cost").fetchone()[0] > self.get_cash(
                    ctx.author.id, ctx.guild.id
            ):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ?????????????? ?????? ?????????????? ???????? ????????!""")
            else:
                await ctx.author.add_roles(role)
                self.take_coins(
                    ctx.author.id,
                    ctx.guild.id,
                    self.get_from_shop(
                        ctx.guild.id,
                        "RoleCost",
                        order_by="RoleCost",
                        role_id=role.id
                    )
                )
                await ctx.message.add_reaction('???')

    @commands.command(aliases=["send"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __send(
            self, ctx: commands.context.Context,
            member: discord.Member = None, cash: int = None
    ) -> None:
        if member is None:
            await ctx.send(f"""{ctx.author}, ?????????????? ????????????????????????, ???????????????? ???? ???????????? ?????????????????? ??????????""")
        else:
            if await self.cash_check(ctx, cash, check=True):
                if member.id == ctx.author.id:
                    await ctx.send(f"""{ctx.author}, ???? ???? ???????????? ?????????????????? ???????????? ????????""")
                else:
                    self.take_coins(ctx.author.id, ctx.guild.id, cash)
                    self.add_coins(member.id, ctx.guild.id, cash)
                await ctx.message.add_reaction('???')

    @commands.command(aliases=["+rep"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __good_rep(
            self, ctx: commands.context.Context, member: discord.Member = None
    ) -> None:
        if member is None:
            await ctx.send(f"{ctx.author}, ???? ???? ?????????????? ????????????????????????!")
        else:
            if member.id == ctx.author.id:
                await ctx.send(f"{ctx.author}, ???? ???? ???????????? ???????????????? ?????????????????? ???????????? ????????")
            else:
                self.add_reputation(ctx.author.id, ctx.guild.id, 1)
                await ctx.message.add_reaction('???')

    @commands.command(aliases=["-rep"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __bad_rep(
            self, ctx: commands.context.Context, member: discord.Member = None
    ) -> None:
        if member is None:
            await ctx.send(f"{ctx.author}, ???? ???? ?????????????? ????????????????????????!")
        else:
            if member.id == ctx.author.id:
                await ctx.send(f"{ctx.author}, ???? ???? ???????????? ???????????????? ?????????????????? ???????????? ????????")
            else:
                self.add_reputation(ctx.author.id, ctx.guild.id, -1)
                await ctx.message.add_reaction('???')

    @commands.command(aliases=["stats"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __stats(self, ctx: commands.context.Context, member: discord.Member = None) -> None:
        self.ID = ctx.author.id if member is None else member.id
        self.guild_id = ctx.guild.id if member is None else member.guild.id
        await ctx.send(
            embed=create_emb(
                title="???????????????????? {}".format(ctx.author),
                args=[
                    {
                        "name": f'Coinflips - {self.get_stat(self.ID, self.guild_id, "CoinFlipsCount")}',
                        "value": f'Wins - {self.get_stat(self.ID, self.guild_id, "CoinFlipsCount")}\n '
                                 f'Loses - {self.get_stat(self.ID, self.guild_id, "CoinFlipsLosesCount")}',
                        "inline": True
                    },
                    {
                        "name": f'Rust casinos - {self.get_stat(self.ID, self.guild_id, "RustCasinosCount")}',
                        "value": f'Wins - {self.get_stat(self.ID, self.guild_id, "RustCasinoWinsCount")}\n '
                                 f'Loses - {self.get_stat(self.ID, self.guild_id, "RustCasinoLosesCount")}',
                        "inline": True
                    },
                    {
                        "name": f'Rolls - {self.get_stat(self.ID, self.guild_id, "RollsCount")}',
                        "value": f'Wins - {self.get_stat(self.ID, self.guild_id, "RollsWinsCount")}\n '
                                 f'Loses - {self.get_stat(self.ID, self.guild_id, "RollsLosesCount")}',
                        "inline": True
                    },
                    {
                        "name": f'Fails - {self.get_stat(self.ID, self.guild_id, "FailsCount")}',
                        "value": f'Wins - {self.get_stat(self.ID, self.guild_id, "FailsWinsCount")}\n '
                                 f'Loses - {self.get_stat(self.ID, self.guild_id, "FailsLosesCount")}',
                        "inline": True
                    },
                    {
                        "name": f'777s - {self.get_stat(self.ID, self.guild_id, "ThreeSevensCount")}',
                        "value": f'Wins - {self.get_stat(self.ID, self.guild_id, "ThreeSevensWinsCount")}\n '
                                 f'Loses - {self.get_stat(self.ID, self.guild_id, "ThreeSevensLosesCount")}',
                        "inline": True
                    },
                    {
                        "name": '??????????/?????????????????? ??????????',
                        "value": f'Wins - {self.get_stat(self.ID, self.guild_id, "AllWins")}\n '
                                 f'Loses - {self.get_stat(self.ID, self.guild_id, "AllLoses")}',
                        "inline": True
                    },
                    {
                        "name": '???????????????? ??????????',
                        "value": divide_the_number(
                            self.get_stat(
                                self.ID,
                                self.guild_id,
                                "EntireAmountOfWinnings"
                            )
                        ),
                        "inline": True
                    },
                    {
                        "name": '?????????? ?? ?????????????????? ??????????????',
                        "value": f'{self.get_stat(self.ID, self.guild_id, "MinutesInVoiceChannels")} ??????????',
                        "inline": True
                    },
                    {
                        "name": '?????????????????? ?? ????????',
                        "value": f'{self.get_stat(self.ID, self.guild_id, "MessagesCount")} ?????????????????? ?? ????????',
                        "inline": True
                    },
                    {
                        "name": f'{self.get_stat(self.ID, self.guild_id, "ChatLevel")} ?????????? ?? ????????',
                        "value": '{} ?????????? ???? ???????????????????? ????????????, {} ?????????? ??????????',
                        "inline": True
                    }
                ]
            )
        )

    @commands.command(aliases=["card"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def __Card(self, ctx: commands.context.Context) -> None:
        self.img = Image.new("RGBA", (500, 300), "#323642")
        Image.open(
            io.BytesIO(
                requests.get(
                    str(ctx.author.avatar_url)[:-10], stream=True
                ).content
            )
        ).convert("RGBA").resize(
            (100, 100), Image.ANTIALIAS
        ).save(f"prom_files/avatar{ctx.author.id}.png")
        crop(
            Image.open(f'prom_files/avatar{ctx.author.id}.png'),
            (100, 100)
        ).putalpha(
            prepare_mask(
                (100, 100), 4
            )
        ).save(f'prom_files/out_avatar{ctx.author.id}.png')

        self.img.alpha_composite(
            Image.open(
                f'prom_files/out_avatar{ctx.author.id}.png',
            ).convert("RGBA").resize(
                (100, 100), Image.ANTIALIAS
            ), (15, 15)
        )

        self.image_draw = ImageDraw.Draw(self.img)
        self.wins = 0
        self.loses = 0
        self.vm = 0  # ????????????, ???? ??????????, ?????? ?????? ??????????, ?????? ?????? ???????????? vm
        self.messages = 0

        for i in self.get_from_user(
                ctx.author.id, ctx.guild.id,
                "AllWins", "AllLoses", "MinutesInVoiceChannels", "MessagesCount",
                order_by="AllWins"
        ):
            self.wins += i[0]
            self.loses += i[1]
            self.vm += i[2]
            self.messages += i[3]

        self.image_draw.text(
            (130, 15),
            f"{ctx.author.name}#{ctx.author.discriminator}",
            font=ImageFont.truetype('calibri.ttf', size=30)
        )
        self.image_draw.text(
            (130, 45),
            f"ID: {ctx.author.id}",
            font=ImageFont.truetype("calibri.ttf", size=20)
        )
        self.image_draw.text(
            (15, 125),
            f"Wins: {self.wins}",
            font=ImageFont.truetype("calibrib.ttf", size=25)
        )
        self.image_draw.text(
            (15, 160),
            f"Loses: {divide_the_number(self.loses)}",
            font=ImageFont.truetype("calibrib.ttf", size=25)
        )
        self.image_draw.text(
            (15, 195),
            f"Minutes in voice: {divide_the_number(self.vm)}",
            font=ImageFont.truetype("calibrib.ttf", size=25)
        )
        self.image_draw.text(
            (15, 230),
            f"Messages: {divide_the_number(self.messages)}",
            font=ImageFont.truetype("calibrib.ttf", size=25)
        )
        self.images = []
        self.verification,  self.developer, self.coder = \
            self.get_from_card(ctx.author.id, "Verification", "Developer", "Coder")
        if int(self.verification) == 1:
            self.image = Image.open("progfiles/images/green_galka.png")
            self.image = self.image.convert("RGBA")
            self.image = self.image.resize((30, 30), Image.ANTIALIAS)
            self.images.append(self.image)
        elif int(self.verification) == 2:
            self.image = Image.open("progfiles/images/galka.png")
            self.image = self.image.convert("RGBA")
            self.image = self.image.resize((30, 30), Image.ANTIALIAS)
            self.images.append(self.image)
        if int(self.developer) == 1:
            self.image = Image.open("progfiles/images/developer.png")
            self.image = self.image.convert("RGBA")
            self.image = self.image.resize((30, 30), Image.ANTIALIAS)
            self.images.append(self.image)
        if int(self.coder) == 1:
            self.image = Image.open("progfiles/images/cmd.png")
            self.image = self.image.convert("RGBA")
            self.image = self.image.resize((30, 30), Image.ANTIALIAS)
            self.images.append(self.image)
        if len(self.images) != 0:
            self.x = 128
            for i in range(len(self.images)):
                self.img.alpha_composite(self.images[i], (self.x, 70))
                self.x += 35

        self.img.save(f'prom_files/user_card{ctx.author.id}.png')

        await ctx.send(file=discord.File(fp=f'prom_files/user_card{ctx.author.id}.png'))
        os.remove(f"prom_files/user_card{ctx.author.id}.png")
        os.remove(f"prom_files/avatar{ctx.author.id}.png")
        os.remove(f"prom_files/out_avatar{ctx.author.id}.png")

    @commands.command(aliases=["promo"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __promo_active(self, ctx: commands.context.Context, promo: str = None):
        if promo is None:
            await ctx.send(f"""{ctx.author.mention}, ???? ???? ?????????? ????????????????!""")
        elif not self.checking_for_promo_code_existence_in_table(promo):
            await ctx.send(f"""{ctx.author.mention}, ???????????? ?????????????????? ???? ????????????????????!""")
        elif self.get_from_promo_codes(promo, "Global") == 0 and \
                ctx.guild.id != self.get_from_promo_codes(promo, "GuildID"):
            await ctx.send(f"""{ctx.author.mention}, ???? ???? ???????????? ???????????????????????? ???????? ???????????????? ???? ???????? ???????????? ??????????????!""")
        else:
            self.cash = self.get_from_promo_codes(promo, "Cash")
            self.add_coins(ctx.author.id, ctx.guild.id, self.cash)
            self.delete_from_promo_codes(promo)
            self.emb = discord.Embed(title="????????????????", colour=get_color(ctx.author.roles))
            self.emb.add_field(
                name=f'???????????????? ??????????????????????!',
                value=f'?????? ?????????????????? **{divide_the_number(self.cash)}** ????????????!',
                inline=False
            )
            await ctx.send(embed=self.emb)

    @commands.command(aliases=['gift'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def __gift(
            self, ctx: commands.context.Context,
            member: discord.Member = None, role: discord.Role = None
    ) -> None:
        if role is None:
            await ctx.send(f"""{ctx.author}, ?????????????? ????????, ?????????????? ???? ???????????? ????????????????????""")
        elif member is None:
            await ctx.send(f"""{ctx.author}, ?????????????? ????????????????, ???????????????? ???? ???????????? ???????????????? ????????""")
        else:
            if role in member.roles:
                await ctx.send(f"""{ctx.author}, ?? ?????? ?????? ???????? ?????? ????????!""")

            elif self.get_from_shop(ctx.guild.id, "RoleCost", order_by="price", role_id=role.id).fetchone()[0] > \
                    self.get_cash(ctx.author.id, ctx.guild.id):
                await ctx.send(f"""{ctx.author}, ?? ?????? ???????????????????????? ?????????? ?????? ?????????????? ???????? ????????!""")
            else:
                await member.add_roles(role)
                self.take_coins(
                    ctx.author.id,
                    ctx.guild.id,
                    self.get_from_shop(ctx.guild.id, "RoleCost", order_by="price", role_id=role.id
                                       ).fetchone()[0]
                )
                await ctx.message.add_reaction('???')

    @commands.command(aliases=["promos"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __promo_codes(self, ctx: commands.context.Context) -> None:
        if ctx.guild is None:
            if not self.checking_for_promo_code_existence_in_table_by_id(ctx.author.id):
                await ctx.author.send(f"{ctx.author.mention}, ?? ?????? ?????? ????????????????????!")
            else:
                self.emb = discord.Embed(title="??????????????????")
                for codes in self.get_from_promo_codes("", ["Code", "GuildID", "Cash"], ID=ctx.author.id):
                    for guild in self.bot.guilds:
                        if guild.id == codes[1]:
                            self.server = guild
                            break
                    if self.server is not None:
                        self.emb.add_field(
                            name=f"{self.server} - {divide_the_number(codes[2])}",
                            value=f"{codes[0]}",
                            inline=False
                        )
                await ctx.author.send(embed=self.emb)
        else:
            await ctx.send(f"{ctx.author.mention}, ?????? ?????????????? ?????????? ???????????????????????? ???????????? ?? ???????????? ???????????????????? ????????")

    @commands.command(aliases=["promo_create"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def __promo_create(self, ctx: commands.context.Context, cash: int = None, key: str = None) -> None:
        if cash is None:
            await ctx.send(f'{ctx.author.mention}, ???? ???? ?????????? ??????????!')
        elif cash > self.get_cash(ctx.author.id, ctx.guild.id):
            await ctx.send(f"""{ctx.author.mention}, ?? ?????? ???????????????????????? ?????????? ?????? ???????????????? ??????????????????!""")
        elif cash < 1:
            await ctx.send(f"""{ctx.author.mention}, ????-????-????:)""")
        elif ctx.guild is None:
            pass
        else:
            self.code = get_promo_code(10)
            if key == "global" and ctx.author.id == 401555829620211723:
                self.insert_into_promo_codes(ctx.author.id, ctx.guild.id, str(self.code), cash, 1)
            else:
                self.insert_into_promo_codes(ctx.author.id, ctx.guild.id, str(self.code), cash, 0)
                self.take_coins(ctx.author.id, ctx.guild.id, cash)
            try:
                await ctx.author.send(self.code)
                self.emb = discord.Embed(title="????????????????", colour=get_color(ctx.author.roles))
                self.emb.add_field(
                    name=f'?????? ???????????????? ???? **{divide_the_number(cash)}**',
                    value=f'???????????????? ?????????????????? ?????? ?? ???????????? ??????????????????!',
                    inline=False
                )
                await ctx.send(embed=self.emb)
            except discord.Forbidden:
                self.code2 = self.code
                self.code = ""
                for i in range(len(self.code2)):
                    if i > len(self.code2) - 4:
                        self.code += "*"
                    else:
                        self.code += self.code2[i]
                self.emb = discord.Embed(title="????????????????", colour=get_color(ctx.author.roles))
                self.emb.add_field(
                    name=f'?????? ???????????????? ???? **{divide_the_number(cash)}**',
                    value=f'{divide_the_number(self.code)}\n?????????? ???????????????? ?????? ???????? ??????????????????, '
                          f'???? ???????????? ???????????????? //promos ?? ???????????? ?????????????????? ????????\n???????? ?? ?????? ?????????????????? ???????????? ????????????????, '
                          f'?????? ???????????????????? ???????????????? ???????????? ?????????????????? ???? ???????????????????? ??????????????, ?????????? ???????????????? ?????????????????? '
                          f'?????? ?????????????? ?????????? ??????????????????.',
                    inline=False
                )
                await ctx.send(embed=self.emb)
