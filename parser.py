class TokenType:
    TEXT = 0
    COMMAND = 1
    LEFT_SQBRACKET = 2
    RIGHT_SQBRACKET = 3

    # LEFT_RNBRACKET = 5
    # RIGHT_RNBRACKET = 6

ESCAPE_SEQUENCE = '\\'

class Lexer:
    def __init__(self):
        self.pos: int = 0
        self.tokens: list[tuple[TokenType, str]] = []

        self.buffer: str = ""

    def tokenize(self, string: str) -> list:
        self.pos = 0
        self.string = string
        self.length = len(string)
        self.buffer = ""
        return self._tokenize()

    def _tokenize(self) -> None:
        prev_char = ""
        while self.pos < self.length:
            char = self.string[self.pos]
            if char == "%" and prev_char != ESCAPE_SEQUENCE:
                self._flush_buffer()
                self._process_command()
                continue
            elif char == '[' and prev_char != ESCAPE_SEQUENCE:
                self.tokens.append((TokenType.LEFT_SQBRACKET, '['))
            elif char == ']' and prev_char != ESCAPE_SEQUENCE:
                self._flush_buffer()
                self.tokens.append((TokenType.RIGHT_SQBRACKET, ']'))
            elif char == ESCAPE_SEQUENCE:
                pass
            else:
                self.buffer += char

            self.pos += 1
            prev_char = char
        self._flush_buffer()

    def _flush_buffer(self):
        if not self.buffer:
            return
        self.tokens.append((TokenType.TEXT, self.buffer))
        self.buffer = ""

    def _process_command(self):
        self.pos += 1

        command = ""
        while self.pos < self.length:
            char = self.string[self.pos]
            if char == '[' or char == ' ' or char == ']' or char == ESCAPE_SEQUENCE:
                break

            command += char
            self.pos += 1
    
        self.tokens.append((TokenType.COMMAND, command))


class Parser:
    def __init__(self):
        self.pos = 0
        self.strings = []

    def parse(self, tokens: list, rstrings: list[str]):
        self.strings = rstrings
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)
        return self._parse_until_rbracket()

    def peek(self):
        if self.pos < self.length:
            return self.tokens[self.pos]
        return None
    
    def consume(self):
        token = self.peek()
        self.pos += 1
        return token

    def _parse_until_rbracket(self) -> str:
        output = []
        while self.pos < self.length:
            tt, tv = self.peek()
            if tt == TokenType.RIGHT_SQBRACKET:
                self.consume()
                break
            elif tt == TokenType.TEXT:
                output.append(tv)
                self.consume()
            elif tt == TokenType.LEFT_SQBRACKET:
                self.consume()
                raise SyntaxError(f"Expected symbol: {tv} at Tpos {self.pos}")
            elif tt == TokenType.COMMAND:
                self.consume()

                if self.peek() is None or self.peek()[0] != TokenType.LEFT_SQBRACKET:
                    match tv:
                        case "s": output.append(self.strings.pop(0))
                        case _: raise SyntaxError(f"Unknown command \"{tv}\" [supposed to be no arguments]")
                    
                    continue
            
                self.consume()
                inner: str = self._parse_until_rbracket()

                match tv:
                    case "b": output.append(inner.upper())
                    case "i": output.append(inner.lower())
                    case _: raise SyntaxError(f"Unknown command \"{tv}\" [supposed to have arguments]")

            else:
                self.consume()

        return ''.join(output)
    
