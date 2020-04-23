from .ErrorHandler import *
from sys import stderr
from os import path

# Set the filename for use in our exceptions.
fileName = path.basename(__file__)


class ArgumentHandler(object):
    def __init__(self, configHandler):
        self.config = configHandler

    def setToken(self, token):
        """
        Set our authorization token in our configuration data.

        :param token: Our authorization token.
        :return:
        """

        # Load the configuration JSON data.
        self.config.load()

        # Modify the authorization token value.
        self.config.set(token=token)

        # Save the configuration JSON data.
        self.config.write()

    def addOption(self, option):
        """
        Set up our scraper to collect data based on the option given.

        :param option: image, video, embed, sound, link, file
        :return:
        """

        # Determine if option is none.
        if option is None:  # Don't bother continuing if the option isn't set.
            return None

        # Load the configuration JSON data.
        self.config.load()

        # Gather our options array.
        options = self.config.configData['options']

        # Append our new option into the options array.
        options.append(option)

        # Modify the options array value.
        self.config.set(options=options)

        # Save the configuration JSON data.
        self.config.write()

    def delOption(self, option):
        """
        Remove an option from our scraper.

        :param option: image, video, embed, sound, link, file
        :return:
        """

        # Load the configuration JSON data.
        self.config.load()

        # Gather our options array.
        options = self.config.configData['options']

        # Remove our option from the options array.
        options.remove(option)

        # Modify the options array value.
        self.config.set(options=options)

        # Save the configuration JSON data.
        self.config.write()

    def addChannel(self, guildId, channelId, channelName):
        """
        Add a channel to our configuration data.

        :param guildId: The ID of the guild/server we want to scrape.
        :param channelId: The ID of the channel in the guild we want to scrape.
        :param channelName: The name of the channel in the guild we want to scrape.
        :return:
        """

        # Load the configuration JSON data.
        self.config.load()

        # Gather our guilds dictionary.
        guilds = self.config.configData['guilds']

        # Update our guilds dictionary.
        guilds[guildId]['channels'].update({channelId: channelName})

        # Modify the guilds dictionary.
        self.config.set(guilds=guilds)

        # Save the configuration JSON data.
        self.config.write()

    def delChannel(self, guildId, channelId):
        """
        Remove a channel from our configuration data.

        :param guildId: The ID of the guild/server we want to scrape.
        :param channelId: The ID of the channel in the guild we don't want to scrape.
        :return:
        """

        # Load the configuration JSON data.
        self.config.load()

        # Gather our guilds dictionary.
        guilds = self.config.configData['guilds']

        # Remove our channel from the guilds dictionary.
        del guilds[guildId]['channels'][channelId]

        # Modify the guilds dictionary.
        self.config.set(guilds=guilds)

        # Save the configuration JSON data.
        self.config.write()

    def addGuild(self, guildId, guildName):
        """
        Add a guild to our configuration data.

        :param guildId: The ID of the guild/server we want to scrape.
        :param guildName: The name of the guild we want to scrape.
        :return:
        """

        # Load the configuration JSON data.
        self.config.load()

        # Gather our guilds dictionary.
        guilds = self.config.configData['guilds']

        # Add our guild to the guilds dictionary.
        guilds.update({guildId: {'name': guildName, 'channels': {}}})

        # Modify the guilds dictionary.
        self.config.set(guilds=guilds)

        # Save the configuration JSON data.
        self.config.write()

    def delGuild(self, guildId):
        """
        Remove a guild from our configuration data.

        :param guildId: The ID of the guild/server we don't want to scrape.
        :return:
        """

        # Load the configuration JSON data.
        self.config.load()

        # Gather our guilds dictionary.
        guilds = self.config.configData['guilds']

        # Remove our guild from the guilds dictionary.
        del guilds[guildId]

        # Modify the guilds dictionary.
        self.config.set(guilds=guilds)

        # Save the configuration JSON data.
        self.config.write()

    def initialize(self):
        """
        Generate a new configuration JSON file.

        :return:
        """

        try:

            self.config.new(token='', guilds={}, options=[])
            self.setToken(input('Authorization Token: '))

            numGuilds = input('How many guilds/servers are we scraping: ')
            for guildNum in range(int(numGuilds)):
                guildId = input(f'Enter the ID for guild #{guildNum + 1}: ')
                guildName = input(f'Enter the name for guild #{guildNum + 1}: ')
                self.addGuild(guildId, guildName)

                numChannels = input(f'How many channels are we scraping in {guildName}: ')
                for channelNum in range(int(numChannels)):
                    channelId = input(f'Enter the ID for channel #{channelNum + 1}: ')
                    channelName = input(f'Enter the name for channel #{channelNum + 1}: ')
                    self.addChannel(guildId, channelId, channelName)

            self.addOption('embed' if input('Are we scraping embeds [0|1]: ') == '1' else None)
            self.addOption('image' if input('Are we scraping images [0|1]: ') == '1' else None)
            self.addOption('video' if input('Are we scraping videos [0|1]: ') == '1' else None)
            self.addOption('sound' if input('Are we scraping audio  [0|1]: ') == '1' else None)
            self.addOption('file'  if input('Are we scraping files  [0|1]: ') == '1' else None)
            self.addOption('link'  if input('Are we scraping links  [0|1]: ') == '1' else None)

        except Exception as ex:
            message = 'Unable to create a new configuration JSON file.'
            raise RuntimeException('initialize', fileName, lineNumber(self.initialize), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())
