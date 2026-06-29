import parser

string = "Lorem ipsum %s\. This is a test string. %s"
#string = "This is a normal text. %b[this is a lowercase text swapped]. This is a normal text"
#string = "%b[%i[THIS TEXT WILL BECOME LOWER AND THEN UPPERCASE AGAIN]] %i[THIS IS A LOWERCASE TEXT]"
#string = r"Escape sequences \[\]"
#string = r"\% percetsn"
#string = "Sample text"

lexer = parser.Lexer()
lexer.tokenize(string)

p = parser.Parser()
print(f"Tokens: {lexer.tokens}\nResult: {p.parse(lexer.tokens, ['hello', 'world'])}")