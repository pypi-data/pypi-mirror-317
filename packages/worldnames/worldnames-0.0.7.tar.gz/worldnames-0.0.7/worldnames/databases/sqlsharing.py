# This module contains a SqlShared class that's being used in both sqlite and mysql module in the databases package.

#Python imports
import os, time, platform
from uuid import uuid4
# 3th party imports
from tabulate import tabulate
from yaspin import yaspin
from mysql.connector import cursor as _cursor
from rich.console import Console
# Worldnames imports
import worldnames
from worldnames.content import logo
from worldnames.content import custom_print
from worldnames.databases.customdatatypes import User

# Globals being used in this module
operating_system = platform.system().lower()
clear = "clear" if operating_system == "linux" or operating_system == "darwin" else "cls"
console = Console()
console.print(logo)

class SqlShared:

    """
    Class with methods that are being used when populating a MySQL or sqlite database.
    """

    headers: list = ["Voornaam", "Achternaam", "Gender", "Leeftijd", "Email"]
    users: list = []

    @staticmethod
    def wait(seconds: int | float) -> None:
        """
        When called I display a spinning icon for the given seconds.
        :param seconds:
        :return: None
        """
        with yaspin():
            time.sleep(seconds)

    def create_table(self, cursor:_cursor, table_name: str="Users", lite=True) -> bool:
        """
        This class method is responsible to create a table in SQL, supports MySQL and Sqlite
        :param cursor:
        :param table_name:
        :param lite:
        :return: bool, true if created, false if not
        """
        # Test Database maken for MySQL
        if not lite:
            custom_print("Tijdelijke database maken...")
            db_name = "db" + uuid4().__str__()[0:10].replace("-", '')
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.execute(f"USE {db_name};")
            self.wait(1)
            custom_print(f"Database: {db_name} aangemaakt")
            self.wait(0.5)
        # Tabel maken in MySQL of Sqlite test DB
        custom_print(f"Tabel {table_name} maken...")
        query = (f"CREATE TABLE {table_name}(first_name CHAR(255),"+
                 "last_name CHAR(255), gender CHAR(255), age INT, email CHAR(255))")
        cursor.execute(query)
        self.wait(1)
        # Tabellen ophalen voor sqlite of mysql
        if lite:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        else:
            cursor.execute("SHOW TABLES;")
        tables = [table[0] for table in cursor.fetchall()]
        if table_name in tables:
            custom_print(f"{table_name} is successvol aangemaakt")
            self.wait(1)
            return True
        else:
            custom_print(f"Het is niet gelukt om de tabel {table_name} te maken.")
            self.wait(2)
            return False

    def add_user(self, user: tuple | User, cursor:_cursor, con, table_name: str="Users") -> None:
        """
        This class method is responsible for adding a user. When called user is added into table destined for that DB.
        :param user: tuple or User
        :param cursor: sql cursor
        :param con: sql connector
        :param table_name: str
        :return: none
        """
        if isinstance(user, User):
            user = tuple([*user])
        custom_print(f"Gebruiker: {user} toevoegen")
        query = f"INSERT INTO {table_name} (first_name, last_name, gender, age, email) VALUES {user}"
        cursor.execute(query)
        con.commit()
        self.wait(0.23)

    def fill_table(self, cursor:_cursor, con, table_name: str="Users", amount_of_users: int = 20) -> None:
        """
        Class method to fill a table with users, default is 20 users. Users will be populated using the world-names populater
        :param cursor: sql cursor
        :param con: sql connector
        :param table_name: str
        :param amount_of_users: int
        :return: None
        """
        for _ in range(amount_of_users):
            self.add_user(worldnames.user(), cursor, con, table_name)

    def view_users(self, cursor:_cursor, table_name: str = "Users") -> None:
        """
        Class method to view users that have been populated
        :param cursor: sql cursor
        :param table_name: str
        :return: None
        """
        os.system(clear)
        console.print(logo)
        custom_print(f"Users for table: {table_name}\n")
        query = f"SELECT * from {table_name}"
        cursor.execute(query)
        res = cursor.fetchall()
        users = res
        self.users = [User(*user) for user in users] # Custom data type User
        # The implemented iterator of the custom data type is used by tabulate
        custom_print(tabulate(self.users, headers=self.headers, tablefmt="fancy_grid"))
        input("\nKlik op enter om verder te gaan...")

    def search_user(self, cursor:_cursor, search_input: str=None, table_name: str = "Users") -> str:
        """
        Class method that let the user search through a table.
        :param cursor: sql cursor
        :param search_input: str
        :param table_name: str
        :return: str (exit)
        """
        custom_print("Typ exit om de zoekfunctie te verlaten\n")
        search_input = input("Zoek: ") if not search_input else search_input
        if search_input.lower().strip() == "exit":
            return "exit"
        fields = ["first_name", "last_name", "gender", "age", "email"]
        search_input = search_input.split()
        results = []
        for field in fields:
            for si in search_input:
                query = f"SELECT * FROM {table_name} WHERE {field} LIKE '%{si}%'"
                cursor.execute(query)
                result = cursor.fetchall()
                results = [*results, *result]
        results = set(results)
        self.wait(0.1)
        os.system(clear)
        console.print(logo)
        custom_print(f"Gevonden resultaten voor zoekopdracht: {' '.join(search_input)}")
        custom_print(tabulate(results,headers=self.headers,tablefmt="fancy_grid"))
        input("\nEnter om verder te gaan...")