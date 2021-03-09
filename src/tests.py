from interpreter import Token, Lexer, Parser

def test_parser_validity(string):
    lex = Lexer(string)
    parser = Parser(lex)

    try:
        parser.parse()
    except Exception as e:
        print(f"\033[1;33m{e}\033[0m")
        return False
    else:
        return True

def import_valid_test_strings():
    #import os.path
    import json

    test_strings = dict()

    with open("../docs/raw/test_strings.txt") as f:
        lines = f.read().split("\n")

    for line in lines:
        if len(line) > 0:
            test_strings[line] = True


    return test_strings


def run_parser_tests():
    #test_strings = {
    #    "clear @s[tag=admin, score={CustomName:\"\"}] minecraft:stone 128": True,
    #    "clear @s[]": True,
    #    "clear @s": True,
    #    "clear @s[] minecraft:stone": True,
    #    "clear @s[] minecraft:stone 128": True,
    #    "clear @s 64": False
    #}

    test_strings = import_valid_test_strings()

    successes = 0
    failures = 0

    for test in test_strings:
        print("[Test]", test)
        result = test_parser_validity(test)

        assertion = result == test_strings[test]
        successes += assertion
        failures += not assertion

        if not assertion:
            print(f"\033[1;31m[Warning] Test failed. Expected: {test_strings[test]}\033[0m")

    if failures == 0:
        print("\033[1;32mAll tests ran successfully.\033[0m")

    else:
        rate = round(successes / (successes+failures) * 1000)/10
        print(f"\033[1;33m{rate}% of tests ran successfully\033[0m")

def data_or_storage():

    test_strings = {
        "block 0 0 0": "data_storage",
        "entity @e[type = armor_stand]": "data_storage",
        "storage minecraft:database": "data_storage",
        "storage minecraft:database": "data_storage",
        "xyz": "generic_data",
        "0": "generic_data",
        "15": "generic_data",
        "15.6": "generic_data",
        "true": "generic_data",
        "false": "generic_data",
        "[a, b, c]": "generic_data",
        "{\"text\":\"hello\"}": "generic_data"
    }

    success = 0
    total = len(test_strings)

    for string in test_strings:
        lex = Lexer(string)
        parser = Parser(lex)
        ops = list()

        try:
            dtype = parser.data_or_storage(ops)
            if dtype == test_strings[string]:
                success += 1
                print(f"\033[1;32m[Test Success]:\t{string}\033[0m")
            else:
                print(f"\033[1;33m[Test Failed]\033[0m:\t{string} \033[1;33m(got \"{dtype}\")\033[0m")
        except Exception as e:
            print(f"\033[1;31m[Catastrophic failure]: {string}\n{e}\033[0m")

    rate = round(success / total * 1000)/10
    print(f"\033[1;33m{rate}% of tests ran successfully\033[0m")


def data_storage():
    #TODO Automate checking these
    #from interpreter import Target, Location

    test_strings = [
        "block 0 0 0",
        "entity @s",
        "entity @s[type=horse]",
        "storage minecraft:database"
    ]

    for test_string in test_strings:
        lex = Lexer(test_string)
        parser = Parser(lex)

        ops = list()

        parser.data_storage(ops)

        print(ops)


def test_components():
    pass

if __name__ == '__main__':
    #data_or_storage()
    #data_storage()
    run_parser_tests()

    #print("please uncomment a check in the code")
