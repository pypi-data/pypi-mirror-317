import os, sys, subprocess, webbrowser

from pathlib import Path
from colorama import Style, Back
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText

from .mutable_path import MutablePath
from .constants import (
    DIR,
    STORAGE_PATH,
    PLATFORM,
    SYS_ROOT
)
from .logging import (
    error,
    info,
    warning,
    important,
    hint
)
from .scs_cache import SCSCacheManager
from .timestamp import Timestamp
from .subprocess import subprocess_run
from .meta import MetaJSON
from .parser import parse_command
from .prop_state import PropState

history: InMemoryHistory = InMemoryHistory()

def main() -> None:
    meta: MetaJSON = MetaJSON(DIR / "meta.json")
    meta.create()
    scs_cm: SCSCacheManager = SCSCacheManager(meta)
    scs_cm.load()
    at: str = (meta.read()["last_location"] or os.getcwd()) if meta.fetch("persistent-location") else os.getcwd()
    if len(sys.argv) > 1:
        if sys.argv[1] == "storage":
            at = str(STORAGE_PATH)
        elif sys.argv[1] == "last" and meta.fetch("persistent-location"):
            at = meta.read()["last_location"] or os.getcwd()
        else:
            at = sys.argv[1]
    abs_at = os.path.abspath(at).removesuffix("-n").replace(" ", "\\ ")
    running_as_new: bool = "--running-as-new" in sys.argv
    if "-n" in sys.argv or "--new" in sys.argv:
        match PLATFORM:
            case "windows":
                subprocess_run(["cmd", "/C", "start", "pistol", abs_at, "--running-as-new"], "internal")
            case "linux":
                hint("not working? make sure gnome-terminal is available")
                subprocess_run(["gnome-terminal", "--", "bash", "-c", f"cd {SYS_ROOT}; pistol {abs_at} --running-as-new; exec bash"], "internal")
            case _:
                error("unidentified operating system; could not find a way to open a new terminal.")
        exit(0)
    mutable_location: MutablePath = MutablePath(Path(os.getcwd()))
    cd_history: list[str] = meta.read()["cd_history"]
    cmd_history: list[tuple[Timestamp | str, str]] = []
    for timestamp, cmd in meta.read()["cmd_history"]:
        cmd_history.append((Timestamp.from_dict(timestamp) if timestamp != "n/a" else timestamp, cmd))
    mutable_location.set(at, [], st=at==str(STORAGE_PATH))
    solo_mode: str = ""
    aliases: dict[str, str] = meta.read()["aliases"]
    while True:
        if (os.path.getsize(meta.path) / 1024) > 500 and meta.fetch("meta-size-warning"): # larger than 500kb
            warning("pistol's meta file is getting quite big! run meta to learn more and free up space.")
            hint("run prop meta-size-warning false to disable this warning.")
        try:
            loc: Path = mutable_location.path
            disp_loc: str = "storage" if str(loc) == str(STORAGE_PATH) else loc
            autocomplete: list[str] = []
            if meta.fetch("suggest-files"):
                autocomplete += [f"./{item}" for item in os.listdir(loc) if not item.startswith(".")] + [".."]
            if meta.fetch("scs"):
                autocomplete += scs_cm.suggest_commands(loc)
            completer: WordCompleter = WordCompleter(autocomplete, ignore_case=True)
            session: PromptSession = PromptSession(history=history, completer=completer)
            command_protection: bool = False
            try:
                if solo_mode:
                    prompt_text: FormattedText = FormattedText([
                        ("class:yellow", f"➤➤ {os.name}: "),
                        ("", f"{disp_loc} "),
                        ("class:magenta", f"[{solo_mode}]"),
                        ("class:blue", "> "),
                    ])
                    full_command: str = (solo_mode + " " + session.prompt(prompt_text)).removeprefix(f"{solo_mode} pistol ")
                    full_command = full_command.removeprefix(f"{solo_mode} ") if full_command.startswith(f"{solo_mode} cd ") else full_command
                    if full_command == f"{solo_mode} exit":
                        info(f"exited {solo_mode}")
                        solo_mode = ""
                        continue
                else:
                    prompt_text: str = FormattedText([
                        ("", "➤➤ "),
                        ("class:yellow", f"{os.name}: "),
                        ("", f"{disp_loc}"),
                        ("class:blue", "> "),
                    ])
                    full_command: str = session.prompt(prompt_text)
            except EOFError:
                print()
                try:
                    import getpass

                    hint("press ^C to exit pistol")
                    hint("press any other button to return to pistol")

                    getpass.getpass(f"➤➤ ")
                    continue
                except KeyboardInterrupt:
                    full_command: str = "exit --no-hint"
                    command_protection = True
                    print()
                except EOFError:
                    print()
                    continue

            parts: list[str] = full_command.split(" ")
            new, string = parse_command(parts)
            if string:
                error("unclosed string in command.")
                continue
            if not new:
                continue
            command: str = new[0]
            args: list[str] = new[1:]
            if not command_protection:
                cmd_history.append((Timestamp.from_now() if meta.fetch("timestamps") else "n/a", full_command))
                if meta.fetch("scs-collection"):
                    scs_cm.add(loc, full_command)

            try:
                def refresh():
                    meta_contents = meta.read()
                    meta_contents["cd_history"] = cd_history
                    writable_cmd_history = []
                    for timestamp, cmd in cmd_history:  # NOQA
                        writable_cmd_history.append((timestamp.to_dict() if timestamp != "n/a" else timestamp, cmd))
                    meta_contents["cmd_history"] = writable_cmd_history
                    meta_contents["aliases"] = aliases
                    meta_contents["last_location"] = str(loc)
                    meta.write(meta_contents)
                    if meta.fetch("scs-refresh"):
                        scs_cm.save()
                def exit_pistol():
                    refresh()
                    info("exited pistol")
                    if "--no-hint" not in args:
                        hint("pressing ^D chord to ^C will exit pistol as well")
                    if running_as_new:
                        hint("press ^D to exit the terminal entirely")
                    exit()
                def run_solo(c: list[str]):
                    nonlocal solo_mode

                    if args not in [
                        [],
                        ["pwsh", "-Command"]
                    ]:
                        force_cwd: bool = "--force-cwd" in args
                        args.remove("--force-cwd") if "--force-cwd" in args else ...
                        if args[0] in c:
                            warning(f"{args[0]} may not work properly when executing using {solo_mode or command}")
                        old_dir: str = os.getcwd()
                        try:
                            os.chdir(loc)
                        except FileNotFoundError:
                            if force_cwd:
                                info(f"created {disp_loc}")
                                os.mkdir(loc)
                                os.chdir(loc)
                            else:
                                warning(f"tried to execute a solo command in a directory that does not exist. solo will execute it in {old_dir} instead.")
                                hint(f"rerun the command with the --force-cwd option to run in {disp_loc}.")
                        subprocess_run(args, command)
                        os.chdir(old_dir)
                    else:
                        solo_mode = command
                def undo_cd(internal: bool = False):
                    try:
                        mutable_location.set(cd_history.pop(), [], ucd=True)
                    except IndexError:
                        if internal:
                            return False
                        else:
                            warning("nothing left to undo")
                    return True
                def st():
                    if str(loc) != str(STORAGE_PATH):
                        mutable_location.set(str(STORAGE_PATH), cd_history, st=True),
                        hint("use st again to return to normal mode")
                    elif not undo_cd(internal=True):
                        warning(f"could not find location to exit to, defaulting to {os.getcwd()}")
                        mutable_location.set(os.getcwd(), [], st=True)
                def view_cd_history():
                    if not cd_history:
                        info("cd history empty")
                    else:
                        index: int = 1
                        for index, item in enumerate(cd_history, start=1):
                            info(f"{index}: {item}")
                        info(f"{index+1}: {disp_loc}")
                        hint(f"{index+1} is your current location. the next ucd will take you to {index}")
                def clear_cd_history():
                    nonlocal cd_history
                    cd_history = []

                from . import VERSION

                def reverse_search():
                    if not cmd_history:
                        error("cannot reverse search; no command history")
                    else:
                        hint("find a command in your command history by entering it exactly,")
                        hint("or just a part of it you remember. type help for more info.")
                        try:
                            search: str = input(f"➤➤ {Back.YELLOW}query{Style.RESET_ALL}> ")
                        except EOFError:
                            print()
                            return
                        if search == "help":
                            info("command history is saved even after you exit pistol")
                            important("command history may not be saved if pistol is reinstalled,")
                            important("tampered with, or reset.")
                            info("you can also just press return to list all command history")
                            info("you can run rmc <full command> to delete a command from your history")
                            info("you can run cch to clear your command history entirely")
                        else:
                            for cmd in cmd_history: # NOQA
                                if search in cmd[1]:
                                    info(f"{cmd[0]} - {cmd[1]}")
                def clear_command_history():
                    nonlocal cmd_history
                    cmd_history = []
                def remove_from_command_history(internal: bool = False):
                    query: str = " ".join(args)
                    for i, cmd in enumerate(cmd_history): # NOQA
                        if cmd[1] == query:
                            break
                    else:
                        if not internal:
                            error(f"{query} could not be found in the command history")
                        return False
                    cmd_history.pop(i)
                    if not internal:
                        info(f"removed {query}")
                    remove_from_command_history(internal=True)
                    return True
                def remove_from_aliases():
                    try:
                        del aliases[args[0]]
                        info(f"removed alias {args[0]}")
                    except KeyError:
                        error(f"alias {args[0]} does not exist.")
                def clear_aliases():
                    nonlocal aliases
                    aliases = {}
                def analyse():
                    info(f"pistol's meta file is currently {os.path.getsize(meta.path) / 1024:.2f}kb large")
                    info(f"it is stored in {meta.path}")
                    info(f"the meta file includes {len(cd_history)} cd history item{'s' if len(cd_history) != 1 else ''},")
                    info(f"{len(cmd_history)} command history item{'s' if len(cmd_history) != 1 else ''},")
                    info(f"and {len(aliases)} alias(es).")
                    info("to free up this space, you can run:")
                    info("- cch to clear command history [1] (usually takes up the most space)")
                    info("- ccdh to clear cd history [2]")
                    info("- ca to clear aliases [3]")
                    info("- cs to clear scs cache [4]")
                    info("- prop timestamps false to disable timestamps for command history items. this significantly reduces the size of the items.")
                    hint("[1] command history includes commands and timestamps used by the rs command.")
                    hint("[2] cd history includes the paths of the locations you were in used by ucd and cdh.")
                    hint("[3] aliases include the names and full commands of the aliases you created.")
                    hint("[4] scs cache includes the commands and locations used in the tab completions.")
                    important("prop auto-re is disabled. remember to run re so changes can take effect") if not meta.fetch("auto-re") else ...
                def set_property():
                    meta_contents = meta.read()
                    try:
                        state = PropState.from_string(args[1])
                    except KeyError:
                        error(f"state must be {', '.join(PropState.options)}, or check")
                    else:
                        meta_contents["props"] |= {args[0]: state.state}
                        meta.write(meta_contents)
                        info(f"{args[0]} set to {state.to_string()}")
                def view_property():
                    props = meta.read()["props"]
                    if args[0] in list(props.keys()):
                        info(f"prop {args[0]} - {PropState(props[args[0]]).to_string()}")
                    else:
                        info(f"prop {args[0]} - not specified; cannot define state.")
                    hint(f"use prop {args[0]} true/false to switch the state")
                def remove_suggestion():
                    arg1: str | None = (args[1] if len(args) >= 2 else "").lower()
                    if arg1 in ["here", ".", ""]:
                        path = loc
                    elif arg1 in ["any", "all", "*"]:
                        path = None
                    elif Path(arg1).exists():
                        path = Path(arg1)
                    else:
                        error(f"invalid symbol {arg1}: try entering here to choose the current directory, * to apply to all directories, or an absolute path.")
                        return
                    scs_cm.remove_command(args[0] if len(args) >= 1 else None, path)
                commands: dict = {
                    "exit": lambda: exit_pistol(),
                    "cd": lambda: mutable_location.set(args[0], cd_history),
                    "ucd": lambda: undo_cd(),
                    "cdh": lambda: view_cd_history(),
                    "ccdh": lambda: (
                        clear_cd_history(),
                        info("cd history cleared")
                    ),
                    "solo": lambda c: run_solo(c),
                    "clear": lambda: subprocess.run("clear"),
                    "cls": lambda: subprocess.run("clear"),
                    "help": lambda: webbrowser.open("https://github.com/pixilll/pistol/blob/main/README.md"),
                    "version": lambda: info(f"pistol for {PLATFORM} {VERSION}"),
                    "pwsolo": lambda c: (
                        args.insert(0, "pwsh"),
                        args.insert(1, "-Command"),
                        run_solo(c)
                    ),
                    "whereami": lambda: info(f"{disp_loc}{(' ('+str(loc)+')') if str(loc) == str(STORAGE_PATH) else ''}"),
                    "search": lambda: webbrowser.open(args[0]),
                    "st": lambda: st(),
                    "rs": lambda: reverse_search(),
                    "cch": lambda: (
                        clear_command_history(),
                        info("command history cleared")
                    ),
                    "rmc": lambda: remove_from_command_history(),
                    "alias": lambda: aliases.update({args[0]: " ".join([f"\"{arg}\"" for arg in args[1:]])}),
                    "rma": lambda: remove_from_aliases(),
                    "ca": lambda: (
                        clear_aliases(),
                        info("aliases cleared")
                    ),
                    "meta": lambda: analyse(),
                    "prop": lambda: view_property() if args[1] == "check" else set_property(),
                    "re": lambda: (
                        refresh(),
                        info("refreshed meta file")
                    ),
                    "rms": lambda: remove_suggestion(),
                    "cs": lambda: (
                        scs_cm.clear(),
                        info("scs cache cleared")
                    )
                }
                solo_commands: list[str] = [
                    "solo",
                    "pwsolo"
                ]
                original_command: str = command
                if command in aliases.keys():
                    new, _ = parse_command(aliases[command].split(" "))
                    command = new[0]
                    args = new[1:]
                if command not in commands.keys():
                    if meta.fetch("fallback-solo"):
                        if meta.fetch("message-on-fallback"):
                            info(f"fallback: running solo {command+' [from alias '+original_command+']' if original_command in aliases.keys() else full_command} instead")
                        args.insert(0, command)
                        command = "solo"
                    else:
                        error(f"{command} is not a valid command")
                        hint(f"try solo {full_command}")
                        continue
                if command in solo_commands:
                    commands[command](commands)
                else:
                    commands[command]()
                if meta.fetch("auto-re"):
                    refresh()
            except IndexError:
                error(f"not enough arguments supplied for {command}")
        except KeyboardInterrupt:
            print()