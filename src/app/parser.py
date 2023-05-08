__author__ = "Jonty Doyle"
__email__ = "dyljon001@myuct.ac.za"
__date__ = "23 September 2022"

from pathlib import Path


class Parser:
    """Parses and handles commands provided to the environment through text.
    Contains a primitive interpreter handling provided environment commands,
    Used predominantly in the Console."""

    def __init__(self, env):
        self.env = env
        self.COMMANDS = self.__fetch_commands()

    def __fetch_commands(self):
        commands = dict()

        # Gets all public methods of environment (i.e load, save etc.)
        for item in dir(self.env):
            attr = getattr(self.env, item)
            private = item.startswith('__') or item.startswith('_')

            if callable(attr) and not private:
                commands[item] = Command(item, attr)

        return commands

    def complete(self, text):
        matches = []
        args = text.split(' ')
        candidate_text = args[-1]

        # If incoming text is command, search commands
        if len(args) == 1:
            for command in self.COMMANDS.keys():
                if command.startswith(candidate_text):
                    matches.append(command)

        # If text are params of command (static handling in method)
        elif args[0] in self.COMMANDS:
            command = args[0]
            if len(args) <= self.COMMANDS[command].argv:
                matches = self.__complete_command(command, text)
        # Only return if one match
        if len(matches) == 1:
            if len(args) == 1:
                completed_text = matches[-1] + ' '
            else:
                completed_text = f'{" ".join(args[:-1])} {matches[-1]}'
            return completed_text
        else:
            return text

    def __complete_command(self, command, text):
        matches = []
        args = text.split(' ')
        candidate_text = args[-1]

        if 'load' in command:
            for env in self.env.envs:
                if env.startswith(candidate_text):
                    matches.append(env)

        elif 'open' in command:
            p = Path('.')
            candidate_path = p / candidate_text
            if candidate_path.parent.is_dir():
                for path in candidate_path.parent.iterdir():
                    if path.name.startswith(candidate_path.name):
                        try:
                            return_path = path.relative_to(p)
                        except ValueError:
                            return_path = path

                        if path.is_dir():
                            matches.append(f'{return_path}/')
                        else:
                            matches.append(f'{return_path}')

        return matches

    def parse(self, text) -> str:
        args = text.split(' ')
        input = args[0]

        if len(args) > 1:
            params = args[1:]
        else:
            params = []

        if input in self.COMMANDS:
            command = self.COMMANDS[input]
            output = command.run(*params)
        elif (input == 'help' or input == '?'):
            output = self.__help(*params)
        else:
            output = f'ERROR: Command "{input}" not found'

        # Returns command output + error code (0 or 1)
        if 'ERROR' in output or output is None:
            return (output, 1)
        else:
            return (output, 0)

    def __help(self, *params):
        if params:
            input = params[0]
            if input in self.COMMANDS:
                c = self.COMMANDS[input]
                return f'{c.name}: {c.help} {c.usage}'
            else:
                return f'Command "{input}" not found'

        else:
            help = 'Type "help [command]" for further information.'
            commands = ", ".join(self.COMMANDS.keys())
            return f'Avaliable Commands: {commands}. {help}'


class Command:

    def __init__(self, name, function):
        self.name = name
        self.__run = function
        self.usage, self.help = self.__handle_doc(function)
        self.argv = len(self.usage.split(' ')) - 1

    def run(self, *args):
        output = self.__run(*args)

        if output is None:
            return self.usage
        else:
            return output

    def __handle_doc(self, function):
        docs = function.__doc__.split('\n')

        help = docs[0]
        usage = docs[1].strip(' ')

        return usage, help
