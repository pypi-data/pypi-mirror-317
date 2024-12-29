# An enumeration for the databases being used in the JSON(CLI) program. Simple enumeration with 2 members.

#Python imports
from enum import Enum
# Worldnames imports
from worldnames.databases.my_sql import MySQL
from worldnames.databases.sqlite import Sqlite

class Databases(Enum):
    sqlite = Sqlite
    mysql = MySQL