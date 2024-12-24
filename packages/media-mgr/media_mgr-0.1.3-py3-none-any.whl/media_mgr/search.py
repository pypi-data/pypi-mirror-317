#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Search Methods
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from collections import defaultdict

import subprocess
import os
import re

from quickcolor.color_def import color

from .comms_utility import run_cmd, is_server_active, group_list

from .media_cfg import MediaConfig
from .server_cfg import ServerConfig

from .paths_and_drives import get_filtered_media_paths

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_num_titles(collection = None):
    numTitles = 0
    for path in collection:
        numTitles += len(collection[path])

    return numTitles

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def extract_search_path_collection(ipv4: str | None = None,
        cmd: str | None = None, getAllGroups: bool = False):
    collection = defaultdict(list)

    cmdOutput = run_cmd(ipv4, cmd)
    if isinstance(cmdOutput, subprocess.CompletedProcess):
        if cmdOutput.returncode:
            raise ValueError(f'Warning: Problem retrieving command output!')

    medium = list(group_list(cmdOutput, 'Drive.path: '))

    for drivePathContents in medium:
        if not drivePathContents:
            continue
        groupId, groupContents = drivePathContents[:1], drivePathContents[1:]
        groupIdStr=''
        for groupIdElement in groupId:
            groupIdStr += groupIdElement

        dumpIt, groupLabel = groupIdStr.split(' ')
        if groupContents or getAllGroups:
            collection[groupLabel] = groupContents

    return collection

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_matching_items_in_search_paths(ipv4: str | None = None,
        searchPathList: list | None = None, searchTerms : list | None = None):
    searchRegex = ''
    for term in searchTerms:
        searchRegex += term + '.*'

    cmd = ''
    for path in searchPathList:
        cmd += f'echo \"Drive.path: {path}\" ; ls {path} | grep -i \'{searchRegex}\' ; '

    return extract_search_path_collection(ipv4, cmd)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def find_items_in_search_paths(ipv4: str | None = None, serverType = 'plex',
        searchPathList: list | None = None, searchTerms: list | None = None):
    if not is_server_active(ipv4 = ipv4):
        return defaultdict(list)

    if not searchPathList:
        searchPathList = get_filtered_media_paths(ipv4 = ipv4, serverType = serverType)

    collection = get_matching_items_in_search_paths(ipv4 = ipv4,
            searchPathList = searchPathList, searchTerms = searchTerms)

    # create a matched dictionary list (titles by paths)
    # filtering paths with matching titles (no empty paths)
    matched = defaultdict(list)
    for path in collection:
        if collection[path]:
            matched[path] = collection[path]

    return matched

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def show_matched_titles(ipv4: str | None = None,
        serverType = 'plex', searchTerms: list = ["the", "duff"]):

    location = str(ipv4) if ipv4 else "local machine"

    matched = []
    try:
        matched = find_items_in_search_paths(ipv4 = ipv4,
                serverType = serverType, searchTerms = searchTerms)

    except Exception as e:
        print(f'{color.CRED2}-- Processing error: Search aborted for titles ' + \
                f'matching {color.CWHITE}--> {color.CYELLOW}{" ".join(searchTerms)}' + \
                f'{color.CWHITE}<-- {color.CRED2}on {color.CWHITE}{location}\n' + \
                f'{color.CRED}   Investigate {color.CWHITE}{location}{color.CRED2} ' + \
                f'for problems with drive mounts!{color.CEND}' + \
                f'\n{e}')
        return

    if not matched:
        print(f'{color.CRED2}-- Did not find any titles matching ' + \
                f'{color.CWHITE}--> {color.CYELLOW}{" ".join(searchTerms)} ' + \
                f'{color.CWHITE}<-- {color.CRED2}on {color.CWHITE}{location}{color.CEND}')
        return

    mc = MediaConfig()
    print(f'{color.CGREEN}-- Found {color.CWHITE}{get_num_titles(matched)} ' + \
            f'{color.CGREEN}titles matching {color.CWHITE}--> {color.CYELLOW}' + \
            f'{" ".join(searchTerms)} {color.CWHITE}<-- {color.CGREEN}on ' + \
            f'{color.CWHITE}{location}{color.CEND}')

    numTitlesMatched = 0
    for path in matched:
        _, colorCode = mc.get_color_label(os.path.basename(path))
        colorCode = colorCode if colorCode else color.CRED
        for title in matched[path]:
            numTitlesMatched += 1
            print(f'{color.CWHITE}{numTitlesMatched:>3}. {colorCode}{path}/{title}{color.CEND}')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def show_all_matched_titles(searchTerms: list | None = None):
    srv = ServerConfig()

    for server in srv.get_server_name_list():
        show_matched_titles(ipv4 = srv.get_server_address(serverLabel = server),
                serverType = srv.get_server_type(serverLabel = server),
                searchTerms = searchTerms)
        print('=' * 100)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

