#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- Media Gathering Routines
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

from collections import defaultdict

import os
from datetime import datetime

from quickcolor.color_def import color
from quickcolor.color_filter import strip_ansi_esc_sequences_from_string
from delayviewer.stopwatch import Stopwatch, handle_stopwatch

from .comms_utility import is_server_active

from .media_cfg import MediaConfig
from .server_cfg import ServerConfig

from .paths_and_drives import get_filtered_media_paths
from .search import get_num_titles, extract_search_path_collection

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_all_items_in_search_paths(ipv4 = None, serverType = 'plex', searchPathList = None):
    if not searchPathList:
        searchPathList = get_filtered_media_paths(ipv4 = ipv4, serverType = serverType)

    cmd =''
    for path in searchPathList:
        cmd += "echo \"Drive.path: %s\" ; ls %s ; " % (path, path)

    # retrieve a dictionary list (titles by paths) unfiltered
    return extract_search_path_collection(ipv4 = ipv4, cmd = cmd, getAllGroups = True)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def sort_retrieved_items_by_type(collection):
    sortedCollection = defaultdict(list)

    for path in collection:
        label = os.path.basename(path)
        if collection[path]:
            sortedCollection[label] += collection[path]

    for label in sortedCollection:
        sortedCollection[label].sort()

    return sortedCollection

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_sorted_title_bundles(ipv4 = None, serverType = 'plex'):
    try:
        retrievedTitles = get_all_items_in_search_paths(ipv4 = ipv4, serverType = serverType)

    except Exception as e:
        print(f'{color.CRED2}-- Processing error: Sorted title bundle retrieval ' + \
                f'aborted for items on {color.CWHITE2}{ipv4}{color.CRED2} and ' + \
                f'server type {color.CWHITE}{serverType}\n' + \
                f'{color.CRED2}   Investigate {color.CWHITE}{ipv4}{color.CRED2}' + \
                f'for problems with drive mounts!{color.CEND}')
        return None

    if not retrievedTitles:
        location = str(ipv4) if ipv4 else 'local machine'
        print(f'\n{color.CRED2}-- Did not find any titles in any search path on {color.CYELLOW}{location}{color.CEND}')
        return None

    return sort_retrieved_items_by_type(retrievedTitles)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def show_retrieved_titles(ipv4 = None, serverType = 'plex'):
    if not is_server_active(ipv4 = ipv4):
        print(f'\n{color.CWHITE2}-- Warning: {color.CRED2}Could not reach server ' + \
                f'{color.CYELLOW}{ipv4}{color.CRED2} -- it is dead!{color.CEND}')
        return

    retrievedTitles = []
    try:
        retrievedTitles = get_all_items_in_search_paths(ipv4 = ipv4, serverType = serverType)

    except Exception as e:
        print(f'{color.CRED2}-- Processing error: Title retrieval aborted for items on' + \
                f'{color.CWHITE}{ipv4}{color.CRED2} and server type {color.CWHITE}{serverType}\n' + \
                f'{color.CRED2}   Investigate {color.CWHITE}{ipv4}{color.CRED2} for problems ' + \
                f'with drive mounts!{color.CEND}')
        return

    if not retrievedTitles:
        location = str(ipv4) if ipv4 else "local machine"
        print(f"\n{colors.fg.red}-- Did not find any titles in any search path on {colors.fg.yellow}{location}{colors.off}")
        return

    mc = MediaConfig()

    location = str(ipv4) if ipv4 else "local machine"
    print(f'{color.CGREEN}-- Found {color.CWHITE}{get_num_titles(retrievedTitles)} ' + \
            f'{color.CGREEN}total titles on {color.CWHITE}{location}{color.CEND}')

    numTitles = 0
    for pathIdx, path in enumerate(retrievedTitles):
        _, colorCode = mc.get_color_label(os.path.basename(path))
        colorCode = colorCode if colorCode else color.CVIOLET
        for titleIdx, title in enumerate(retrievedTitles[path]):
            numTitles += 1
            print(f'{color.CVIOLET}{pathIdx:>3}-{titleIdx:<4} - {color.CWHITE}' + \
                    f'{numTitles:>3}. {colorCode}{path}/{title}{color.CEND}')
        # input("Press enter to continue...")

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def show_all_retrieved_titles():
    sc = ServerConfig()

    for name, serverCfg in sc.get_server_list():
        show_retrieved_titles(ipv4 = serverCfg['ipv4'], serverType = serverCfg['serverType'])

        print('-' * 120)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

def get_header_in_collection(area, numTitlesInArea):
    if numTitlesInArea > 1:
        header = f'\n{color.CGREEN}-- There are {color.CWHITE}{numTitlesInArea} {color.CGREEN}titles in the'
    else:
        header = f'\n{color.CGREEN}-- There is {color.CWHITE}{numTitlesInArea} {color.CGREEN}title in the'

    return f'{header} {color.CYELLOW}{area} {color.CGREEN}area{color.CEND}\n'

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

