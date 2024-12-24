#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- CLI Methods for Search
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

# PYTHON_ARGCOMPLETE_OK
import argcomplete, argparse

import json
import os
import sys

from quickcolor.color_def import color
from showexception.showexception import exception_details

from ..search import show_matched_titles, show_all_matched_titles

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CYELLOW2}Search {color.CEND}for media manager',
                    epilog='-.' * 40)

        parser.add_argument('-d', '--debug', action="store_true",
                help='run with debug hooks enabled')

        parser.add_argument('--version', action="store_true", help='top-level package version')

        subparsers = parser.add_subparsers(dest='cmd')

        p_showMatchedTitles = subparsers.add_parser('show.match', help='show matched titles')
        p_showMatchedTitles.add_argument('--ipv4', default=None, metavar='<ipv4.addr>', help='Server IPV4')
        p_showMatchedTitles.add_argument('--type', default='plex',
                metavar='<srvType>', choices=['plex', 'worker'], help='Server types')
        p_showMatchedTitles.add_argument("terms", metavar='<term_1> .. <term_n>', nargs=argparse.REMAINDER,
                help='Search terms to match')

        p_showAllMatchedTitles = subparsers.add_parser('show.all.matches', help='show matched titles from all servers')
        p_showAllMatchedTitles.add_argument("terms", metavar='<term_1> .. <term_n>', nargs='*',
                help='Search terms to match')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.version:
            from importlib.metadata import version
            import media_mgr
            print(f'{color.CGREEN}{os.path.basename(sys.argv[0])}{color.CEND} resides in package ' + \
                    f'{color.CBLUE2}{media_mgr.__package__}{color.CEND} ' + \
                    f'version {color.CVIOLET2}{version("media_mgr")}{color.CEND} ...')
            sys.exit(0)

        if args.cmd == 'show.match':
            show_matched_titles(ipv4 = args.ipv4, serverType = args.type,
                    searchTerms = args.terms)

        elif args.cmd == 'show.all.matches':
            show_all_matched_titles(searchTerms = args.terms)

    except Exception as e:
        exception_details(e, "Search CLI")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def cli_search_plex():
    try:
        parser = argparse.ArgumentParser(
                    description=f'{"-." * 3}  {color.CBLUE2}Search {color.CYELLOW2}All Servers {color.CEND}utility',
                    epilog='-.' * 40)

        parser.add_argument('--version', action="store_true", help='top-level package version')

        parser.add_argument("terms", metavar='<term_1> .. <term_n>', nargs='*',
                help='Search terms to match')

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        # print(args)

        if len(sys.argv) == 1:
            parser.print_help(sys.stderr)
            sys.exit(1)

        if args.version:
            from importlib.metadata import version
            import media_mgr
            print(f'{color.CGREEN}{os.path.basename(sys.argv[0])}{color.CEND} resides in package ' + \
                    f'{color.CBLUE2}{media_mgr.__package__}{color.CEND} ' + \
                    f'version {color.CVIOLET2}{version("media_mgr")}{color.CEND} ...')
            sys.exit(0)

        show_all_matched_titles(searchTerms = args.terms)

    except Exception as e:
        exception_details(e, "Search All Servers CLI")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

