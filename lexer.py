import os
from enum import Enum

class Token(Enum):
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COLON = "COLON"
    COMMA = "COMMA"
    STRING = "STRING"
    NUMBER = "NUMBER"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"

def tokenize(*, input_text, filename = "lexer.txt"):
    tokenized_seq = []
    if os.path.exists(filename):
        os.remove(filename)
        print(f"file <{filename}> was erased")
    with open(filename, 'a') as f:
        n = len(input_text)
        it = iter(input_text)
        while True:
            try:
                token = next(it)
                if token == '{':
                    tokenized_seq.append(Token.LBRACE.value)
                    f.write(Token.LBRACE.value + '\n')
                elif token == '}':
                    tokenized_seq.append(Token.RBRACE.value)
                    f.write(Token.RBRACE.value + '\n')
                elif token == '[':
                    tokenized_seq.append(Token.LBRACKET.value)
                    f.write(Token.LBRACKET.value + '\n') 
                elif token == ']':
                    tokenized_seq.append(Token.RBRACKET.value)
                    f.write(Token.RBRACKET.value + '\n')
                elif token == ':':
                    tokenized_seq.append(Token.COLON.value)
                    f.write(Token.COLON.value + '\n')
                elif token == ',':
                    tokenized_seq.append(Token.COMMA.value)
                    f.write(Token.COMMA.value + '\n')
                elif token == '"':
                    string = tokenize_string(it)
                    tokenized_seq.append(string.strip())
                    f.write(string)
                elif token == '-' or token == '.' or token.isdigit():
                    number, buffer = tokenize_number(it, token)
                    tokenized_seq.append(number.strip())
                    f.write(number)
                    if buffer == ':':
                        tokenized_seq.append(Token.COLON.value)
                        f.write(Token.COLON.value + '\n')
                    elif buffer == ',':
                        tokenized_seq.append(Token.COMMA.value)
                        f.write(Token.COMMA.value + '\n')
                elif token == 't':
                    tokenized_seq.append(Token.TRUE.value)
                    f.write(Token.TRUE.value + '\n')
                elif token == 'f':
                    tokenized_seq.append(Token.FALSE.value)
                    f.write(Token.FALSE.value + '\n')
                elif token == 'n':
                    tokenized_seq.append(Token.NULL.value)
                    f.write(Token.NULL.value + '\n')
            except StopIteration:
                print("StopIteration")
                break
    return tokenized_seq

def tokenize_string(it):
    token = ''
    string = ""
    while True:
        try:
            token = next(it)
            if token == '"':
                break
            if token == '\\':
                esc = next(it)
                string += esc
            else:
                string += token
        except StopIteration:
            print("StopIteration")
            break
    return f"{Token.STRING.value}({string})\n"

def tokenize_number(it, prev_token):
    number = prev_token 
    buffer = None
    while True:
        try:
            token = next(it)
            if token.isdigit() or token == '.':
                number += token
            else:
                buffer = token
                break
        except StopIteration:
            print("StopIteration")
            break
    return f"{Token.NUMBER.value}({number})\n", buffer

if __name__ == "__main__":
    input_file = "example_for_lexer.json"
    with open(input_file) as f:
        input_text = f.read()
        tokenized_seq = tokenize(input_text=input_text)
        print(tokenized_seq)
