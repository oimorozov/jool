#!/usr/bin/env python3
import sys
from lexer import tokenize

SUBCOMMANDS = {
    "find": "find",
    "remove": "remove"
    #TBD: more commands 
}

def lev(s1 ,s2):
    n1 = len(s1)
    n2 = len(s2)
    if n1 == 0:
        return n2
    if n2 == 0:
        return n1
    if s1[0] == s2[0]:
        return lev(s1[1:], s2[1:])
    return 1 + min(lev(s1[1:], s2), lev(s1, s2[1:]), lev(s1[1:], s2[1:]))

def find_most_similar_subcommand(subcommand):
    accuracy = []
    for subcmd in SUBCOMMANDS.values():
        accuracy.append((subcmd, (lev(subcmd, subcommand))))
    accuracy.sort(key=lambda x: x[1])
    return accuracy[0][0]

def cmd_usage(program, subcommand = None):
    if subcommand == None:
        print(f"""Usage:
    {program} [SUBCOMMAND] <query> <file.json>
    SUBCOMMANDS:
        find    <query> <file.json>
        remove  <query> <file.json>
    """
        )
    else:
        subcommand = find_most_similar_subcommand(subcommand)
        if subcommand == "find":
            print(f"""Usage:
    {program} {subcommand} <query> <file.json>
        find key in json and print key-value pair
    """
        )
        elif subcommand == "remove":
            print(f"""Usage:
    {program} {subcommand} <query> <file.json>
        remove key-value pair in json
    """
        )
        
if __name__ == "__main__":
    n = len(sys.argv)
    if n == 1:
        program = sys.argv
        cmd_usage(*program)
        sys.exit(1)
    elif n == 2:
        program, subcommand = sys.argv
        cmd_usage(program, subcommand)
        sys.exit(1)
    elif n == 3:
        program, *args = sys.argv
        subcommand, *args = args
        cmd_usage(program, subcommand)
        sys.exit(1)
    elif n == 4:
        program, *args = sys.argv
        subcommand, *args = args
        word, *args = args
        file, *args = args
        with open(file, "r+") as f:
            input_text = f.read()
            tokenized_seq = tokenize(input_text=input_text)
            if subcommand == SUBCOMMANDS["find"]:
                print("Find Command")
            elif subcommand == SUBCOMMANDS["remove"]:
                print("Remove Command")
            else:
                cmd_usage(program, subcommand)
    else:
        print("Too many arguments were provided, expected 3")
        program, *args = sys.argv
        cmd_usage(program)
        sys.exit(1)

    sys.exit(0)
