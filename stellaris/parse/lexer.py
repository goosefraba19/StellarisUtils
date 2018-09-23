import re

class Lexer:
    def __init__(self):
        self._pattern_text = re.compile(r"[a-zA-Z0-9_:.@-]+")
        self._pattern_escaped_text = re.compile(r"\"((\\.|[^\"])*)\"")

    def input(self, data):
        self._index = 0
        self._data = data
        self._length = len(data)

    def token(self):
        while True:

            try:
                c = self._data[self._index]
            except IndexError:
                return ("eof", None)

            # whitespace (skip)
            if c in "\t\n ":
                self._index += 1
                continue

            # literals
            if c in "{}=":
                self._index += 1
                return (c, None)

            # text
            match = self._pattern_text.match(self._data, self._index)
            if match:
                self._index = match.end()
                return ("text", match[0])

            # escaped text
            match = self._pattern_escaped_text.match(self._data, self._index)
            if match:
                self._index = match.end()
                return ("text", match[1])

            raise Exception("could find matching token")
