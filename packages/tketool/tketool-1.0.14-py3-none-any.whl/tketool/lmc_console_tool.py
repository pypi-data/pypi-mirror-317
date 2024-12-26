# pass_generate pass_doc
import argparse
from tketool.cmd_utils import *
from tketool.lmc.table_auto.cmd_util import *


def main():
    parser = argparse.ArgumentParser(description="A simple command line tool")
    commands = {}

    # Only create subparsers once
    subparsers = parser.add_subparsers(dest="command", help='Commands')

    add_cmd(subparsers, execute_excel, commands)

    args = parser.parse_args()

    if args.command in commands:
        command_params = inspect.signature(commands[args.command]).parameters
        params = {name: getattr(args, name, None) for name in command_params}
        commands[args.command](**params)
    else:
        parser.print_help()
