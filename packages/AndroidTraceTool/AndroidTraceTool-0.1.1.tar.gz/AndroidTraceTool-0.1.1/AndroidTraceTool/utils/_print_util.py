from colorama import Fore, Back, Style


def print_info(message):
    print(Fore.WHITE + str(message) + Style.RESET_ALL)


def print_success(message):
    print(Fore.GREEN + str(message) + Style.RESET_ALL)


def print_error(message):
    print(Fore.RED + str(message) + Style.RESET_ALL)


def print_warning(message):
    print(Fore.YELLOW + str(message) + Style.RESET_ALL)
