import cmd
import sys


class PromptCLI(cmd.Cmd):
    intro = "\033[1;32mWelcome to the Beautiful CLI! Type 'help' or '?' for a list of commands.\033[0m"
    prompt = "\033[1;34mYou: \033[0m"  # Blue and bold prompt
    file = None

    def do_exit(self, arg):
        """Exit the CLI."""
        print("\033[1;31mGoodbye!\033[0m")  # Red text
        return True

    def do_history(self, arg):
        """Show the command history."""
        print("\033[1;33mCommand History:\033[0m")  # Yellow text
        for i, command in enumerate(self._get_history(), start=1):
            print(f"{i}: {command}")

    def default(self, line):
        """Handle unrecognized commands."""
        print(f"\033[1;35mBot:\033[0m {line}")  # Magenta text

    def _get_history(self):
        """Retrieve command history."""
        return self._hist or []

    def precmd(self, line):
        """Record history before executing the command."""
        if not hasattr(self, "_hist"):
            self._hist = []
        if line.strip():
            self._hist.append(line)
        return line

    def do_echo(self, arg):
        """Echo back the input."""
        print(f"\033[1;36mYou said:\033[0m {arg}")  # Cyan text

    def do_clear(self, arg):
        """Clear the screen."""
        print("\033c", end="")
