"""

#######################################################################

    Module Name: repl_base
    Description: Base class for REPL tools
    Author: Joseph Bochinski
    Date: 2024-12-16


#######################################################################
"""

# region Imports
from __future__ import annotations

import argparse
import os
import re
import shlex

from dataclasses import dataclass, field
from typing import Any, Callable, Literal

from prompt_toolkit import PromptSession
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from ptpython.repl import embed
from rich.console import Console
from rich.theme import Theme

# endregion Imports


# region Constants

ColorSystem = Literal["auto", "standard", "256", "truecolor", "windows"]
# endregion Constants


# region Classes


def is_num_str(val: str) -> bool:
    return bool(re.match(r"^-?\d+(\.\d+)?$", val))


@dataclass
class ReplTheme(Theme):
    title: str = "bold cyan"
    prompt: str = "bold green"
    warn: str = "bold yellow"
    error: str = "bold red"
    cmd_name: str = "bold green"
    cmd_desc: str = "cyan"
    exit_kw: str = "bold green"
    exit_str: str = "cyan"
    greeting: str = "cyan"
    addl_styles: dict = None

    def __post_init__(self) -> None:
        styles = dict(vars(self))
        extras = styles.pop("addl_styles", {})
        if extras:
            styles.update(extras)
        super().__init__(styles)


@dataclass
class ReplCommand:
    """Class definition for a provided CLI REPL command"""

    command: Callable = None
    help_txt: str = ""
    parser: argparse.ArgumentParser = None
    def_kwargs: dict = field(default_factory=dict)


