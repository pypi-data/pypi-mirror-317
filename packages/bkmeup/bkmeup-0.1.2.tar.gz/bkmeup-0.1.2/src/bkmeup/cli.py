#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI for cleaning __pycache__ nested folders from specified root path
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import os
import sys

from quickcolor.color_def import color
from showexception.showexception import exception_details

from .bkmeup import get_shell_type, get_system_info, running_in_ede
from .bkmeup import create_archive, get_list_of_default_items_to_bkup

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}BkMeUp {color.CWHITE2}Shell Config{color.CYELLOW2} archiver & bkup!{color.CEND}',
                    epilog='-.' * 40)

        parser.add_argument('--version', action="store_true", help='top-level package version')

        subparsers = parser.add_subparsers(dest='cmd')

        p_showEnvInfo = subparsers.add_parser('show.env.info',
                                              help='show system environment info')

        p_showDfltBkupList = subparsers.add_parser('show.dflt.bkup.list',
                                                   help='show list of default items to archive/bkup')

        p_createArchive = subparsers.add_parser('create.archive',
                                                help='accumulate shell config files if they exist and archive them')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if args.version:
            from importlib.metadata import version
            import bkmeup
            print(f'{color.CGREEN}{os.path.basename(sys.argv[0])}{color.CEND} resides in package ' + \
                    f'{color.CBLUE2}{bkmeup.__package__}{color.CEND} ' + \
                    f'version {color.CVIOLET2}{version("bkmeup")}{color.CEND} ...')
            sys.exit(0)

        if args.cmd == 'show.env.info':
            print(f'Currently running in {color.CBLUE2}{get_shell_type()}{color.CEND}!')
            print(f'System info: {color.CCYAN}{get_system_info()}{color.CEND}!')
            if running_in_ede():
                print(f'{color.CYELLOW}This is an EDE based session!{color.CEND}!')

        elif args.cmd == 'show.dflt.bkup.list':
            for idx, item in enumerate(get_list_of_default_items_to_bkup()):
                print(f' --> {idx+1:>2}. {color.CYELLOW}{item}{color.CEND}')

        elif args.cmd == 'create.archive':
            create_archive()

    except Exception as e:
        exception_details(e, "BkMeUp CLI")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

