#!/usr/bin/env python3
# ------------------------------------------------------------------------------------------------------
# -- shell config backup and archive
# ------------------------------------------------------------------------------------------------------
# ======================================================================================================

import os
import tarfile

from datetime import datetime
from pathlib import Path

from quickcolor.color_def import color
from delayviewer.spinner import handle_spinner

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

defaultBkupItems_Common : list = [ '.config/coreCfg', '.config/tilix/schemes',
                                  '.local/share/fonts',
                                  '.colordiffrc', '.dircolors',
                                  '.gitconfig', '.jfrog', '.netrc', '.pypirc',
                                  '.scripts', '.ssh', '.vim', '.vimrc' ]

defaultBkupItems_Zsh : list = [ '.zshrc', '.zprofile', '.zshenv', '.p10k.zsh' ]

defaultBkupItems_Bash : list = [ '.bashrc', '.profile', '.bash_profile' ]

# ------------------------------------------------------------------------------------------------------

def running_in_ede() -> bool:
    return os.path.exists('/etc/ede/ede_version')

def get_ede_version() -> str:
    with open('/etc/ede/ede_version', 'r') as f:
        edeVersion = f.read()

    return f'_{edeVersion}'

# ------------------------------------------------------------------------------------------------------

def get_shell_type() -> str:
    return os.path.basename(os.path.realpath(f'/proc/{os.getppid()}/exe'))

# ------------------------------------------------------------------------------------------------------

def get_linux_system_info() -> str:
    import distro
    osRelInfo = distro.os_release_info()
    return f'{osRelInfo["name"].replace(" ", "_")}_{osRelInfo["version_id"]}'

def get_macos_system_info() -> str:
    # need better mechanism of determining OS type and version
    return 'MacOS'

# ------------------------------------------------------------------------------------------------------

def get_system_info() -> str:
    import platform
    machineName = platform.node()
    shellType = get_shell_type()
    prefix = f'{machineName}_{shellType}'

    if running_in_ede():
        prefix = f'{prefix}_ede_{get_ede_version()}'

    if platform.system().lower() == 'linux':
        return f'{prefix}_{get_linux_system_info()}'
    elif platform.system().lower() == 'darwin':
        return f'{prefix}_{get_darwin_system_info()}'
    else:
        raise ValueError(f'Unexpected system type: {platform.system().lower()}')

# ------------------------------------------------------------------------------------------------------

def extract_list_of_items_to_bkup(inputFilePaths: list) -> list:
    existingFilePaths: list = []

    os.chdir(Path.home())
    for item in inputFilePaths:
        if os.path.exists(item):
            existingFilePaths.append(item)

    return existingFilePaths

# ------------------------------------------------------------------------------------------------------

def get_list_of_default_items_to_bkup() -> list:
    shellType = get_shell_type()
    if shellType == 'zsh':
        shellSpecificList = defaultBkupItems_Zsh
    elif shellType == 'bash':
        shellSpecificList = defaultBkupItems_Bash
    else:
        raise ValueError(f'Running in an unexpected shell type ({shellType})')

    return extract_list_of_items_to_bkup(defaultBkupItems_Common + shellSpecificList)

# ------------------------------------------------------------------------------------------------------

def filter_exclusions(tarinfo):
    pathToHome = Path.home()
    defaultExcludedStartWith = [ '.ssh/known_hosts', '.vim/plugged', '__pycache__' ]

    for excluded in defaultExcludedStartWith:
        if tarinfo.name.startswith(excluded):
            return None

    return tarinfo

# ------------------------------------------------------------------------------------------------------

@handle_spinner
def create_archive(spinner = None):
    spinner.start(f' --> Getting {color.CGREEN2}list of default items{color.CEND} to backup...')
    bkupItems = get_list_of_default_items_to_bkup()
    spinner.stop()

    spinner.start(f' --> {color.CBLUE2}Archiving {color.CEND}...')
    archiveName = f'{get_system_info()}_bkup_all_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.tgz'
    with tarfile.open(archiveName, 'w:gz') as tf:
        for item in bkupItems:
            tf.add(item, filter = filter_exclusions)
    spinner.stop()

    print(f' --> Created {color.CGREEN}{archiveName}{color.CEND}!')

# ------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------

