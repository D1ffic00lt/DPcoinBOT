# -*- coding: utf-8 -*-
from __future__ import annotations

import sqlite3

from sqlite3 import Cursor
from typing import Tuple

from ..templates.helperfunction import *


class Database:
    def __init__(self, filename: str) -> None:
        self.time = None
        self.now2 = None
        self.minutes: int = 0
        self.day: int = 0
        self.month: int = 0
        self.prises: dict = {}
        self.valentine: dict = {}
        self.connection: sqlite3.Connection = sqlite3.connect(filename, check_same_thread=False)
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
            Name                         VARCHAR (255) NOT NULL,
            ID                           INT NOT NULL,
            Cash                         BIGINT DEFAULT 0 NOT NULL,
            Reputation                   INT DEFAULT 0 NOT NULL,
            Lvl                          INT DEFAULT 0 NOT NULL,
            GuildID                      INT NOT NULL,
            CoinFlipsCount               INT DEFAULT 0 NOT NULL,
            CoinFlipsWinsCount           INT DEFAULT 0 NOT NULL,
            CoinFlipsLosesCount          INT DEFAULT 0 NOT NULL,
            RustCasinos                  INT DEFAULT 0 NOT NULL, 
            RustCasinoWinsCount          INT DEFAULT 0 NOT NULL, 
            RustCasinoLoses              INT DEFAULT 0 NOT NULL,
            RollsCount                   INT DEFAULT 0 NOT NULL, 
            RollsWinsCount               INT DEFAULT 0 NOT NULL, 
            RollsLosesCount              INT DEFAULT 0 NOT NULL, 
            FailsCount                   INT DEFAULT 0 NOT NULL, 
            FailsWinsCount               INT DEFAULT 0 NOT NULL, 
            FailsLosesCount              INT DEFAULT 0 NOT NULL,
            ThreeSevensCount             INT DEFAULT 0 NOT NULL, 
            ThreeSevensWinsCount         INT DEFAULT 0 NOT NULL, 
            ThreeSevensLosesCount        INT DEFAULT 0 NOT NULL,
            AllWins                      INT DEFAULT 0 NOT NULL,
            AllLoses                     INT DEFAULT 0 NOT NULL,
            EntireAmountOfWinnings       BIGINT DEFAULT 0 NOT NULL,
            MinutesInVoiceChannels       INT DEFAULT 0 NOT NULL,
            Xp BIGINT                    DEFAULT 0 NOT NULL,
            ChatLevel                    INT DEFAULT 0 NOT NULL,
            MessagesCount                INT DEFAULT 0 NOT NULL,
            CashInBank BIGINT            DEFAULT 0 NOT NULL 
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Shop (
            RoleId                       INT NOT NULL,
            GuildID                      INT NOT NULL,
            RoleCost                     BIGINT DEFAULT 0 NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Server (
            GuildID                      INT NOT NULL,
            AdministratorRoleID          INT NOT NULL,
            ChannelID                    INT NOT NULL,
            CasinoChannelID              INT NOT NULL,
            CategoryID                   INT NOT NULL,
            Auto                         BOOLEAN NOT NULL,
            StartingBalance              BIGINT DEFAULT 0 NOT NULL,
            BankInterest                 INT DEFAULT 0 NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ItemsShop (
            ItemID                       INT NOT NULL,
            ItemName                     VARCHAR (255) NOT NULL,
            GuildID                      INT NOT NULL,
            ItemCost                     BIGINT NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Online (
            ID                           INT NOT NULL,
            GuildID                      INT NOT NULL,
            Time                         VARCHAR (255) NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS OnlineStats (
            ID                           INT NOT NULL,
            GuildID                      INT NOT NULL,
            Time                         TIME NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CoinFlip (
            FirstPlayerID                INT NOT NULL,
            SecondPlayerID               INT NOT NULL,
            FirstPlayerName              VARCHAR (255) NOT NULL,
            SecondPlayerName             VARCHAR (255) NOT NULL,
            GuildID                      INT NOT NULL,
            GuildName                    VARCHAR (255) NOT NULL,
            Cash                         INT NOT NULL,
            Date                         VARCHAR (255) NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Guilds (
            ID                           INT NOT NULL,
            Name                         VARCHAR (255) NOT NULL,
            Members                      INT NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Levels (
           Level                         INT NOT NULL,
           XP                            BIGINT NOT NULL,
           Award                         INT NOT NULL
          )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Achievements (
           Name                         VARCHAR (255) NOT NULL,
           ID                           INT NOT NULL,
           GuildID                      INT NOT NULL,
           Voice_1                      BOOLEAN DEFAULT false NOT NULL,
           Voice_10                     BOOLEAN DEFAULT false NOT NULL,
           Voice_100                    BOOLEAN DEFAULT false NOT NULL,
           Voice_1000                   BOOLEAN DEFAULT false NOT NULL,
           Voice_10000                  BOOLEAN DEFAULT false NOT NULL,
           Voice_100000                 BOOLEAN DEFAULT false NOT NULL,
           Voice_1000000                BOOLEAN DEFAULT false NOT NULL,
           Voice_10000000               BOOLEAN DEFAULT false NOT NULL,
           Lose_3                       BOOLEAN DEFAULT false NOT NULL,
           Lose_10                      BOOLEAN DEFAULT false NOT NULL,
           Lose_20                      BOOLEAN DEFAULT false NOT NULL,
           Loses                        INT DEFAULT 0 NOT NULL,
           Wins_3                       BOOLEAN DEFAULT false NOT NULL,
           Wins_10                      BOOLEAN DEFAULT false NOT NULL,
           Wins_20                      BOOLEAN DEFAULT false NOT NULL,
           Wins                         INT DEFAULT 0 NOT NULL,
           DroppingZeroInFail           BOOLEAN DEFAULT false NOT NULL
          )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS NewYearEvent (
           Name                         VARCHAR (255) NOT NULL,
           ID                           INT NOT NULL,
           GuildID                      INT NOT NULL,
           MandarinsCount               INT DEFAULT 0 NOT NULL,
           OlivierSaladCount            INT DEFAULT 0 NOT NULL,
           CaesarSaladCount             INT DEFAULT 0 NOT NULL,
           RedСaviarCount               INT DEFAULT 0 NOT NULL,
           BlackСaviarCount             INT DEFAULT 0 NOT NULL,
           SlicedMeatCount              INT DEFAULT 0 NOT NULL,
           DucksCount                   INT DEFAULT 0 NOT NULL,
           SaltedRedFishsCount          INT DEFAULT 0 NOT NULL,
           DobryJuiceCount              INT DEFAULT 0 NOT NULL,
           BabyChampagneCount           INT DEFAULT 0 NOT NULL,
           moodCount                    INT DEFAULT 0 NOT NULL
          )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Inventory (
           Name                         VARCHAR (255) NOT NULL,
           ID                           INT NOT NULL,
           GuildID                      INT NOT NULL,
           NewYearPrises                INT DEFAULT 0 NOT NULL,
           Valentines                   INT DEFAULT 0 NOT NULL
           )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Card (
           ID                           INT NOT NULL,
           Verification                 INT DEFAULT 0 NOT NULL,
           Developer                    BOOLEAN DEFAULT false NOT NULL,
           Coder                        BOOLEAN DEFAULT false NOT NULL
           )""")
        self.connection.commit()

    @ignore_exceptions
    def checking_for_user_existence_in_table(self, ID: int, guild_id: int = 0) -> bool:
        if self.cursor.execute("SELECT `Name` FROM `Users` WHERE `ID` = ? AND `GuildID` = ?",
                               (ID, guild_id)).fetchone() is None:
            return False
        return True

    @ignore_exceptions
    def checking_for_guild_existence_in_table(self, guild_id: int) -> bool:
        if self.cursor.execute("SELECT * FROM `Server` WHERE `GuildID` = ?", (guild_id,)).fetchone() is None:
            return False
        return True

    @ignore_exceptions
    def checking_for_levels_existence_in_table(self) -> bool:
        if self.cursor.execute("SELECT * FROM `Levels` WHERE `Level` = 1").fetchone() is None:
            return False
        return True

    @ignore_exceptions
    def insert_into_users(
            self,
            name: str,
            ID: int,
            starting_balance: int,
            guild_id: int
    ) -> Cursor:
        with self.connection:
            return self.cursor.execute("INSERT INTO `Users` VALUES (?, ?, ?, 0, 1, ?)",
                                       (name, ID, starting_balance, guild_id))

    @ignore_exceptions
    def check_completion_dropping_zero_in_fail_achievement(self, ID: int, guild_id: int) -> bool:
        if self.cursor.execute("SELECT DroppingZeroInFail FROM Achievements WHERE ID = ? AND GuildID = ?",
                               (ID, guild_id)).fetchone()[0] == 0:
            return False
        return True

    @ignore_exceptions
    def complete_dropping_zero_in_fail_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                "UPDATE Achievements SET DroppingZeroInFail = true WHERE ID = ? AND GuildID = ?",
                (ID, guild_id)
            )

    @ignore_exceptions
    def insert_into_card(self, ID: int) -> Cursor:
        if self.cursor.execute("SELECT * FROM `Card` WHERE `ID` = ?", (ID,)).fetchone() is None:
            with self.connection:
                return self.cursor.execute("INSERT INTO `Card` VALUES (?)", (ID,))

    @ignore_exceptions
    def insert_into_achievements(self, name: str, ID: int, guild_id: int) -> Cursor:
        if self.cursor.execute("SELECT * FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                               (ID, guild_id)).fetchone() is None:
            with self.connection:
                return self.cursor.execute(f"INSERT INTO `Achievements` VALUES (?, ?, ?)", (name, ID, guild_id))

    @ignore_exceptions
    def insert_into_inventory(self, name: str, ID: int, guild_id: int) -> Cursor:
        if self.cursor.execute("SELECT * FROM `Inventory` WHERE `ID` = ? AND `GuildID` = ?",
                               (ID, guild_id)).fetchone() is None:
            with self.connection:
                return self.cursor.execute(f"INSERT INTO `Inventory` VALUES (?, ?, ?)", (name, ID, guild_id))

    @ignore_exceptions
    def insert_into_new_year_event(self, name: str, ID: int, guild_id: int) -> Cursor:
        if self.cursor.execute("SELECT * FROM `NewYearEvent` WHERE `ID` = ? AND `GuildID` = ?",
                               (ID, guild_id)).fetchone() is None:
            with self.connection:
                return self.cursor.execute(f"INSERT INTO `NewYearEvent` VALUES (?, ?, ?)", (name, ID, guild_id))

    @ignore_exceptions
    def insert_into_levels(self, Level: int, xp: int, award: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("INSERT INTO `Levels` VALUES (?, ?, ?)", (Level, xp, award))

    @ignore_exceptions
    def get_start_cash(self, guild_id: int) -> int:
        return self.cursor.execute("SELECT `StartingBalance` FROM `Server` "
                                   "WHERE `GuildID` = ?", (guild_id,)).fetchone()[0]

    @ignore_exceptions
    def get_user_name(self, ID: int) -> str:
        return self.cursor.execute(f"SELECT `Name` FROM `Users` WHERE `ID` = ?", (ID,)).fetchone()[0]

    @ignore_exceptions
    def get_from_user(
            self,
            guild_id: int,
            *args: Tuple[str],
            order_by: str,
            limit: int = None
    ) -> Any:
        if limit is None:
            return self.cursor.execute(
                f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `Users` WHERE "
                f"`GuildID` = ? ORDER BY `{order_by}` DESC",
                (guild_id,)
            )
        else:
            return self.cursor.execute(
                f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `Users` WHERE "
                f"`GuildID` = ? ORDER BY `{order_by}` DESC LIMIT 10",
                (guild_id,)
            )

    @ignore_exceptions
    def get_from_shop(self, guild_id: int, *args: Tuple[str], order_by: str, role_id: int = None) -> Any:
        if role_id is None:
            return self.cursor.execute(
                f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `Shop` WHERE "
                f"`GuildID` = ? ORDER BY `{order_by}` ASC",
                (guild_id,)
            )
        else:
            return self.cursor.execute(
                f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `Shop` WHERE `GuildID` = ? AND RoleID = ?",
                (guild_id, role_id)
            ).fetchone()[0]

    @ignore_exceptions
    def get_from_item_shop(self, guild_id: int, *args: Tuple[str], order_by: str) -> Any:
        return self.cursor.execute(
            f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `ItemShop` "
            f"WHERE `GuildID` = ? ORDER BY `{order_by}` ASC",
            (guild_id,)
        )

    @ignore_exceptions
    def get_item_from_item_shop(
            self,
            guild_id: int,
            item_id: int,
            *args: Tuple[str],
            order_by: str
    ) -> Any:
        return self.cursor.execute(
            f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `ItemShop` "
            f"WHERE `GuildID` = ? AND ItemID = ? ORDER BY `{order_by}` ASC",
            (guild_id, item_id)
        )

    @ignore_exceptions
    def get_level(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute(
            "SELECT `Lvl` FROM `Users` WHERE ID = ? AND GuildID = ?",
            (ID, guild_id)
        ).fetchone()[0]

    @ignore_exceptions
    def get_from_server(self, guild_id: int, *args: Tuple[str]) -> Any:
        return self.cursor.execute(
            f"SELECT {', '.join([f'`{i}`' for i in args])} FROM `Server` WHERE `GuildID` = ?",
            (guild_id,)
        ).fetchall()

    @ignore_exceptions
    def get_users_count(self, unique: bool = False) -> int:
        return self.cursor.execute('SELECT COUNT(1) FROM `Users`').fetchone()[0] \
            if not unique else self.cursor.execute('SELECT COUNT(1) FROM `Card`').fetchone()[0]

    @ignore_exceptions
    def get_cash(self, ID: int, guild_id: int, bank: bool = False) -> int:
        return self.cursor.execute(f"SELECT `{'Cash' if not bank else 'CashInBank'}` FROM `Users` "
                                   f"WHERE `ID` = ? AND `GuildID` = ?", (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def update_name(self, name: str, ID: int) -> Cursor:
        with self.connection:
            return self.cursor.execute('UPDATE `Users` SET `Name` = ? WHERE `ID` = ?', (name, ID))

    @ignore_exceptions
    def update_card(self, ID: int, type_of_card: str, mode: int) -> Cursor:
        with self.connection:
            return self.cursor.execute('UPDATE `Card` SET `?` = ? WHERE `ID` =?', (type_of_card, mode, ID))

    @ignore_exceptions
    def check_user(self, ID) -> bool:
        if self.cursor.execute("SELECT * FROM `Users` WHERE `ID` = ?", (ID,)).fetchone() is None:
            return False
        return True

    @ignore_exceptions
    def clear_coinflip(self) -> Cursor:
        with self.connection:
            return self.cursor.execute('DELETE FROM `CoinFlip`')

    @ignore_exceptions
    def add_prises(self, prises: int, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                "UPDATE Inventory SET NewYearPrises = NewYearPrises + ? WHERE ID = ? AND GuildID = ?",
                (prises, ID, guild_id)
            )

    @ignore_exceptions
    def add_valentines(self, valentines: int, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                "UPDATE Inventory SET Valentines = Valentines + ? WHERE ID = ? AND GuildID = ?",
                (valentines, ID, guild_id)
            )

    @ignore_exceptions
    def server_add(self, Bot: commands.Bot) -> None:
        for guild in Bot.guilds:
            for member in guild.members:
                if not self.checking_for_user_existence_in_table(member.id, guild.id):
                    if not self.checking_for_guild_existence_in_table(guild.id):
                        start_cash = 0
                    else:
                        start_cash = self.get_start_cash(guild.id)
                    self.insert_into_users(str(member), member.id, start_cash, guild.id)
                self.insert_into_card(member.id)
                self.insert_into_achievements(str(member), member.id, guild.id)
                self.insert_into_inventory(str(member), member.id, guild.id)
                self.insert_into_new_year_event(str(member), member.id, guild.id)
                if self.get_user_name(member.id) != member:
                    self.update_name(str(member), member.id)

    @ignore_exceptions
    def voice_create_stats(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("INSERT INTO `OnlineStats` VALUES (?, ?, ?)", (ID, guild_id, get_time()))

    @ignore_exceptions
    def voice_create(self, ID: int, guild_id: int, voice_create_stats: bool = False) -> Cursor:
        if voice_create_stats:
            self.voice_create_stats(ID, guild_id)
        with self.connection:
            return self.cursor.execute("INSERT INTO `Online` VALUES (?, ?, ?)", (ID, guild_id, get_time()))

    @ignore_exceptions
    def add_coins(self, ID: int, guild_id: int, cash: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET `Cash` + ? WHERE `ID` = ? AND `GuildID` = ?",
                                       (cash, ID, guild_id))

    @ignore_exceptions
    def take_coins(self, ID: int, guild_id: int, cash: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET `Cash` - ? WHERE `ID` = ? AND `GuildID` = ?",
                                       (cash, ID, guild_id))

    @ignore_exceptions
    def create_voice_stats(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("INSERT INTO `OnlineStats` VALUES (?, ?, ?)", (ID, guild_id, get_time()))

    @ignore_exceptions
    def add_coins_to_the_bank(
            self,
            ID: int,
            guild_id: int,
            cash: int,
    ) -> Cursor:
        with self.connection:
            self.take_coins(ID, guild_id, cash)
            return self.cursor.execute("UPDATE  `Users` SET `CashInBank` = `CashInBank` + ? "
                                       "WHERE `ID` = ? AND `GuildID` = ?", (cash, ID, guild_id))

    @ignore_exceptions
    def add_reputation(self, ID: int, GuildID: int, reputation: int) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                "UPDATE `Users` SET `Reputation` = `Reputation` + ? WHERE `ID` = ? AND `GuildID` = ?",
                (reputation, ID, GuildID)
            )

    @ignore_exceptions
    def take_coins_from_the_bank(
            self,
            ID: int,
            guild_id: int,
            cash: int | str,
    ) -> Cursor:
        with self.connection:
            self.add_coins(
                ID,
                guild_id,
                self.get_cash(ID, guild_id, bank=True) if isinstance(cash, str) else cash)
            if isinstance(cash, str):
                return self.cursor.execute("UPDATE `Users` SET `CashInBank` = 0 "
                                           "WHERE `ID` = ? AND `GuildID` = ?", (ID, guild_id))
            else:
                return self.cursor.execute("UPDATE `Users` SET `CashInBank` = `CashInBank` - ? "
                                           "WHERE `ID` = ? AND `GuildID` = ?", (cash, ID, guild_id))

    @ignore_exceptions
    def get_loses_count(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Loses` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def get_wins_count(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Wins` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def get_three_losses_in_row_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Lose_3` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_three_losses_in_row_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Lose_3` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_ten_losses_in_row_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Lose_10` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_ten_losses_in_row_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Lose_10` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_twenty_losses_in_row_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Lose_20` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_twenty_losses_in_row_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Lose_20` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_three_wins_in_row_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Wins_3` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_three_wins_in_row_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Wins_3` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_ten_wins_in_row_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Wins_10` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_ten_wins_in_row_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Wins_10` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_twenty_wins_in_row_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Wins_20` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_twenty_wins_in_row_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Wins_20` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def update_user_stats_1(self, arg: str, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET ? = ?+ 1 WHERE `ID` = ? AND `GuildID` = ?",
                                       (arg, arg, ID, guild_id))

    @ignore_exceptions
    def update_user_stats_2(self, first_arg: str, second_arg: str, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET ?? = ?? + 1 WHERE `ID` = ? AND `GuildID` = ?",
                                       (first_arg, second_arg, first_arg, second_arg, ID, guild_id))

    @ignore_exceptions
    def update_user_stats_3(self, arg: str, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET All? = All? + 1 WHERE `ID` = ? AND `GuildID` = ?",
                                       (arg, arg, ID, guild_id))

    @ignore_exceptions
    def update_user_stats_4(self, count: int, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Users` SET Count = Count + ? WHERE `ID` = ? AND `GuildID` = ?",
                                       (count, ID, guild_id))

    @ignore_exceptions
    def stats_update_member(
            self,
            ID: int,
            guild_id: int,
            first_arg: str,
            second_arg: str,
            third_arg: str,
            count: int
    ) -> None:
        self.update_user_stats_1(first_arg, ID, guild_id)
        self.update_user_stats_2(second_arg, third_arg, ID, guild_id)
        self.update_user_stats_3(third_arg, ID, guild_id)
        self.update_user_stats_4(count, ID, guild_id)

    @ignore_exceptions
    def get_time_from_online_stats(self, ID: int, guild_id: int) -> str:
        return datetime_to_str(self.cursor.execute("SELECT `Time` FROM `OnlineStats` WHERE `ID` = ? AND `GuildID` = ?",
                                                   (ID, guild_id)).fetchone()[0])

    @ignore_exceptions
    def delete_from_online_stats(self, ID: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("DELETE FROM `OnlineStats` WHERE `ID` = ?", (ID,))

    @ignore_exceptions
    def delete_from_online(self, ID: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("DELETE FROM `Online` WHERE `ID` = ?", (ID,))

    @ignore_exceptions
    def update_minutes_in_voice_channels(self, count: int, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                "UPDATE `Users` SET `MinutesInVoiceChannels` = `MinutesInVoiceChannels` + ? "
                "WHERE `ID` = ? AND `GuildID` = ?", (count, ID, guild_id)
            )

    @ignore_exceptions
    def insert_into_online_stats(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("INSERT INTO `OnlineStats` VALUES (?, ?, ?)",
                                       (ID, guild_id, get_time()))

    @ignore_exceptions
    def get_minutes(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `MinutesInVoiceChannels` FROM `Users` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def get_voice_1_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_1` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def add_level(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute(
                "UPDATE `Users` SET Lvl = Lvl + 1 WHERE ID = ? AND GuildID = ?",
                (ID, guild_id)
            )

    @ignore_exceptions
    def set_voice_1_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET Voice_1 = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_voice_10_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_10` FROM Achievements WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_10_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Voice_10` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_voice_100_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_100` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_100_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET Voice_100 = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_voice_1000_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_1000` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_1000_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Voice_1000` = true WHERE `ID` = ? AND `GuildID` = ?",
                                       (ID, guild_id))

    @ignore_exceptions
    def get_voice_10000_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_10000` FROM `Achievements` WHERE id = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_10000_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Voice_10000` = true "
                                       "WHERE `ID` = ? AND `GuildID` = ?", (ID, guild_id))

    @ignore_exceptions
    def get_voice_100000_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_100000` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_100000_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Voice_100000` = true "
                                       "WHERE `ID` = ? AND `GuildID` = ?", (ID, guild_id))

    @ignore_exceptions
    def get_voice_1000000_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_1000000` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_1000000_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Voice_1000000` = true "
                                       "WHERE `ID` = ? AND `GuildID` = ?", (ID, guild_id))

    @ignore_exceptions
    def get_voice_10000000_achievement(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT `Voice_1000000` FROM `Achievements` WHERE `ID` = ? AND `GuildID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def set_voice_10000000_achievement(self, ID: int, guild_id: int) -> Cursor:
        with self.connection:
            return self.cursor.execute("UPDATE `Achievements` SET `Voice_1000000` = true "
                                       "WHERE `ID` = ? AND `GuildID` = ?", (ID, guild_id))

    @ignore_exceptions
    def add_win(self, ID: int, guild_id: int, null: bool = False) -> Cursor:
        with self.connection:
            if null:
                return self.cursor.execute(
                    "UPDATE `Achievements` SET `Wins` = 0 WHERE `ID` = ? AND `GuildID` = ?",
                    (ID, guild_id)
                )
            else:
                return self.cursor.execute(
                    "UPDATE `Achievements` SET `Wins` = `Wins` + 1 WHERE `ID` = ? AND `GuildID` = ?",
                    (ID, guild_id)
                )

    @ignore_exceptions
    def add_lose(self, ID: int, guild_id: int, null: bool = False) -> Cursor:
        with self.connection:
            if null:
                return self.cursor.execute(
                    "UPDATE `Achievements` SET `Loses` = 0 WHERE `ID` = ? AND `GuildID` = ?",
                    (ID, guild_id)
                )
            else:
                return self.cursor.execute(
                    "UPDATE `Achievements` SET `Loses` = `Loses` + 1 WHERE `ID` = ? AND `GuildID` = ?",
                    (ID, guild_id)
                )

    @ignore_exceptions
    def get_level(self, ID: int, guild_id: int) -> int:
        return self.cursor.execute("SELECT Lvl FROM `Users` WHERE `GuildID` = ? AND `ID` = ?",
                                   (ID, guild_id)).fetchone()[0]

    @ignore_exceptions
    def get_stat(self, ID: int, guild_id: int, stat: str) -> int | float:
        return self.cursor.execute(
            f"SELECT `?` FROM `Users` WHERE `ID` = ? AND `GuildID` = ?",
            (stat, ID, guild_id)
        ).fetchone()[0]

    @ignore_exceptions
    async def voice_delete_stats(self, member: discord.Member, arg: bool) -> None:
        try:
            self.now2 = self.get_time_from_online_stats(member.id, member.guild.id)
        except TypeError:
            pass
        else:
            self.time = datetime_to_str(get_time()) - self.now2
            self.delete_from_online_stats(member.id)
            self.update_minutes_in_voice_channels(int(self.time.total_seconds() // 60), member.id, member.guild.id)

            if arg is True:
                self.insert_into_online_stats(member.id, member.guild.id)
            minutes = self.get_minutes(member.id, member.guild.id)
            if minutes >= 1 and str(self.get_voice_1_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 500)
                self.set_voice_1_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «Вроде они добрые...»!\nВам начислено 500 коинов!")
            elif minutes >= 10 and str(self.get_voice_10_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 700)
                self.set_voice_10_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «Они добрые!»!\nВам начислено 700 коинов!")
            elif minutes >= 100 and str(self.get_voice_100_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 1500)
                self.set_voice_100_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «Отличная компания»!\nВам начислено 1500 коинов!")
            elif minutes >= 1000 and str(self.get_voice_1000_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 3000)
                self.set_voice_1000_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «А они точно добрые?»!\nВам начислено 3000 коинов!")
            elif minutes >= 10000 and str(self.get_voice_10000_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 7000)
                self.set_voice_10000_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «СПАСИТЕ»!\nВам начислено 7000 коинов!")
            elif minutes >= 100000 and str(self.get_voice_100000_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 14000)
                self.set_voice_100000_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «А может и не надо...»!\nВам начислено 14000 коинов!")
            elif minutes >= 1000000 and str(self.get_voice_1000000_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 28000)
                self.set_voice_1000000_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «Всё-таки они хорошие:)»!\nВам начислено 28000 коинов!")
            elif minutes >= 10000000 and str(self.get_voice_10000000_achievement(member.id, member.guild.id)) == "0":
                self.add_coins(member.id, member.guild.id, 56000)
                self.set_voice_10000000_achievement(member.id, member.guild.id)
                await member.send(f"На сервере {member.guild} "
                                  f"получено достижение «А у меня есть личная жизнь?»!\nВам начислено 56000 коинов!")

    @ignore_exceptions
    async def achievement(self, ctx: commands.context.Context) -> None:
        loses = self.get_loses_count(ctx.author.id, ctx.guild.id)
        wins = self.get_wins_count(ctx.author.id, ctx.guild.id)
        if self.get_three_losses_in_row_achievement(ctx.author.id, ctx.guild.id) == 0 and loses >= 3:
            self.add_coins(ctx.author.id, ctx.guild.id, 400)
            self.set_three_losses_in_row_achievement(ctx.author.id, ctx.guild.id)
            await ctx.author.send(f"На сервере {ctx.author.guild} "
                                  f"получено достижение «Азартный человек»!\nВам начислено 400 коинов!")

        elif self.get_ten_losses_in_row_achievement(ctx.author.id, ctx.guild.id) == 0 and loses >= 10:
            self.add_coins(ctx.author.id, ctx.guild.id, 3000)
            self.set_ten_losses_in_row_achievement(ctx.author.id, ctx.guild.id)
            await ctx.author.send(f"На сервере {ctx.author.guild} "
                                  f"получено достижение «Сумасшедший»!\nВам начислено 3000 коинов!")

        elif self.get_twenty_losses_in_row_achievement(ctx.author.id, ctx.guild.id) == 0 and loses >= 20:
            self.add_coins(ctx.author.id, ctx.guild.id, 10000)
            self.set_twenty_losses_in_row_achievement(ctx.author.id, ctx.guild.id)
            await ctx.author.send(f"На сервере {ctx.author.guild} "
                                  f"получено достижение «Бессмертный»!\nВам начислено 10000 коинов!")

        elif self.get_three_wins_in_row_achievement(ctx.author.id, ctx.guild.id) == 0 and wins >= 3:
            self.add_coins(ctx.author.id, ctx.guild.id, 400)
            self.set_three_wins_in_row_achievement(ctx.author.id, ctx.guild.id)
            await ctx.author.send(f"На сервере {ctx.author.guild} "
                                  f"получено достижение «Да я богач!»!\nВам начислено 400 коинов!")

        elif self.get_ten_wins_in_row_achievement(ctx.author.id, ctx.guild.id) == 0 and wins >= 10:
            self.add_coins(ctx.author.id, ctx.guild.id, 3000)
            self.set_ten_wins_in_row_achievement(ctx.author.id, ctx.guild.id)
            await ctx.author.send(f"На сервере {ctx.author.guild} "
                                  f"получено достижение «Это вообще законно?»!\nВам начислено 3000 коинов!")

        elif self.get_twenty_wins_in_row_achievement(ctx.author.id, ctx.guild.id) == 0 and wins >= 20:
            self.add_coins(ctx.author.id, ctx.guild.id, 20000)
            self.set_twenty_wins_in_row_achievement(ctx.author.id, ctx.author.id)
            await ctx.author.send(f"На сервере {ctx.author.guild} "
                                  f"получено достижение «Кажется меня не любят...»!\nВам начислено 20000 коинов!")

    @ignore_exceptions
    async def achievement_member(self, member: discord.Member) -> None:
        loses = self.get_loses_count(member.id, member.guild.id)
        wins = self.get_wins_count(member.id, member.guild.id)
        if self.get_three_losses_in_row_achievement(member.id, member.guild.id) == 0 and loses >= 3:
            self.add_coins(member.id, member.guild.id, 400)
            self.set_three_losses_in_row_achievement(member.id, member.guild.id)
            await member.send(f"На сервере {member.guild} "
                              f"получено достижение «Азартный человек»!\nВам начислено 400 коинов!")

        elif self.get_ten_losses_in_row_achievement(member.id, member.guild.id) == 0 and loses >= 10:
            self.add_coins(member.id, member.guild.id, 3000)
            self.set_ten_losses_in_row_achievement(member.id, member.guild.id)
            await member.send(f"На сервере {member.guild} "
                              f"получено достижение «Сумасшедший»!\nВам начислено 3000 коинов!")

        elif self.get_twenty_losses_in_row_achievement(member.id, member.guild.id) == 0 and loses >= 20:
            self.add_coins(member.id, member.guild.id, 10000)
            self.set_twenty_losses_in_row_achievement(member.id, member.guild.id)
            await member.send(f"На сервере {member.guild} "
                              f"получено достижение «Бессмертный»!\nВам начислено 10000 коинов!")

        elif self.get_three_wins_in_row_achievement(member.id, member.guild.id) == 0 and wins >= 3:
            self.add_coins(member.id, member.guild.id, 400)
            self.set_three_wins_in_row_achievement(member.id, member.guild.id)
            await member.send(f"На сервере {member.guild} "
                              f"получено достижение «Да я богач!»!\nВам начислено 400 коинов!")

        elif self.get_ten_wins_in_row_achievement(member.id, member.guild.id) == 0 and wins >= 10:
            self.add_coins(member.id, member.guild.id, 3000)
            self.set_ten_wins_in_row_achievement(member.id, member.guild.id)
            await member.send(f"На сервере {member.guild} "
                              f"получено достижение «Это вообще законно?»!\nВам начислено 3000 коинов!")

        elif self.get_twenty_wins_in_row_achievement(member.id, member.guild.id) == 0 and wins >= 20:
            self.add_coins(member.id, member.guild.id, 20000)
            self.set_twenty_wins_in_row_achievement(member.id, member.author.id)
            await member.send(f"На сервере {member.guild} "
                              f"получено достижение «Кажется меня не любят...»!\nВам начислено 20000 коинов!")

    @ignore_exceptions
    async def cash_check(
            self,
            ctx: commands.context.Context,
            cash: int,
            max_cash: int = None,
            min_cash: int = 1,
            check: bool = False
    ) -> bool:
        if cash is None:
            await ctx.send(f"""{ctx.author.mention}, Вы не ввели сумму!""")
        elif check and cash > self.get_cash(ctx.author.id, ctx.guild.id):
            await ctx.send(f"""{ctx.author.mention}, у Вас недостаточно средств!""")
        else:
            if cash == "all":
                return True
            elif max_cash is not None:
                if (cash < min_cash or cash > max_cash) and ctx.author.id != 401555829620211723:
                    await ctx.send(f'{ctx.author.mention}, нельзя ввести число меньше '
                                   f'{divide_the_number(min_cash)} и больше {divide_the_number(max_cash)}!')
                else:
                    return True
            elif max_cash is None:
                if cash < min_cash and ctx.author.id != 401555829620211723:
                    await ctx.send(f'{ctx.author.mention}, нельзя ввести число меньше {divide_the_number(min_cash)}!')
                else:
                    return True
        return False

    @ignore_exceptions
    async def stats_update(
            self,
            ctx: commands.context.Context,
            first_arg: str,
            second_arg: str,
            third_arg: str,
            count: int
    ) -> None:
        self.update_user_stats_1(first_arg, ctx.author.id, ctx.author.id)
        self.update_user_stats_2(second_arg, ctx.author.id, ctx.author.id)
        self.update_user_stats_3(third_arg, ctx.author.id, ctx.guild.id)
        self.update_user_stats_4(count, ctx.author.id, ctx.guild.id)

        if third_arg == "loses":
            self.add_lose(ctx.author.id, ctx.guild.id)
            self.add_win(ctx.author.id, ctx.guild.id, True)

        elif third_arg == "wins":
            self.add_win(ctx.author.id, ctx.guild.id)
            self.add_lose(ctx.author.id, ctx.guild.id, True)

        await self.achievement(ctx)

    @ignore_exceptions
    async def voice_delete(self, member: discord.Member) -> None:
        try:
            now2 = self.get_time_from_online_stats(member.id, member.guild.id)
        except TypeError:
            pass
        else:
            lvl = self.get_level(member.id, member.guild.id)
            if lvl != 1:
                if lvl != 5:
                    lvl *= 2
                else:
                    lvl *= 4
            self.minutes = self.get_minutes(member.id, member.guild.id)
            self.add_coins(member.id, member.guild.id, self.minutes * (datetime_to_str(get_time()) - now2))
            self.delete_from_online(member.id)
            self.update_minutes_in_voice_channels(self.minutes, member.id, member.guild.id)
            self.month = int(datetime.today().strftime('%m'))
            self.day = int(datetime.today().strftime('%d'))
            if self.month > 11 or self.month == 1:
                if (self.month == 12 and self.day > 10) or (self.month == 1 and self.day < 15):
                    self.prises[member.id] = 0
                    for i in range(self.minutes):
                        if random.randint(1, 3) == 3:
                            if random.randint(1, 3) == 3:
                                if random.randint(1, 3) == 3:
                                    if random.randint(1, 3) == 1:
                                        if random.randint(1, 3) == 3:
                                            self.prises[member.id] += 1
                    if self.prises[member.id] != 0:
                        self.add_prises(self.prises[member.id], member.id, member.guild.id)
                        try:
                            await member.send(
                                "Вам начислено {} новогодних подарков! Чтобы открыть их пропишите //open\n"
                                "У нас кстати новогодний ивент:) пиши //help new_year".format(
                                    self.prises[member.id]
                                )
                            )
                        except discord.errors.Forbidden:
                            pass
            if self.month == 2 and self.day == 14:
                self.valentine[member.id] = 0
                for i in range(self.minutes):
                    if random.randint(0, 4) == 1:
                        if random.randint(0, 4) == 2:
                            if random.randint(0, 4) == 3:
                                self.valentine[member.id] += 1
                if self.valentine[member.id] != 0:
                    self.add_valentines(self.valentine[member.id], member.id, member.guild.id)
                    try:
                        await member.send(
                            "Вам пришло {} валентинок! Чтобы открыть их пропишите //val_open".format(
                                self.valentine[member.id]
                            )
                        )
                    except discord.errors.Forbidden:
                        pass

    def is_the_casino_allowed(self, channel_id: int) -> bool:
        if self.cursor.execute("SELECT CasinoChannelID FROM Server WHERE GuildID = ?",
                               (channel_id,)).fetchone() is None:
            return True
        if channel_id in [572705890524725248, 573712070864797706] or \
                self.cursor.execute("SELECT CasinoChannelID FROM Server WHERE GuildID = ?", (channel_id,)).fetchone():
            return True
        return False
