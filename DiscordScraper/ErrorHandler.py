class CustomError(Exception):
    def __init__(self, errortype, filename, linenum, function, arguments):
        super(CustomError, self).__init__(errortype)
        self.message = f'{filename}:{linenum + 1} -> {function}({",".join([str(a) for a in arguments])})'

    def getMessage(self):
        return f'{self.message}: {self}\n'