@dataclass
class ReplBase:
    """Dataclass for CLI options"""

    debug_enabled: bool = None
    """Debug mode enabled"""

    title: str = None
    """Title of the CLI REPL Prompt"""

    exit_keywords: list[str] = None
    """List of strings that cause the REPL to close, defaults to x, q, 
        exit, and quit"""

    init_prompt: str | list[str] = None
    """Prompt to display at startup"""

    color_system: ColorSystem = None
    """Color syste for the rich console"""

    theme: ReplTheme | dict = None

    console: Console = None
    """ Rich Console instance """

    history: str = None
    """Path to the prompt history file"""

    temp_file: str = None
    """Path to prompt temporary file"""

    style: dict | Style = None
    """Style for the prompt"""

    ignore_case: bool = None
    """Ignore case setting for the WordCompleter instance"""

    commands: dict[str, ReplCommand] = None
    """Command dictionary for prompt_toolkit. Keys are command names,
        values are the corresponding description/help text"""

    parent: ReplBase | dict = None

    session: PromptSession = None

    def __post_init__(self) -> None:
        if isinstance(self.commands, dict):
            for cmd_name, cmd in self.commands.items():
                if isinstance(cmd, dict):
                    self.commands[cmd_name] = ReplCommand(**cmd)

        if self.debug_enabled is None:
            self.debug_enabled = False

        self.title = self.title or "CLI Tool"

        self.exit_keywords = self.exit_keywords or ["x", "q", "exit", "quit"]

        exit_kw_str = ", ".join(
            f'[exit_kw]"{kw}"[/exit_kw]' for kw in self.exit_keywords
        )
        exit_kw_pref = "Type one of " if len(self.exit_keywords) > 1 else "Type "
        exit_str = f"[exit_str]{exit_kw_pref}{exit_kw_str} to exit[/exit_str]"

        self.init_prompt = self.init_prompt or [
            f"[title]<<| {self.title} |>>[/title]",
            exit_str,
            '[greeting]Type [cmd_name]"help"[/cmd_name] to view available commands.[/greeting]',
        ]

        self.color_system = self.color_system or "truecolor"

        if isinstance(self.theme, dict):
            props = list(dict(vars(ReplTheme())).keys())
            init = {"addl_styles": {}}
            for key, value in self.theme.items():
                if key in props:
                    init[key] = value
                else:
                    init["addl_styles"][key] = value

            self.theme = ReplTheme(**init)
        elif self.theme is None:
            self.theme = ReplTheme()

        self.console = Console(color_system=self.color_system, theme=self.theme)

        self.history = self.history or os.path.expanduser(
            "~/.config/.prompt_history"
        )

        if self.history:
            hist_dir = os.path.dirname(self.history)
            if not os.path.exists(hist_dir):
                os.makedirs(hist_dir, exist_ok=True)

        self.temp_file = self.temp_file or os.path.expanduser(
            "~/.config/.prompt_tmp"
        )

        if self.temp_file:
            temp_dir = os.path.dirname(self.temp_file)
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir, exist_ok=True)

        self.style = self.style or {
            "prompt": "bold green",
            "": "default",
        }
        if isinstance(self.style, dict):
            self.style = Style.from_dict(self.style)

        self.apply_def_cmds()

    def apply_def_cmds(self) -> None:
        """Add the descriptions for the help and exit commands"""
        base_cmds: dict[str, ReplCommand] = {
            "\\[help, h]": ReplCommand(help_txt="Display this help message again"),
        }
        if self.exit_keywords:
            exit_str = ", ".join(self.exit_keywords)
            base_cmds.update(
                {
                    f"\\[{exit_str}]": ReplCommand(help_txt="Exit tool"),
                }
            )

        self.commands = self.commands or {}
        base_cmds.update(self.commands)
        self.commands = base_cmds

    def get_cmd_names(self) -> list[str]:
        """Retrieve names of commands, parsing out the help/exit commands"""

        help_str = "[help, h]"
        exit_str = f'[{", ".join(self.exit_keywords)}]'
        names: list[str] = [
            name
            for name in self.commands.keys()
            if name not in [help_str, exit_str]
        ]
        names.extend(["help", "h"])
        names.extend(self.exit_keywords)
        return names

    def print(self, *args) -> None:
        """Shortcut to console.print"""
        self.console.print(*args)

    def input(self, *args, suggestions: AutoSuggest = None) -> str:
        """Shortcut to console.input"""
        if self.session:
            return self.session.prompt(*args, auto_suggest=suggestions)
        return self.console.input(*args)

    def input_int(self, *args) -> int:
        """Parse input as int"""

        user_input = self.input(*args).strip().split(".")[0].strip()
        if is_num_str(user_input):
            return int(user_input)

    def input_bool(self, *args, true_list: list[str] = None) -> int:
        """Parse input as bool"""
        true_list = true_list or ["y", "yes"]
        true_list = [val.lower() for val in true_list]

        user_input = self.input(*args)
        return user_input.strip().lower() in true_list

    def input_prefer_int(self, *args) -> int | str:
        """Parse input as int if possible, otherwise return the string"""

        user_input = self.input(*args).strip().split(".")[0].strip()
        if is_num_str(user_input):
            return int(user_input)
        return user_input

    def input_choice(self, *args, choices: list[str]) -> str:
        """Prompt for a choice from a list of options"""
        for idx, choice in enumerate(choices):
            self.print(f"[{idx+1}]: {choice}")
        choice = self.input_int(*args)
        if choice and choice > 0 and choice <= len(choices):
            return choices[choice - 1]

    def input_choice_dict(self, prompt: str, choices: dict) -> Any:
        """Similar to input_choice, but with more control over the options

        Args:
            prompt (str): String to print to the user
            choices (dict): Dict of choices; keys will be the displayed options, values will be the associated return value

        Returns:
            Any: Selected value
        """

        keys = list(choices.keys())
        for idx, choice in enumerate(keys):
            self.print(f"[{idx+1}]: {choice}")

        choice = self.input_int(prompt)
        if choice and choice > 0 and choice <= len(keys):
            key = keys[choice]
            return choices[key]

    def debug(self, *args) -> None:
        """Print only if debug_enabled == True"""
        if self.debug_enabled:
            self.print(*args)

    def add_command(
        self,
        cmd_name: str,
        cmd_func: Callable = None,
        help_txt: str = "",
        use_parser: bool = False,
        description: str = "",
        # auto_suggest: AutoSuggest,
        **def_kwargs,
    ) -> ReplCommand:
        """Add a command to the REPL

        Args:
            cmd_name (str): Name of the command
            cmd_func (Callable, optional): Function to execute when called.
                Defaults to None.
            help_txt (str, optional): Help text to display from REPL help command.
                Defaults to "".
            use_parser (bool, optional): If true, adds an argparse.ArgumentParser
                to the new ReplCommand instance. Defaults to False.
            description (str, optional): Optional description for the
                ArgumentParser help text. Defaults to help_txt.
            def_args: Default arguments for the command function
            def_kwargs: Default keyword arguments for the command function

        Returns:
            ReplCommand: The new ReplCommand instance
        """

        new_cmd = ReplCommand(command=cmd_func, help_txt=help_txt)
        if use_parser:
            new_cmd.parser = argparse.ArgumentParser(
                description=description or help_txt
            )
        if def_kwargs:
            new_cmd.def_kwargs = def_kwargs

        self.commands[cmd_name] = new_cmd
        return new_cmd

    def interactive(self, *args, **kwargs) -> None:
        """Starts an interactive session from within the class"""
        if kwargs:
            globals().update(kwargs)
        embed(globals(), locals())

    def show_help(self) -> None:
        """Print out the provided help text"""

        for cmd_name, cmd in self.commands.items():
            self.print(
                f"[cmd_name]{cmd_name}:[/cmd_name] [cmd_desc]{cmd.help_txt}[/cmd_desc]"
            )

    def print_prompt(self) -> None:
        """Prints the prompt message if defined"""

        if isinstance(self.init_prompt, list):
            for line in self.init_prompt:
                self.print(line)
        else:
            self.print(self.init_prompt)

    def run(self) -> None:
        """Initiates a REPL with the provided configuration"""

        completer = WordCompleter(
            self.get_cmd_names(), ignore_case=self.ignore_case
        )

        self.session = PromptSession(
            completer=completer,
            style=self.style,
            history=FileHistory(self.history),
            tempfile=self.temp_file,
            auto_suggest=SuggestFromLs,
        )

        self.print_prompt()

        while True:
            try:
                user_input = self.session.prompt("> ", complete_while_typing=True)

                if user_input.lower() in ["help", "h"]:
                    self.show_help()
                elif user_input.lower() in self.exit_keywords:
                    self.print(f"[warn]Exiting REPL ({self.title})...[/warn]")
                    break
                else:
                    args = shlex.split(user_input)
                    if not args:
                        self.print("[warn][WARNING]: No command provided[/warn]")
                        continue

                    cmd = self.commands.get(args[0])

                    if not cmd:
                        self.print("[warn][WARNING]: Invalid command[/warn]")
                        continue

                    cmd_args = args[1:]
                    if cmd.command:
                        if cmd.parser:
                            if cmd_args and cmd_args[0] in [
                                "help",
                                "h",
                                "-h",
                                "--help",
                            ]:
                                cmd.parser.print_help()
                                continue

                            cmd.command(cmd.parser.parse_args(cmd_args))
                        else:
                            if cmd.def_kwargs:
                                cmd.command(*cmd_args, **cmd.def_kwargs)
                            else:
                                cmd.command(*cmd_args)
                    else:
                        self.print(
                            "[warn][WARNING]: No function provided for command[/warn]"
                        )
            except (EOFError, KeyboardInterrupt):
                self.print(f"[warn]Exiting REPL ({self.title})...[/warn]")
                break

        if self.parent:
            self.parent.print_prompt()


class SuggestFromLs(AutoSuggest):

    def get_suggestion(
        self, buffer: Buffer, document: Document
    ) -> Suggestion | None:
        files = os.listdir()

        # Consider only the last line for the suggestion.
        text = document.text.rsplit("\n", 1)[-1]

        if text.strip():
            for item in files:
                if item.lower().startswith(text.lower()):
                    return Suggestion(item[len(text) :])
        return None


@dataclass
class TestRepl(ReplBase):
    def __post_init__(self) -> None:
        super().__post_init__()
        self.add_command("test_cmd", self.test_cmd, help_txt="Test command")

    def test_cmd(self) -> None:
        user_input = self.input("Testing prompt: ", suggestions=SuggestFromLs())
        self.print(user_input)


# endregion Classes


# region Functions

# endregion Functions
