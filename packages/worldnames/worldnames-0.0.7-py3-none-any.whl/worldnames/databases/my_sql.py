# This module contains a MySQL class thats being used to connect to a MySQL database.

# Python imports
import time, os, sys, platform
# 3th part imports
from mysql import connector
from mysql.connector import (errorcode, cursor)
from rich.console import Console
from tabulate import tabulate
# Worldnames imports
from worldnames.content import logo
from worldnames.content import custom_print
from worldnames.databases.sqlsharing import SqlShared

# Globals being used in this module
operating_system = platform.system().lower()
clear = "clear" if operating_system == "linux" or operating_system == "darwin" else "cls"
console = Console()


class MySQL(SqlShared):

    """
    A MySQL class to simulate populating a database using MySQL inheriting from SqlShared containing methods to
    populate the mysql database.
    """

    def __init__(self) -> None:
        self.connected = False
        self.users = list()
        self.databases = None
        self.validators = {
            'user_name': False,
            'password': False,
            'host': False,
            'port': False
        }
        self.connection_attempt = False
        while True:
            os.system(clear)
            console.print(logo)
            custom_print("Om een verbinding te kunnen maken met jouw MySQL database. Dien je de" \
                         + "volgende informatie in te vullen: \n")
            if not self.validators['user_name']:
                self.user_name = input("Gebruikersnaam: ").strip()
                self.validators['user_name'] = True
            if not self.validators['password']:
                self.password = input("Wachtwoord: ").strip()
                self.validators['password'] = True
            if not self.validators['host']:
                self.host = input("Host: ").strip()
                self.validators['host'] = True
            if not self.validators['port']:
                self.port = input("Poort: ").strip()
                self.validators['port'] = True
            try:
                custom_print("\nVerbinding maken met MySQL...")
                self.cnx = self.connect()
            except connector.Error as error:
                if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    custom_print("Gebruikersnaam of wachtwoord is ongeldig!")
                    self.validators['user_name'] = False
                    self.validators['password'] = False
                    time.sleep(2)
                    continue
                elif error.errno in [errorcode.CR_CONN_HOST_ERROR, -1, errorcode.CR_UNKNOWN_HOST, errorcode.ER_BAD_HOST_ERROR]:
                    custom_print(f"Host {self.host} of poort {self.port} is ongeldig!")
                    self.validators['port'] = False
                    self.validators['host'] = False
                    time.sleep(2)
                    continue
                else:
                    custom_print("Something went wrong, create a ISSUE on: https://github.com/ayoub-abdessadak/worldnames/issues")
                    custom_print(f"ERROR: {error.errno}, {error.msg}, {error}, {error.sqlstate}")
                    sys.exit()
            else:
                custom_print("Verbinding successvol")
                self.connection_attempt = True
                self.disconnect()
                return

    def connect(self) -> connector:
        """
        class method to connect to the mysql database
        :return: a mysql connector
        """
        self.connected = True
        return connector.connect(user=self.user_name, password=self.password, host=self.host, port=self.port)

    def disconnect(self) -> None:
        """
        class method to disconnect to the mysql database
        :return: None
        """
        self.connected = False
        self.cnx.close()

    def get_cursor(self) -> cursor:
        """
        class method to lazy retrieve a cursor
        :return: a mysql cursor
        """
        if not self.connected:
            self.cnx = self.connect()
        return self.cnx.cursor(buffered=True)

    def run(self) -> None:
        """
        class method to run the populating simulator and start an infinite loop, letting the user search through a table.
        :return: None
        """
        table_name = "Users"
        super().create_table(self.get_cursor(), table_name, False)
        super().fill_table(self.get_cursor(), self.cnx, table_name, 20)
        super().view_users(self.get_cursor(), table_name)
        while True:
            os.system(clear)
            console.print(logo)
            custom_print(self)
            _exit = super().search_user(self.get_cursor(), None, table_name)
            if _exit:
                break

    def __repr__(self) -> str:
        """
        printing the table nicely using tabulate
        :return: string
        """
        return f"""{tabulate(self.users, headers=self.headers, tablefmt="fancy_grid")}\n"""
