from lexer import tokenize, Token
from pprint import pprint

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens # List[Tuple[Token, String]]
        self.__pos = 0

    def current(self):
        return self.tokens[self.__pos]
    
    def next(self):
        self.__pos += 1
        if self.__pos >= len(self.tokens):
            return None
        return self.tokens[self.__pos]

    def expect(self, token):
        token_type, token_value = self.current()
        if token_type != token:
            raise ValueError(f"Expected {token}, got {token_type} at {self.__pos}")
        self.next()
        return token_value

    def parse(self):
        return self.parse_value()

    def parse_value(self):
        token_type = self.current()[0]
        if token_type == Token.LBRACE.value:
            return self.parse_object()
        elif token_type == Token.LBRACKET.value:
            return self.parse_array()
        elif token_type == Token.STRING.value:
            return self.parse_string()
        elif token_type == Token.NUMBER.value:
            return self.parse_number()
        elif token_type == Token.TRUE.value:
            return self.parse_true()
        elif token_type == Token.FALSE.value:
            return self.parse_false()
        elif token_type == Token.NULL.value:
            return self.parse_null()
        
    def parse_object(self):
        obj = {}
        self.expect(Token.LBRACE.value)
        if self.current()[0] == Token.RBRACE.value:
            self.next()
            return obj
        while True:
            key = self.expect(Token.STRING.value)
            self.expect(Token.COLON.value)
            value = self.parse_value()
            obj[key] = value
            if self.current()[0] == Token.RBRACE.value:
                self.next()
                return obj
            self.expect(Token.COMMA.value)

    def parse_array(self):
        self.expect(Token.LBRACKET.value)
        arr = []
        if self.current()[0] == Token.RBRACKET.value:
            self.next()
            return arr
        while True:
            arr.append(self.parse_value())
            if self.current()[0] == Token.RBRACKET.value:
                self.next()
                return arr
            self.expect(Token.COMMA.value)

    def parse_string(self):
        return self.expect(Token.STRING.value)

    def parse_number(self):
        return self.expect(Token.NUMBER.value)

    def parse_true(self):
        self.next()
        return True

    def parse_false(self):
        self.next()
        return False

    def parse_null(self):
        self.next()
        return None

if __name__ == "__main__":
    with open("example.json", "r") as f:
        input_text = f.read()
        tokens = tokenize(input_text=input_text)
        parser = Parser(tokens)
        d = parser.parse()
        pprint(d)



