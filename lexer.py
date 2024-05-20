from utils import *

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.length = len(source_code)
        self.last_type = ""
        self.tokens = []
        self.symbol_table = []
        self.position = 0
        self.cursor = ""
        self.advance()

    def advance(self):
        if self.position < self.length:
            self.cursor = self.source_code[self.position]
            self.position += 1
        else:
            self.cursor = None

    def tokenize_identifier_or_keyword(self):
        identifier = ""
        while self.cursor is not None and (self.cursor.isalpha() or self.cursor == "_"):
            identifier += self.cursor
            self.advance()
        token_type = "KEYWORD" if identifier in KEYWORDS else "IDENTIFIER"
        if token_type == "IDENTIFIER":
            self.add_to_symbol_table(identifier)
        else:
            if identifier in TYPES:
                self.last_type = identifier
        return token_type, identifier

    def tokenize_digits(self):
        digits = ""
        while self.cursor is not None and self.cursor.isdigit():
            digits += self.cursor
            self.advance()
        token_type = "DIGITS"
        return token_type, digits
    
    def tokenize_operator(self):
        operator = self.cursor
        self.advance()
        if operator + self.cursor in OPERATORS:
            operator = operator + self.cursor
            self.advance()
        token_type = "OPERATOR"
        return token_type, operator
    
    def add_to_symbol_table(self, identifier):
        if identifier not in self.symbol_table:
            for symbol in self.symbol_table:
                if symbol["name"] == identifier:
                    return
            self.symbol_table.append({
                "name": identifier,
                "type": self.last_type,
                "kind": "variable",
                "scope": "global",
                "addr": 4 * len(self.symbol_table)
            })

    def next_token(self):
        while self.cursor is not None:
            if self.cursor.isspace():
                self.advance()
            elif self.cursor.isalpha() or self.cursor == "_":
                token_type, token = self.tokenize_identifier_or_keyword()
                self.tokens.append((token_type, token))
                return token_type, token
            elif self.cursor.isdigit():
                token_type, token = self.tokenize_digits()
                self.tokens.append((token_type, token))
                return token_type, token
            elif self.cursor in OPERATORS:
                token_type, token = self.tokenize_operator()
                self.tokens.append((token_type, token))
                return token_type, token
            elif self.cursor in DELIMITERS:
                token_type, token = "DELIMITER", self.cursor
                self.tokens.append((token_type, token))
                self.advance()
                return token_type, token
            else:
                token_type, token = "ERROR", self.cursor
                self.tokens.append((token_type, token))
                self.advance()
                return token_type, token
        return None, None