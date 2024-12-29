# Auteur: Ayoub ben Abdessadak
# This module runs the RunJsonProgram class and specifically the run_program method bound to an instance of that class.
# That method contains some conditional statements that causing the program to loop through a dictionary. It can be extended for more functionalities.

# Python imports
import time, os, sys, platform
# 3th party imports
from rich.console import Console
# world-names imports
from worldnames.flow import program
from worldnames.content import logo, icon

# globals being used in this module
operating_system = platform.system().lower()
clear = "clear" if operating_system == "linux" or operating_system == "darwin" else "cls"
console = Console()

class RunJsonProgram:

    """
    This class is written to run a CLI program that can be written in JSON (FROM AN PYTHON MODULE).
    """

    def __init__(self) -> None:
        self.database = None
        self.showed_icon = False

    def run_program(self, program_flow: dict) -> None:
        """
        The run program method bound to the created instance of RunJsonProgram runs a program that can be written in JSON.
        See the program in flow.py
        :param program_flow: Program in JSON
        :return: None
        """
        _next = 1
        while True:
            if _next == -1:
                print("Tot ziens :)")
                sys.exit()
            flow = program_flow[_next]
            os.system(clear)
            console.print(self.__logo())
            print(flow["color"] + f'''\n{flow["title"]}\n{flow["options"]}''')
            choice = input(flow["question"])
            if flow["action"] == "call":
                try:
                    output = flow['enum'][flow['option_values'][choice.strip()]].value()
                    output.run()
                    _next = flow["next"]
                    continue
                except KeyError:
                    print("De opgegeven keuze is ongeldig.")
                    time.sleep(2)
                    continue
                except Exception as error:
                    print(f"Something went wrong, make a issue on GIT, for {error}")
                    sys.exit()

            if flow["action"] == "flow":
                try:
                    _next = flow["option_values"][choice.strip()]
                    continue
                except KeyError:
                    print("De opgegeven keuze is ongeldig.")
                    time.sleep(2)
                    continue
                except Exception as error:
                    print(f"Something went wrong, make a issue on GIT, for {error}")
                    sys.exit()

            if not flow["action"]:
                _next = flow["next"]
                continue

    def __logo(self) -> str:
        """
        If you call me I will return once an icon and always the worldnames logo. You should print me.
        :return: str
        """
        if not self.showed_icon:
            self.showed_icon = True
            return logo + icon
        else:
            return logo

if __name__ == "__main__":
    rjp = RunJsonProgram()
    rjp.run_program(program)
