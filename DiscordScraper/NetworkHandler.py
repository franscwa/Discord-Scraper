from .ErrorHandler import CustomError
from inspect import findsource
from sys import stderr
from time import sleep
import requests


class NetworkHeader(object):
    headerData = {}

    def new(self, kwargs=None):
        try:
            if kwargs is None:
                kwargs = {}

            for key, value in kwargs.items():
                self.headerData.update({key: value})

        except ( OSError, TypeError, KeyError, IndexError, ValueError ) as e:
            raise CustomError(e, 'NetworkHandler', findsource(self.new)[1], 'new', [v for k, v in kwargs.items()])

        except CustomError as ce:
            stderr.write(ce.getMessage())


class NetworkHandler(object):
    targetData = {}

    def __init__(self):
        super(NetworkHandler, self).__init__()

    def set(self, **kwargs):
        try:
            for key, value in kwargs.items():
                self.targetData.update({key: value})

        except ( OSError, TypeError, KeyError, IndexError, ValueError ) as e:
            raise CustomError(e, 'NetworkHandler', findsource(self.set)[1], 'set', [v for k, v in kwargs.items()])

        except CustomError as ce:
            stderr.write(ce.getMessage())

    @staticmethod
    def download(networkHandler, networkHeader, stream=False):
        try:
            sleep(0.5)  # For the sake of ratelimiting
            return requests.get(networkHandler.targetData['url'], headers=networkHeader.headerData, stream=stream)

        except ( OSError, TypeError, KeyError, IndexError, ValueError ) as e:
            raise CustomError(e, 'NetworkHandler', findsource(NetworkHandler.download)[1], 'download', [networkHandler, networkHeader, stream])

        except CustomError as ce:
            stderr.write(ce.getMessage())
