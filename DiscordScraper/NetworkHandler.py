from .ErrorHandler import *
from sys import stderr
from time import sleep
from os import path
import requests

# Set the current filename for quick reference in all raised exceptions.
fileName = path.basename(__file__)


class NetworkHandler(object):

    # Store a blank string for our target URL and a blank dictionary for our request headers.
    targetUrl, headerData = '', {}

    def setHeaders(self, headerData):
        """
        Set our connection headers.

        :param headerData: The request header dictionary
        :return:
        """

        try:

            # Update or change the contents of our request headers.
            self.headerData.update(headerData)

        except Exception as ex:
            message = 'Unable to set our request headers.\n'
            raise RuntimeException('setHeaders', fileName, lineNumber(self.setHeaders), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    def setSearchParams(self, guildId, channelId, snowflakeMin, snowflakeMax, includeNsfw=True, options=None):
        """
        Generate the search URL for gathering the contents of a channel.

        :param guildId: The ID of the guild/server that contains our channel.
        :param channelId: The ID of the channel that contains the data we want.
        :param snowflakeMin: The snowflake of the target day (00:00:00.000 for local timezone)
        :param snowflakeMax: The snowflake of the next day (00:00:00.000 for local timezone)
        :param includeNsfw: A flag that determines whether or not we can access data from channels marked as NSFW.
        :param options: An array that stores the types of data that we are wanting to return from the search query.
        :return:
        """

        try:
            if len(options) == 0:  # If we're faced with an empty array, then it's probably best to null it out.
                options = None

            # Create a URI query value for every single data type that we want to retrieve.
            optionsHave = '&has={}'.format('&has='.join(options)) if options is not None else ''

            # Combine the URI queries for our snowflakes so that we can return search results day-by-day.
            minMaxSnowflakes = f'&min_id={snowflakeMin}&max_id={snowflakeMax}'

            # Combine all of our URI queries together in their proper order based on the order from Discord's search.
            totalUri = f'{optionsHave}{minMaxSnowflakes}&include_nsfw={"true" if includeNsfw else "false"}'

            # Generate the URL path that the script will request JSON data from.
            searchUri = f'/api/v6/guilds/{guildId}/messages/search?channel_id={channelId}{totalUri}'

            # Set our class variable which sets the target URL from where we will grab our JSON data.
            self.targetUrl = f'https://discordapp.com{searchUri}'

        except Exception as ex:
            message = f'Unable to generate a valid search query.\n'
            raise RuntimeException('setSearchParams', fileName, lineNumber(self.setSearchParams), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    def downloadJsonData(self, timeout=0.5):
        """
        Download the JSON data from our Discord search.

        :param timeout: The amount of time in seconds to wait before continuing with the request.
        :return:
        """

        try:

            # Wait for a specific time (in seconds) before carrying out a request to prevent being ratelimited.
            sleep(timeout)

            # Request some JSON data from our search query.
            requestData = requests.get(self.targetUrl, headers=self.headerData, stream=False)

            # Raise a network exception when the status code is 4XX or 5XX.
            if 399 < requestData.status_code:
                raise NetworkException(self.targetUrl, requestData.status_code, requestData.text)

            # Return our gathered JSON data in the form of a dictionary.
            return requestData.json()

        except NetworkException as nex:
            stderr.write(nex.getMessage())

        except Exception as ex:
            message = f'Unable to download JSON data from Discord.\n'
            raise RuntimeException('downloadJsonData', fileName, lineNumber(self.downloadJsonData), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    def downloadBinaryData(self, targetFileUrl, targetFilePath, targetRequestHeaders=None, stream=True):
        """
        Download the binary data from the attachments and embedded contents of our Discord search.

        :param targetFileUrl: The URL that points to the file we're wanting to grab.
        :param targetFilePath: The local folder that will be used to store the file contents.
        :param targetRequestHeaders: The request headers that we will send to non-Discord servers.
        :param stream: A flag that determines whether we will download file in chunks or as a whole.
        :return:
        """

        try:

            # Combine the file name and path.
            targetFileName = path.join(targetFilePath, '_'.join(targetFileUrl.split('/')[-2::]).split('?')[0])

            # Determine if our file exists.
            if path.isfile(targetFileName):
                return None  # Just end the function right here, no need to make another request for data we have.

            # Determine if our request headers are set or not.
            if targetRequestHeaders is None:
                targetRequestHeaders = self.headerData  # Just simply default to the class request headers instead.

            # Request some binary data from our target file URL.
            requestData = requests.get(targetFileUrl, headers=targetRequestHeaders, stream=stream)

            # Raise a network exception when the status code is 4XX or 5XX.
            if 399 < requestData.status_code:
                raise NetworkException(targetFileUrl, requestData.status_code, requestData.reason)

            # Create a new file and write the gathered contents to it.
            with open(targetFileName, 'wb') as fileStream:
                fileStream.write(requestData.raw.read())

        except NetworkException as nex:
            stderr.write(nex.getMessage())

        except Exception as ex:
            message = f'Unable to download binary data from {targetFileUrl}.\n'
            raise RuntimeException('downloadBinaryData', fileName, lineNumber(self.downloadBinaryData), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())
