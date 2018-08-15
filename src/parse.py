import re

class Lexer:
    def __init__(self):
        self._pattern_text = re.compile(r"[a-zA-Z0-9_:.-]+")
        self._pattern_escaped_text = re.compile(r"\"([^\"]*)\"")

    def input(self, data):
        self._index = 0
        self._data = data
        self._length = len(data)

    def token(self):
        while True:

            # eof
            if self._length <= self._index:
                return ("eof", None)

            c = self._data[self._index]

            # whitespace (skip)
            if c in " \t\n":
                self._index += 1
                continue

            # literals
            if c in "{}=":
                self._index += 1
                return (c, None)

            # text
            match = self._pattern_text.match(self._data, self._index)
            if match:
                value = match.group(0)
                self._index += len(value)
                return ("text", value)

            # escaped text
            match = self._pattern_escaped_text.match(self._data, self._index)
            if match:
                self._index += len(match.group(0))
                return ("text", match.group(1))

            raise Exception("could find matching token")

class Parser:
    def __init__(self):
        self._lexer = Lexer()
        self._token = None

    def input(self, data):
        self._lexer.input(data)

    def parse(self):
        self._token = self._lexer.token()

        pairs = []
        while self._token[0] != "eof":
            pairs.append(self._parse_pair())
        return self._convert_pairs(pairs)

    def _parse_pair(self):
        if self._token[0] == "text":
            key_or_value = self._token[1]
            self._token = self._lexer.token()
            if self._token[0] == "=":
                self._token = self._lexer.token()
                if self._token[0] == "text":
                    value = self._token[1]
                    self._token = self._lexer.token()
                    return (key_or_value, value)
                elif self._token[0] == "{":
                    value = self._parse_object()
                    return (key_or_value, value)
                else:
                    raise Exception()    
            else:
                return (None, key_or_value)
        elif self._token[0] == "{":
            value = self._parse_object()
            return (None, value)

    def _parse_object(self):
        self._token = self._lexer.token()
        pairs = []
        while self._token[0] != "}":
            pairs.append(self._parse_pair())
        self._token = self._lexer.token()
        return self._convert_pairs(pairs)

    def _convert_pairs(self, pairs):
        groups = {}
        is_list = True
        for (key, value) in pairs:
            if key not in groups:
                groups[key] = [value]
            else:
                groups[key].append(value)

            if key != None:
                is_list = False

        if is_list:
            return [value for (key,value) in pairs]
        else:
            for key in groups.keys():
                if len(groups[key]) == 1:
                    groups[key] = groups[key][0]
            return groups



