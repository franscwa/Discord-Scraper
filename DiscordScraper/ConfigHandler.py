from .ErrorHandler import *
from json import loads, dumps
from os import unlink, path
from sys import stderr

# Get the current filename for use in our exceptions.
fileName = path.basename(__file__)


class ConfigHandler(object):

    # Create an empty dictionary to store our configuration data.
    configData = {}

    def __init__(self, filename):
        filename = f'{filename}.json'  # Sanitize our input by appending the filetype of our stored config JSON.
        self.filename = filename

    def new(self, **kwargs):
        """
        Create a new JSON file to store our configuration data.

        :param kwargs: The keyword-based arguments that will be treated as a dictionary.
        :return:
        """

        try:

            # Determine if we already have an existing config JSON file. If so then simply delete it.
            if path.exists(self.filename):
                unlink(self.filename)

            # Iterate through the keys and values of our keyword-based arguments. Add them to our configuration data.
            for key, value in kwargs.items():
                self.configData.update({key: value})

            # Create a new config JSON file and write the contents of our configuration data into it.
            self.write()

        except Exception as ex:
            message = 'Unable to create or delete JSON configuration data.'
            raise RuntimeException('new', fileName, lineNumber(self.new), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    def load(self):
        """
        Load the contents of our JSON file into our configuration data.

        :return:
        """

        try:

            # Read the contents of our configuration JSON file.
            with open(self.filename, 'r', encoding='utf8') as fstream:
                fdata = fstream.read()

            # Determine if our configuration data hasn't been loaded yet.
            if len(self.configData) == 0:  # This prevents our configuration data from being reset at runtime.
                self.configData = loads(fdata)

        except Exception as ex:
            message = 'Unable to load the contents of our JSON configuration data.'
            raise RuntimeException('load', fileName, lineNumber(self.load), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    def set(self, **kwargs):
        """
        Alter our configuration data at runtime.

        :param kwargs: The keyword-based arguments that will be treated as a dictionary.
        :return:
        """

        try:

            # Determine if we have already loaded our configuration data.
            if len(self.configData) == 0:
                raise Exception('No configuration data available for modification.')

            # Skim through the keys and values of our keyword-based arguments.
            for key, value in kwargs.items():

                # Throw an exception is the given key is not a part of our configuration data.
                if key not in self.configData:
                    raise Exception(f'Invalid config key \'{key}\' given.')

                # Otherwise simply modify the existing configuration data with our new value.
                self.configData[key] = value

        except Exception as ex:
            message = 'Unable to modify the contents of our configuration data.'
            raise RuntimeException('set', fileName, lineNumber(self.set), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())

    def write(self):
        """
        Write our configuration data into a JSON file to store.

        :return:
        """

        try:

            # Throw an exception if our configuration data hasn't been loaded yet.
            if len(self.configData) == 0:
                raise Exception('No configuration data available for export.')

            # Create a new file to dump our configuration data JSON into.
            with open(self.filename, 'w', encoding='utf8') as fstream:
                fstream.write(dumps(self.configData))

        except Exception as ex:
            message = 'Unable to create our configuration JSON file.'
            raise RuntimeException('write', fileName, lineNumber(self.write), message) from ex

        except RuntimeException as rex:
            stderr.write(rex.getMessage())
