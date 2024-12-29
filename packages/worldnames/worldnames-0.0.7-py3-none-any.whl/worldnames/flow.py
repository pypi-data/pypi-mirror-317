# This module holds the program written in JSON that's being used in the RunJsonProgram class.
# The goal is to reduce the amount of conditional statements being used to write a CLI program.

# Worldnames imports
from worldnames.databases import Databases
# 3th party imports
from colorama import Fore

program = {
    1: {
        "title": "User Populater WorldNames - Een programma om fictieve gebruikers aan te maken",
        "question": "Klik op enter om door te gaan...",
        "action": "",
        "options": f"",
        "option_values": None,
        "enum": None,
        "next": 2,
        "color":Fore.GREEN,
    },
    2: {
        "title": "Simulatie (in dit programma wordt een simulatie uitgevoerd voor het populeren van een database)\n",
        "question": "\nMaak een keuze: ",
        "action": "call",
        "options": f"1. Simuleren via MySQL\n2. Simuleren via SqlLite",
        "option_values": {
            "1": "mysql",
            "2": "sqlite",
        },
        "enum": Databases,
        "next": 3,
        "color": Fore.GREEN,
    },
    3: {
        "title": "WorldNames Hoofdmenu\n",
        "question": "\nKeuze: ",
        "action": "flow",
        "options": f"1. Om opnieuw een simulatie uit te voeren\n2. Om het programma te verlaten",
        "option_values": {
            "1": 2,
            "2": -1,
        },
        "enum": None,
        "next": 3,
        "color": Fore.GREEN,
    },
}

