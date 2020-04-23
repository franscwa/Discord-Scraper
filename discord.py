from DiscordScraper import NetworkHandler, DatetimeHandler, ConfigHandler, ArgumentHandler
from DiscordScraper.DatetimeHandler import futureCheck
from os import makedirs, getcwd, path

# Set our general network header data.
networkHeaders = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.10 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36' }


def handleNetworkData(configHandler, dayMinSnowflake, dayMaxSnowflake):
    """
    The function that will handle all of the downloading of the JSON and binary data.

    :param configHandler: The configuration handler class object.
    :param dayMinSnowflake: The minimum snowflake value (yesterday's snowflake).
    :param dayMaxSnowflake: The maximum snowflake value (today's snowflake).
    :return:
    """

    # Iterate through our guilds for our guild IDs, names, and channels.
    for guildId, guildData in configHandler.configData['guilds'].items():

        # Iterate through our guild channels for our channel IDs and names.
        for channelId, channelName in guildData['channels'].items():

            # Create a relative file path based on the current directory.
            relativePath = path.join(getcwd(), 'Scrapes', guildData['name'], channelName)

            # If the relative filepath doesn't exist, then simply create it alongside the subfolders.
            if not path.exists(relativePath):
                makedirs(relativePath)

            # Update our general network header data to include our referer and authorization token.
            networkHeaders.update({'referer': f'https://discordapp.com/channels/{guildId}/{channelId}', 'authorization': configHandler.configData['token']})

            # Create our NetworkHandler class object.
            networkHandler = NetworkHandler()

            # Set our network headers.
            networkHandler.setHeaders(networkHeaders)

            # Set our target URL.
            networkHandler.setSearchParams(guildId, channelId, dayMinSnowflake, dayMaxSnowflake, options=configHandler.configData['options'])

            # Download our JSON data.
            jsonData = networkHandler.downloadJsonData()

            # Determine if we have any results, if not then we just skip the channel for the day.
            if jsonData['total_results'] == 0:
                continue

            # Otherwise iterate through all of the messages in the JSON data.
            for messages in jsonData['messages']:

                # Gather each individual message.
                for message in messages:

                    # Determine if we have any attachments to grab.
                    if 'attachments' in message and len(message['attachments']) > 0:

                        # Gather each individual attachment.
                        for attachment in message['attachments']:

                            # Set the file URL.
                            fileUrl = attachment['proxy_url']

                            # Download the file.
                            networkHandler.downloadBinaryData(fileUrl, relativePath)

                    # Determine if we have any embedded messages to grab.
                    if 'embeds' in message and len(message['embeds']) > 0:

                        # Set a custom user agent string.
                        fileHeader = { 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}

                        # Gather each individual embedded message.
                        for embed in message['embeds']:

                            # Determine if there's any images in our embedded message.
                            if 'image' in embed and len(embed['image']) > 0:

                                # Set the file URL.
                                fileUrl = embed['image']['proxy_url']

                                # Download the file.
                                networkHandler.downloadBinaryData(fileUrl, relativePath, fileHeader)

                            # Determine if there's any videos in our embedded message.
                            if 'video' in embed and len(embed['video']) > 0:

                                # Determine if there's a proxy_url option in the embed video.
                                if 'proxy_url' in embed['video']:

                                    # Set the file URL.
                                    fileUrl = embed['video']['proxy_url']

                                    # Download the file.
                                    networkHandler.downloadBinaryData(fileUrl, relativePath, fileHeader)


def start(configHandler):
    """
    Boot our scraper script and let it start scraping data.

    :param configHandler: The configuration handler class object.
    :return:
    """

    # Create a blank array to store our snowflake ranges.
    timeRangeSnowflakes = []

    # Load our configuration from our configuration JSON file.
    configHandler.load()

    # Get the entire calendar range for Discord's existence.
    yearRange = DatetimeHandler.getRange(2015, DatetimeHandler.getToday().year, DatetimeHandler.getToday().month)

    # Iterate through the years and the calendar dates in our year range.
    for year, dates in yearRange.items():

        # Iterate through the months in our calendar dates.
        for month in range(len(dates), 1, -1):

            # Iterate through the days in our months.
            for day in range(dates[month - 1], 1, -1):

                # Determine if the current date is in the future. Skip it altogether if it is.
                if futureCheck(year, month, day):
                    continue

                # Get the current date timestamp.
                dayTimestamp = DatetimeHandler.fromDay(year, month, day)

                # Convert the timestamp over to a snowflake.
                daySnowflake = DatetimeHandler.fromTimestamp(dayTimestamp)

                # Append the snowflake to our snowflake ranges.
                timeRangeSnowflakes.append(daySnowflake)

    # Cap off the end of our snowflake ranges with the last snowflake in the range.
    timeRangeSnowflakes.append(timeRangeSnowflakes[-1])

    # Iterate through our snowflake range values.
    for index in range(len(timeRangeSnowflakes) - 1):

        # Set the current snowflake value as the maximum.
        dayMaxSnowflake = timeRangeSnowflakes[index]

        # Set yesterday's snowflake value as the minimum.
        dayMinSnowflake = timeRangeSnowflakes[index + 1]

        # Pass our snowflake ranges to our network handler function.
        handleNetworkData(configHandler, dayMinSnowflake, dayMaxSnowflake)


if __name__ == '__main__':

    # Load a file named discord.json which will store our configuration data.
    configHandler = ConfigHandler('discord')

    # Determine if our configuration data file exists.
    if not path.isfile(configHandler.filename):  # Create a new one if one doesn't already exist.
        ArgumentHandler(configHandler).initialize()

    # Start the scraping process otherwise.
    start(configHandler)
