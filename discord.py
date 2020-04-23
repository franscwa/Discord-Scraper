from DiscordScraper import ConfigHandler, DatetimeHandler, NetworkHandler, NetworkHeader, CustomError
from os import makedirs, getcwd, path
from inspect import findsource
from sys import stderr


def setToken(configHandler, token):
    configHandler.load()
    configHandler.set(token=token)
    configHandler.write()


def setOption(configHandler, option, value):
    configHandler.load()

    options = configHandler.configData['options']
    options.update({option: value})

    configHandler.set(options=options)
    configHandler.write()


def delChannel(configHandler, guildID, channelID):
    configHandler.load()

    guilds = configHandler.configData['guilds']
    del guilds[guildID]['channels'][channelID]

    configHandler.set(guilds=guilds)
    configHandler.write()


def addChannel(configHandler, guildID, channelID, channelName):
    configHandler.load()

    guilds = configHandler.configData['guilds']
    guilds[guildID]['channels'].update({channelID: channelName})

    configHandler.set(guilds=guilds)
    configHandler.write()


def delGuild(configHandler, guildID):
    configHandler.load()

    guilds = configHandler.configData['guilds']
    del guilds[guildID]

    configHandler.set(guilds=guilds)
    configHandler.write()


def addGuild(configHandler, guildID, guildName):
    configHandler.load()

    guilds = configHandler.configData['guilds']
    guilds.update({guildID: {'name': guildName, 'channels': {}}})

    configHandler.set(guilds=guilds)
    configHandler.write()


def initialize(configHandler):
    try:
        configHandler.new(token='', channels={}, options={})
        setToken(configHandler, input('Authorization Token: '))

        numGuilds = input('How many guilds/servers are we scraping: ')
        for guildNum in range(int(numGuilds)):
            guildID = str(input(f'Enter the ID for Guild #{guildNum + 1}: '))
            guildName = str(input(f'Enter the name for Guild #{guildNum + 1}: '))
            addGuild(configHandler, guildID, guildName)

            numChannels = input(f'How many channels are we scraping in {guildName}: ')
            for channelNum in range(int(numChannels)):
                channelID = str(input(f'Enter the ID for Channel #{channelNum + 1}: '))
                channelName = str(input(f'Enter the name for Channel #{channelNum + 1}: '))
                addChannel(configHandler, guildID, channelID, channelName)

        setOption(configHandler, 'nsfw',   int(input('Are we scraping NSFW data [0|1]: ')))
        setOption(configHandler, 'embeds', int(input('Are we scraping embedded data [0|1]: ')))
        setOption(configHandler, 'images', int(input('Are we scraping image data [0|1]: ')))
        setOption(configHandler, 'sounds', int(input('Are we scraping sound data [0|1]: ')))
        setOption(configHandler, 'links',  int(input('Are we scraping hyperlinks [0|1]: ')))
        setOption(configHandler, 'files',  int(input('Are we scraping user files [0|1]: ')))
        setOption(configHandler, 'texts',  int(input('Are we scraping user posts [0|1]: ')))

    except ( ValueError, TypeError ) as e:
        raise CustomError(e, 'Discord', findsource(initialize)[1], 'initialize', [configHandler])

    except CustomError as ce:
        stderr.write(ce.getMessage())


def downloadFile(url, networkHeader, filepath, filename):
    try:
        file = path.join(filepath, filename)
        if path.isfile(file):
            return None

        networkHandler = NetworkHandler()
        networkHandler.set(url=url)

        with open(file, 'wb') as fstream:
            fstream.write(networkHandler.download(networkHandler, networkHeader, True).raw.read())

    except ( ValueError, TypeError ) as e:
        raise CustomError(e, 'Discord', findsource(downloadFile)[1], 'downloadFile', [url, networkHeader, filepath, filename])

    except CustomError as ce:
        stderr.write(ce.getMessage())


def start(configHandler):
    configHandler.load()

    networkHeaders = {
        'authorization': configHandler.configData['token'],
        'referer': 'https://discordapp.com/channels/{}/{}',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.10 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36'
    }

    yearRange = DatetimeHandler.getRange(2015, DatetimeHandler.getToday().year, DatetimeHandler.getToday().month)
    timeRangeSnowflakes = []

    for year, months in yearRange.items():
        for month in range(len(months), 1, -1):
            for day in range(months[month - 1], 1, -1):
                if (DatetimeHandler.getToday().year == year) and (DatetimeHandler.getToday().month == month) and (DatetimeHandler.getToday().day + 1 < day):
                    continue

                dayTimestamp = DatetimeHandler.fromDay(year, month, day)
                daySnowflake = DatetimeHandler.fromTimestamp(dayTimestamp)
                timeRangeSnowflakes.append(daySnowflake)

    timeRangeSnowflakes.append(timeRangeSnowflakes[-1])
    for index in range(len(timeRangeSnowflakes) - 1):
        dayMaxSnowflake = timeRangeSnowflakes[index]
        dayMinSnowflake = timeRangeSnowflakes[index + 1]

        for guildID, guildData in configHandler.configData['guilds'].items():
            for channelID, channelName in guildData['channels'].items():
                relativePath = path.join(getcwd(), 'Scrapes', guildData['name'], channelName)
                if not path.exists(relativePath):
                    makedirs(relativePath)

                networkHeaders.update({'referer': networkHeaders['referer'].format(guildID, channelID)})
                has = '&has=image&has=video&has=embed&has=file&has=link&has=sound'

                networkHeader = NetworkHeader()
                networkHeader.new(networkHeaders)

                networkHandler = NetworkHandler()
                networkHandler.set(url=f'https://discordapp.com/api/v6/guilds/{guildID}/messages/search?channel_id={channelID}{has}&min_id={dayMinSnowflake}&max_id={dayMaxSnowflake}&include_nsfw=true')

                networkData = NetworkHandler.download(networkHandler, networkHeader).json()
                if networkData['total_results'] == 0:
                    continue

                for messages in networkData['messages']:
                    for message in messages:
                        if 'attachments' in message and len(message['attachments']) > 0:
                            for attachment in message['attachments']:
                                url = attachment['proxy_url']
                                downloadFile(url, networkHeader, relativePath, '_'.join(url.split('/')[-2::]).split('?')[0])

                        if 'embeds' in message and len(message['embeds']) > 0:
                            for embed in message['embeds']:
                                if 'image' in embed and len(embed['image']) > 0:
                                    url = embed['image']['proxy_url']
                                    downloadFile(url, networkHeader, relativePath, '_'.join(url.split('/')[-2::]).split('?')[0])


if __name__ == '__main__':

    configHandler = ConfigHandler('discord')
    if not path.isfile(configHandler.filename):
        initialize(configHandler)

    else:
        start(configHandler)
