

import pyfiglet
from colorama import Fore
from tabulate import tabulate
 
DEBU = Fore.CYAN
INFO = Fore.GREEN
WARN = Fore.BLUE
ERRO = Fore.YELLOW
CRIT = Fore.RED
NORM = Fore.WHITE

fore_color_map = {
	'cyan': Fore.CYAN,
	'green': Fore.GREEN,
	'blue': Fore.BLUE,
	'yellow': Fore.YELLOW,
	'red': Fore.RED,
	'white': Fore.WHITE,
	None: Fore.WHITE,
	'black': Fore.BLACK,
	'magenta': Fore.MAGENTA,

}

def print_banner(banner, color):
	banner = pyfiglet.figlet_format(banner, font='doom')
	print(fore_color_map[color] + '\n' + banner)
	print(Fore.WHITE + "")

def print_table(df, tablefmt='rounded_outline'):
	printable = tabulate(df, headers='keys', tablefmt=tablefmt)
	print(printable)
	