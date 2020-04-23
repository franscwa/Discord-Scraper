from .ConfigHandler import ConfigHandler
from .ErrorHandler import CustomError
from .DatetimeHandler import *
from .NetworkHandler import *


class DiscordScraper(object):
    isAlpha = False
    isBeta = False
    isRelease = False

    @staticmethod
    def getCandidate(version):
        return version if DiscordScraper.isRelease \
            else f'b{version}' if DiscordScraper.isBeta \
            else f'a{version}' if DiscordScraper.isAlpha \
            else f'rc{version}'


__author__  = 'Dracovian <https://github.com/Dracovian>'
__version__ = { 'major': 0, 'minor': 0, 'candidate': DiscordScraper.getCandidate(0), 'rc': 0 }
__package__ = 'Discord Scraper'


def getVersionString():
    return f'{__version__["major"]}.{__version__["minor"]}.{__version__["candidate"]}'


def getVersion():
    return (__version__["major"] * 1000) + (__version__["minor"] * 100) + __version__["rc"]
