'''Utilities for handling text formatting.'''

import sys as _sys
import os as _os
from ._text_format import TextFormat


class FormattedText:
    def __init__(self, text: str, *options: bytes):
        self.text = text
        self.options = options

    def get_format(self) -> str:
        result = ''

        for option in self.options:
            if option is not None:
                result += option.decode()

        return result
    
    @staticmethod
    def reset_format() -> str:
        return TextFormat.RESET.decode()

    def __str__(self) -> str:
        if len(self.options) == 0:
            return self.text
        
        result = ''
        result += self.get_format()
        result += self.text
        result += self.reset_format()

        return result
    
    def __repr__(self) -> str:
        return self.__str__()
    

def read_input(*format_options: bytes) -> str:
    '''
    Ask input from a user using specified styling options.

    :param format_options: Text styling options.

    :returns: User input.
    '''

    result = None
    format = FormattedText('', *format_options)

    try:
        print(format.get_format(), file=_sys.stderr, end='')
        result = input()
        print(format.reset_format(), file=_sys.stderr, end='')
    except KeyboardInterrupt as e:
        print(format.reset_format(), file=_sys.stderr, end='')
        raise e

    return result

def clear_line(file=_sys.stdout, flush: bool = False):
    '''
    Clears the current line from any text of formatting.
    Not really suitable for files.

    :param file: Stream to clear.
    :param flush: Whether to flush the stream after printing.
    '''
    
    if file is None:
        return

    try:
        size = _os.get_terminal_size().columns
        print('\r', ' ' * size, '\r',
              sep='', end='', file=file, flush=flush)
    except OSError:
        pass    # Do nothing

    