from lexer import tokenize
from parser import Parser


# fix with ai :(
def format_json(data):
    def format_value(value, tabs):
        indent = '\t' * tabs

        if isinstance(value, dict):
            print('{')
            items = list(value.items())
            for i, (k, v) in enumerate(items):
                print(indent + f'"{k}": ', end='')
                format_value(v, tabs + 1)
                if i < len(items) - 1:
                    print(',')
                else:
                    print()
            print('\t' * (tabs - 1) + '}', end='')

        elif isinstance(value, list):
            print('[')
            for i, item in enumerate(value):
                print(indent, end='')
                format_value(item, tabs + 1)
                if i < len(value) - 1:
                    print(',')
                else:
                    print()
            print('\t' * (tabs - 1) + ']', end='')

        elif value is True:
            print('true', end='')
        elif value is False:
            print('false', end='')
        elif value is None:
            print('null', end='')
        elif isinstance(value, (int, float)):
            print(value, end='')
        else:
            print(f'"{value}"', end='')

    format_value(data, 1)
    print()
 
if __name__ == "__main__":
    d = {
        "string": "hello, world!",
        "object": {
            "array": [1, 2, 3, 4, 5, "string"],
            "another_object": {
                "True": True
            }
        },
        "number": 123.456,
        "object_array": [
            {
                "phone_number": 89001229303,
                "name": "Gustavo"
            },
            {
                "phone_number": 12345678902,
                "name": "Max"
            }
        ]
    }
    with open("example.json", "r") as f:
        input_text = f.read()
        tokens = tokenize(input_text=input_text)
        parser = Parser(tokens)
        d = parser.parse()
        format_json(d)

