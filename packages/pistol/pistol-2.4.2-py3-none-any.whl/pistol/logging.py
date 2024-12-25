from colorama import Style, Fore, Back

def error(text: str) -> None:
    print(f"🚨 {Fore.RED}error: {text}{Style.RESET_ALL}")
def hint(text: str) -> None:
    print(f"💡 {Fore.BLUE}hint: {text}{Style.RESET_ALL}")
def warning(text: str) -> None:
    print(f"⚠  {Fore.YELLOW}warning: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def important(text: str) -> None:
    print(f"⚠  {Back.YELLOW}{Fore.BLACK}important: {text}{Style.RESET_ALL}")
    # two spaces are on purpose!!
def info(text: str) -> None:
    print(f"➤➤ {text}")