@handle_stopwatch
def show_title_bundles(ipv4 = None, serverType = 'plex', stopwatch = None):
    print()
    stopwatch.start(f'{color.CBLUE2}-- Bundle retrieval in progress ...{color.CEND}')
    sortedCollection = get_sorted_title_bundles(ipv4 = ipv4, serverType = serverType)
    if not sortedCollection:
        stopwatch.stop(f'{color.CRED2}Error in retrieval!{color.CEND}')
        return
    stopwatch.stop()

    mc = MediaConfig()

    for label in sortedCollection:
        print(get_header_in_collection(area = label,
            numTitlesInArea = len(sortedCollection[label])))

        _, colorCode = mc.get_color_label(label)
        colorCode = colorCode if colorCode else color.CRED

        numTitles = 0
        for title in sortedCollection[label]:
            numTitles += 1
            print(f'{color.CWHITE}{numTitles:>3}. {colorCode}{title}{color.CEND}')

        print('-' * 120)

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

@handle_stopwatch
def store_title_bundles(ipv4 = None, serverType = 'plex', storePath = None, stopwatch = None):
    print()
    stopwatch.start(f'{color.CBLUE2}-- Bundle retrieval in progress ...{color.CEND}')
    sortedCollection = get_sorted_title_bundles(ipv4 = ipv4, serverType = serverType)
    if not sortedCollection:
        stopwatch.stop(f'{color.CRED2}Error in retrieval!{color.CEND}')
        return
    stopwatch.stop()

    print(f'{color.CBLUE2}-- Retrieved title bundles from {color.CWHITE}{ipv4}{color.CBLUE2} ', end='', flush=True)

    mc = MediaConfig()

    if not storePath:
        storePath = '/tmp'
    elif not os.path.isdir(storePath):
        storePath = '/tmp'

    fullBundlePath = f'{storePath}/title_bundles_{datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}.txt'
    with open(fullBundlePath, "w") as fileHandle:

        for label in sortedCollection:
            fileHandle.write(strip_ansi_esc_sequences_from_string(get_header_in_collection(area = label,
                numTitlesInArea = len(sortedCollection[label]))) + '\n')

            _, colorCode = mc.get_color_label(label)
            colorCode = colorCode if colorCode else color.CRED

            for idx, title in enumerate(sortedCollection[label]):
                # fileHandle.write(f'{color.CWHITE}{idx+1:>3}. {colorCode}{title}{color.CEND}\n')
                fileHandle.write(f'{idx+1:>3}. {title}\n')

            fileHandle.write('\n')

    print(f'{color.CBLUE2}and storing to {color.CWHITE}{fullBundlePath}{color.CEND}')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

@handle_stopwatch
def store_title_bundles_plex_and_worker(ipv4Plex = None, ipv4Worker = None,
        storePath = None, stopwatch = None):

    print()
    stopwatch.start(f'{color.CBLUE2}-- Plex bundle retrieval in progress ...{color.CEND}')
    sortedCollection_Plex = get_sorted_title_bundles(ipv4 = ipv4Plex, serverType = 'plex')
    if not sortedCollection_Plex:
        stopwatch.stop(f'{color.CRED2}Error in retrieval!{color.CEND}')
        return
    stopwatch.stop()

    stopwatch.start(f'{color.CBLUE2}-- Worker bundle retrieval in progress ...{color.CEND}')
    sortedCollection_Worker = get_sorted_title_bundles(ipv4 = ipv4Worker, serverType = 'worker')
    if not sortedCollection_Worker:
        stopwatch.stop(f'{color.CRED2}Error in retrieval!{color.CEND}')
        return
    stopwatch.stop()

    print(f'{color.CBLUE2}-- Retrieved title bundles from {color.CWHITE}' + \
            f'{ipv4Plex}{color.CBLUE2} and {color.CWHITE}{ipv4Worker}' + \
            f'{color.CBLUE2} ', end='', flush=True)

    mc = MediaConfig()

    if not storePath:
        storePath = '/tmp'
    elif not os.path.isdir(storePath):
        storePath = '/tmp'

    sortedCollection = sortedCollection_Plex | sortedCollection_Worker

    fullBundlePath = f'{storePath}/title_bundles_{datetime.now().strftime("%Y-%m-%d_%H_%M_%S")}.txt'
    with open(fullBundlePath, "w") as fileHandle:
        for label in sortedCollection:
            fileHandle.write(strip_ansi_esc_sequences_from_string(get_header_in_collection(area = label,
                numTitlesInArea = len(sortedCollection[label]))) + "\n")

            for idx, title in enumerate(sortedCollection[label]):
                fileHandle.write(f'{idx+1:>3}. {title}\n')

            fileHandle.write('\n')

    print(f'{color.CBLUE2}and storing to {color.CWHITE}{fullBundlePath}{color.CEND}')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

