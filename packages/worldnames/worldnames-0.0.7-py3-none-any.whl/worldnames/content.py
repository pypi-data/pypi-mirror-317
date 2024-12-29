# This module holds the icon and logo being used in the world-names CLI program as wel as a custom print method for a nicer UI on the CLI

# 3th party imports
from rich.text import Text
from colorama import Fore

# Custom print function
def custom_print(*args, **kwargs) -> None:
    print(Fore.GREEN, *args, **kwargs)
    
logo_world_names = """
V0.0.5 WorldNames  - https://github.com/ayoub-abdessadak/worldnames
                        _      _
                       | |    | |
__      __  ___   _ __ | |  __| | _ __    __ _  _ __ ___    ___  ___
\ \ /\ / / / _ \ | '__|| | / _` || '_ \  / _` || '_ ` _ \  / _ \/ __|
 \ V  V / | (_) || |   | || (_| || | | || (_| || | | | | ||  __/\__ |
  \_/\_/   \___/ |_|   |_| \__,_||_| |_| \__,_||_| |_| |_| \___||___/
"""
icon_ = """                    

	                          ,, -- ~~~~~ --,,          .·``·..·``·. 
	                    , - ˜˜                      ˜˜-,    (   i love  `·. 
	                ,-''                                  '',  `·.  you!    ) 
	              ,˜                                    ,,-'     `·..·``·..·` 
	            ,˜                       __...---(ˆˆ¯¯ 
	           .;                 ,..,              ˜˜ ' -, 
	          .;              ,-'¯    ¯ˆ·--..-·ˆ¯ˆˆ ----,' _ 
	          ;            ,-''        (¯¯\   (¯¯\    ,-˜    ˜-, 
	          ;.     ,,---,-'''---,      @_)  @_)-˜         ,' 
	           ;.   ( ,-' ˜       ˆ-,.,.,.,.,.,.,.,.,          ,-``·. 
	            ˜-,- '     ,-˜;                      ˜˜·----·''     ;` 
	              ˜-,         ˜-,        «-,..¸_¸.·-,-˜   ,˜  ,-˜ 
	                 ˜-,    ,                ',_, -˜   , ˜ ,-˜ 
	                     ˜-,  ˜ -- ,.                   , -˜ 
	                       ,-''-- 
	.,.,.,.,.,.,.,.,.--,˜ˆ˜'ˆ˜'ˆ˜''ˆ˜'ˆ˜'ˆ˜ˆ˜'ˆ˜') 
	                    ,-''                            ˜-,.,.,,     ;˜'ˆ'˜'˜ 
	                  ,-''    ,-'                          ˜;    ˜˜-..-' 
	 ;˜¯˜·-,      ,-''     ,-'                              ˜;. 
	  ˜-,    ˜-,,-'      ,-˜                                 ; 
	(¯˜˜¯            ,-˜ ˜··---.,.,.,.,.,.,.,.,.,.,.,.---··˜; 
	¯˜˜¯)     ,,,-' ˜-,                                   ,˜ 
	  ,-'˜   ,·'˜        ';                               ,-˜ 
	   ˜···˜             ';                           ,-˜ 
	                     ';     ˜˜-,.,.,.,.,.,.,.,--;' 
	                    ;'         ;'    ;'        ;' 
	              ,.,.,;'          ;_,.;',.,_    ';_,.,._ 
	            ;'               ,;'          ˜;  '         ˜; 
	            ˜;                          ;'             ;' 
	              ˜·-.,.,.,.,.,.,.,.,.,.,-·˜,.,,.,...,,-·˜
	              
	              Written by Ayoub ben Abdessadak

"""
logo = Text(logo_world_names, style="bold green")
logo.stylize("blink", 7, 12)

icon = Text(icon_, style="bold green")
icon.stylize("blink", 7, 12)
