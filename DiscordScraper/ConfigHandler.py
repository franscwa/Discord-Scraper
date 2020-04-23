from .ErrorHandler import CustomError
from inspect import findsource
from json import loads, dumps
from os import unlink, path
from sys import stderr


class ConfigHandler(object):
    configData = {}

    def __init__(self, filename):
        filename = f'{filename}.json'
        self.filename = filename

    def new(self, **kwargs):
        try:
            if path.exists(self.filename):
                unlink(self.filename)

            for key, value in kwargs.items():
                self.configData.update({key: value})

            with open(self.filename, 'w', encoding='utf8') as fstream:
                fstream.write(dumps(self.configData))

        except ( OSError, TypeError, KeyError, IndexError, ValueError ) as e:
            raise CustomError(e, 'ConfigHandler', findsource(self.new)[1], 'new', [v for k, v in kwargs.items()])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf8') as fstream:
                fdata = fstream.read()

            if len(self.configData) == 0:
                self.configData = loads(fdata)

        except (OSError, TypeError, KeyError, IndexError, ValueError) as e:
            raise CustomError(e, 'ConfigHandler', findsource(self.load)[1], 'load', [])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    def set(self, **kwargs):
        try:
            if len(self.configData) == 0:
                raise IndexError('No configuration data available for modification.')

            for key, value in kwargs.items():
                if key not in self.configData:
                    raise KeyError(f'Invalid config key {key} given.')

                self.configData[key] = value

        except (OSError, TypeError, KeyError, IndexError, ValueError) as e:
            raise CustomError(e, 'ConfigHandler', findsource(self.set)[1], 'set', [v for k, v in kwargs.items()])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    def write(self):
        try:
            if len(self.configData) == 0:
                raise IndexError('No configuration data available for export.')

            with open(self.filename, 'w', encoding='utf8') as fstream:
                fstream.write(dumps(self.configData))

        except (OSError, TypeError, KeyError, IndexError, ValueError) as e:
            raise CustomError(e, 'ConfigHandler', findsource(self.write)[1], 'write', [])

        except CustomError as ce:
            stderr.write(ce.getMessage())
