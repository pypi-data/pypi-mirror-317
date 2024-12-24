import sys

from plutonkit.config.command import ACTIONS


class Help:
    def __init__(self, argv) -> None:
        self.argv = argv

    def comment(self):
        return "To see all available commands"

    def execute(self):
        template = "Here are the available commands you can used\nCommands:\n"
        len_str = 0
        for key, val in ACTIONS.items():
            if len_str < len(key):
                len_str = len(key)+1

        for key, val in ACTIONS.items():
            split_space = "".join([ "." for _ in range(0, len_str - len(key))])
            template += f" ({key}) {split_space} {val.comment()}\n"
        print(template)
        sys.exit(0)
