from .DatetimeHandler import DatetimeHandler
from .ArgumentHandler import ArgumentHandler
from .NetworkHandler import NetworkHandler
from .ConfigHandler import ConfigHandler
from .ErrorHandler import *


class DiscordScraper(object):

    # Is this an alpha build?
    isAlpha = False

    # Is this a beta build?
    isBeta = False

    # Is this a full release?
    isRelease = False

    @staticmethod
    def getCandidate(version):
        """
        Generate the release candidate string based on the current build.

        :param version: The release candidate version.
        :return:
        """

        # Return b for beta, a for alpha, and rc for release candidate.
        return version if DiscordScraper.isRelease       \
            else f'b{version}' if DiscordScraper.isBeta  \
            else f'a{version}' if DiscordScraper.isAlpha \
            else f'rc{version}'


__author__  = 'Dracovian <https://github.com/Dracovian>'
__version__ = { 'major': 0, 'minor': 0, 'candidate': DiscordScraper.getCandidate(0), 'rc': 0 }
__package__ = 'Discord Scraper'


def getVersionString():
    """
    Return the script version in the form of a string.

    :return:
    """

    return f'{__version__["major"]}.{__version__["minor"]}.{__version__["candidate"]}'


def getVersion():
    """
    Return the script version in the form of an integer.

    :return:
    """

    return (__version__["major"] * 1000) + (__version__["minor"] * 100) + __version__["rc"]
