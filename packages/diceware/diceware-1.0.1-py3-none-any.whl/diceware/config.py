#  diceware -- passphrases to remember
#  Copyright (C) 2015-2024  Uli Fouquet
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""config -- diceware configuration

`diceware` is configurable via commandline, configuration files and
direct API calls.

"""
import os
import re
from configparser import ConfigParser as SafeParser


OPTIONS_DEFAULTS = dict(
    num=6,
    caps=True,
    specials=0,
    delimiter="",
    randomsource="system",
    verbose=0,
    wordlist=["en_eff"],
    dice_sides=6,
    )


#: valid wordlist names
RE_WLIST_NAME = re.compile(r'(?![\w\-]+).')


def valid_locations():
    """The list of valid paths we look up for config files.

    We search for config files in the following locations (in that order):

    1a) dirs in colon-separated var $XDG_CONFIG_DIRS
    1b) /etc/xdg/diceware/diceware.ini  # if $XDG_CONFIG_DIRS is undefined
    2a) $XDG_CONFIG_HOME/diceware/diceware.ini  # if $XDG_CONFIG_HOME is defined
    2b) $HOME/.config/diceware/diceware.ini  # if $HOME is defined but not $XDG_CONFIG_HOME

    Finally we look also for:

    3) ~/.diceware.ini

    Later read configs override prior ones. Therefore an existing
    `~/.diceware.ini` contains values that cannot be overridden, except on
    commandline.
    """
    result = []
    user_home = os.path.expanduser("~")
    if user_home != "~":
        result.append(os.path.join(user_home, ".diceware.ini"))
    xdg_dirs = os.getenv("XDG_CONFIG_DIRS", os.path.normcase("/etc/xdg"))
    if os.getenv("XDG_CONFIG_HOME") or os.getenv("HOME"):
        xdg_dirs = (
            os.getenv("XDG_CONFIG_HOME", os.path.join(os.getenv("HOME", ""), ".config"))
            + ":"
            + xdg_dirs
        )
    result.extend(
        [os.path.join(x, "diceware", "diceware.ini") for x in xdg_dirs.split(":")]
    )
    result.reverse()
    return result


def get_configparser(path_list=None):
    """Parse `path_list` for config values.

    If no list is given we use `valid_locations()`.

    Return a list of paths read and a config parser instance.
    """
    if path_list is None:
        path_list = valid_locations()
    parser = SafeParser()
    found = parser.read(path_list)
    return found, parser


def string_to_wlist_list(text):
    """Split string into list of valid wordlist names.
    """
    return [name for name in re.split(RE_WLIST_NAME, text) if name != ""]


def get_config_dict(
        path_list=None, defaults_dict=OPTIONS_DEFAULTS, section="diceware"):
    """Get config values found in files from `path_list`.

    Read files in `path_list` config files and return option values from
    section `section` as regular dictionary.

    We only accept values for which a default exists in
    `defaults_dict`. If `defaults_dict` is ``None`` we use
    ``OPTIONS_DEFAULTS``.

    Values are interpolated to have same value type as same-named values
    from `defaults_dict` if they are integers or boolean.

    String/text values are stripped from preceding/trailing quotes
    (single and double).
    """
    result = dict(defaults_dict)
    found, parser = get_configparser(path_list)
    for key, val in defaults_dict.items():
        if not parser.has_option(section, key):
            continue
        if isinstance(val, bool):
            result[key] = parser.getboolean(section, key)
        elif isinstance(val, int):
            result[key] = parser.getint(section, key)
        elif key == "wordlist":
            result[key] = string_to_wlist_list(parser.get(section, key))
        else:
            result[key] = parser.get(section, key).strip("\"'")
    return result
