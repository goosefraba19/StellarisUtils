class Parser:
    def __init__(self, lexer):
        self._lexer = lexer
        self._token = None

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
                    return (key_or_value, self._parse_object())
                else:
                    raise Exception()    
            else:
                return (None, key_or_value)
        elif self._token[0] == "{":
            return (None, self._parse_object())

    def _parse_object(self):
        self._token = self._lexer.token()
        pairs = []
        while self._token[0] != "}":
            pairs.append(self._parse_pair())
        self._token = self._lexer.token()
        return self._convert_pairs(pairs)

    def _convert_pairs(self, pairs):

        if len(pairs) == 0:
            return pairs

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