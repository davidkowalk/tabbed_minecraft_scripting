from interpreter import Token, Lexer, Parser

def test_parser_validity(string):
    lex = Lexer(string)
    parser = Parser(lex)

    try:
        parser.parse()
    except:
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
        result = test_parser_validity(test)
        print("[Test]", test, "->", result)

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

if __name__ == '__main__':
    run_parser_tests()
