# This module contains a Sqlite class that's being used to create or connect to a sqlite database.

# Python imports
from datetime import datetime
import sqlite3, os, sys, platform
# 3th party imports
from tabulate import tabulate
from rich.console import Console
# Worldnames imports
from worldnames.databases.sqlsharing import SqlShared
from worldnames.content import logo
from worldnames.content import custom_print

# Globals being used in this module
operating_system = platform.system().lower()
clear = "clear" if operating_system == "linux" or operating_system == "darwin" else "cls"
console = Console()
console.print(logo)

class Sqlite(SqlShared):

    """
    Class for sim-populating a sqlite database.
    """

    def __init__(self, simulation: bool=True) -> None:
        """
        on init creating a test database or opening an existing database.
        :param simulation:
        """
        self.tables = None
        self.table_name = None
        self.users = list()
        if simulation:
            self.database_name = f"SIMDATABASE-{datetime.now().isoformat()}"
            self.database_name = self.database_name.replace(":", "_").replace(".", "_")
            file = open(self.database_name, "w")
            file.close()
        else:
            self.database_name = input("Geef de sqlite.db file op met het volledige pad naar het bestand: ")
        try:
            self.con = sqlite3.connect(self.database_name)
            self.cursor = self.con.cursor()
        except Exception as error:
            custom_print(f"Create a issue for error {error} on github")
            sys.exit()

    def run(self) -> None:
        """
        class method to run the populating simulator and start an infinite loop, letting the user search through a table.
        :return: None
        """
        table_name = "Users"
        super().create_table(self.cursor, table_name, True)
        super().fill_table(self.cursor, self.con, table_name, 20)
        super().view_users(self.cursor, table_name)
        while True:
            os.system(clear)
            console.print(logo)
            custom_print(self)
            _exit = super().search_user(self.cursor, None, table_name)
            if _exit:
                break

    def __repr__(self) -> str:
        """
        printing the table nicely using tabulate
        :return: string
        """
        return f"""{tabulate(self.users,headers=self.headers,tablefmt="fancy_grid")}\n"""

