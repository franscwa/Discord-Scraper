from inspect import findsource

# Retrieve the line number with the correct offset value for our given function.
lineNumber = lambda function: findsource(function)[1] + 1


class CustomException(Exception):
    def __init__(self, etype, message):
        super(CustomException, self).__init__(etype, message)


class NetworkException(CustomException):
    def __init__(self, url, status, message):
        super(NetworkException, self).__init__(NetworkException, message)
        self.message = f'[NETWORK ERROR]: HTTP {status} on {url}\n'

    def getMessage(self):
        return self.message


class RuntimeException(CustomException):
    def __init__(self, function, filename, linenum, message):
        super(RuntimeException, self).__init__(RuntimeException, message)
        self.message = f'[RUNTIME ERROR]: {function} from {filename}:{linenum}\n'

    def getMessage(self):
        return self.message


class InputException(CustomException):
    def __init__(self, function, argument, userinput, message):
        super(InputException, self).__init__(InputException, message)
        self.message = f'[INPUT ERROR]: {userinput} was not expected for {argument} in {function}\n'

    def getMessage(self):
        return self.message
