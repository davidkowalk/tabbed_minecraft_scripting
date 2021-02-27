INTEGER, ID, COMMAND, TARGET, ATTR_BEGIN, ATTR_END, ASSIGN, COMMA, NBT, NEWLINE, EOF = 'INTEGER', 'ID', 'COMMAND', 'TARGET', 'ATTRIBUTE_START', 'ATTRIBUTE_END', 'ASSIGN', ',', 'NBT', 'NEWLINE', 'EOF'

# This interpreter takes compiled files and executes the function provided by the user.

###############################################################################
#                                                                             #
#  LEXICAL ANALYZER                                                           #
#                                                                             #
###############################################################################

# Converts String to Token Stream

class Token(object):
    """
    Holds type and value of a Token.

    A Token is to a command what a word is to a sentence.
    """

    def __init__(self, type, value):

        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(
            type = repr(self.type),
            value = self.value
        )

    def __repr__(self):
        return self.__str__()

# list reserved keywords (command keys)
KEYWORDS = {
    "attribute": Token(COMMAND, "attribute"),
    "bossbar": Token(COMMAND, "bossbar"),
    "clear": Token(COMMAND, "clear"),
    "data": Token(COMMAND, "data"),
    "effect": Token(COMMAND, "effect"),
    "enchant": Token(COMMAND, "enchant"),
    "execute": Token(COMMAND, "execute"),
    "function": Token(COMMAND, "function"),
    "gamemode": Token(COMMAND, "gamemode"),
    "give": Token(COMMAND, "give"),
    "kill": Token(COMMAND, "kill"),
    "list": Token(COMMAND, "list"),
    "say": Token(COMMAND, "say"),
    "scoreboard": Token(COMMAND, "scoreboard"),
    "stop": Token(COMMAND, "stop"),
    "summon": Token(COMMAND, "summon"),
    "tag": Token(COMMAND, "tag"),
    "team": Token(COMMAND, "team"),
    "teleport": Token(COMMAND, "teleport"),
    "tellraw": Token(COMMAND, "tellraw"),
    "title": Token(COMMAND, "title"),
    "?": Token(COMMAND, "?"),
    "advancement": Token(COMMAND, "advancement"),
    "ban": Token(COMMAND, "ban"),
    "ban-ip": Token(COMMAND, "ban-ip"),
    "defaultgamemode": Token(COMMAND, "defaultgamemode"),
    "deop": Token(COMMAND, "deop"),
    "help": Token(COMMAND, "help"),
    "kick": Token(COMMAND, "kick"),
    "locate": Token(COMMAND, "locate"),
    "locatebiome": Token(COMMAND, "locatebiome"),
    "loot": Token(COMMAND, "loot"),
    "me": Token(COMMAND, "me"),
    "msg": Token(COMMAND, "msg"),
    "op": Token(COMMAND, "op"),
    "pardon": Token(COMMAND, "pardon"),
    "pardon-ip": Token(COMMAND, "pardon-ip"),
    "publish": Token(COMMAND, "publish"),
    "save-all": Token(COMMAND, "save-all"),
    "save-off": Token(COMMAND, "save-off"),
    "save-on": Token(COMMAND, "save-on"),
    "setidletimeout": Token(COMMAND, "setidletimeout"),
    "setworldspawn": Token(COMMAND, "setworldspawn"),
    "spectate": Token(COMMAND, "spectate"),
    "spreadplayers": Token(COMMAND, "spreadplayers"),
    "whitelist": Token(COMMAND, "whitelist")
}

class Lexer(object):

    """
    The Lexical Analyzer turns a stream of Characters into a stream of Tokens by looking at the string and fitting it into a grammar
    """

    def __init__(self, text, line = 1):
        self.text = text
        self.pos = 0
        self.line_pos = 0
        self.line = line
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception(f"Invalid Character: {self.current_char} at {self.line_pos} in line {self.line}")


    def get_next_token(self):

        """
        Generates a stream of Tokens from a String
        """

        while self.current_char is not None:

            # Detect end of line
            if self.current_char == "\n":
                self.line += 1
                self.line_pos = 0
                self.advance()
                return Token(NEWLINE, "NEWLINE")

            # Skip Whitespace
            if self.current_char.isspace():
                # print("[Warning] Skipping whitespace in line {line}".format(line=self.line))
                self.skip_whitespace()
                continue

            # Collects integers
            if self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())

            # Collect ids and keywords
            if self.current_char.isalpha():
                return self.get_id()

            if self.current_char == "@":
                return self.get_target()

            if self.current_char == "[":
                self.advance()
                return Token(ATTR_BEGIN, "[")

            if self.current_char == "]":
                self.advance()
                return Token(ATTR_END, "]")

            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, "=")

            if self.current_char == "{":
                return self.get_nbt()

            self.error()


        return Token(EOF, None)


    # Utility Functions

    def out_of_bounds(self):
        return self.pos >= len(self.text)

    def advance(self):
        self.pos += 1
        self.line_pos += 1

        if self.out_of_bounds():
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):

        while self.current_char is not None and self.current_char.isspace() and self.current_char != "\n":
            self.advance()

    def get_integer(self):

        int_str = ""

        while self.current_char is not None and self.current_char.isdigit():
            int_str += self.current_char
            self.advance()

        return int(int_str)

    def get_id(self):
        result = ""

        # Collect all characters
        #while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ["?", "-", "_", "."]):
        while self.current_char is not None and not self.current_char.isspace():
            result += self.current_char
            self.advance()

        # If result is in known keywords, return Token of that, otherwise generate and return token of id
        return KEYWORDS.get(result, Token(ID, result))

    def get_target(self):
        target = ""
        in_bracket = 0

        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == "@"):

            target += self.current_char
            self.advance()

        return Token(TARGET, target)

#    def get_attr(self):
#
#        attr_str = "["
#        in_bracket = 0
#
#        self.advance()
#
#        while (self.current_char is not None and self.current_char != "\n") and (self.current_char != "]" or in_bracket > 0):
#
#            if self.current_char == "[":
#                in_bracket += 1
#
#            if self.current_char == "]":
#                in_bracket -= 1
#
#            attr_str += self.current_char
#            self.advance()
#
#        if self.current_char == "]":
#            attr_str += self.current_char
#            self.advance()
#
#        return Token(ATTR, attr_str)

    def get_nbt(self):

        snbt = ""
        instring = False
        last_char = ""

        while self.current_char is not None and (self.current_char != "}" or instring):
            snbt += self.current_char

            if self.current_char == "\"" and last_char != "\\":
                instring = not instring

            last_char = self.current_char
            self.advance()

        snbt += self.current_char
        self.advance()

        return Token(NBT, snbt)




#from interpreter import print_stream
#
#func = """data modify entity @s name.text set value {"message": "{\"text\": \"hello\"}"}
#say test
#scoreboard players set @a[score = {}] obj 15
#"""
#
#print_stream(func)


def print_stream(string):

    lex = Lexer(string)

    token = Token("EMPTY", "EMPTY")

    while token.value is not None:
        token = lex.get_next_token()
        print(token)


###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

# Turns Token Stream into Tree Structure (Abstract Syntax Tree / AST)

class AST(object):
    pass

class CommandList(AST):
    """
    Holds list of Commands in function
    """
    def __init__(self):
        self.children = list()

class Command(AST):
    """
    Holds Command with head (like "say") and operands (like "<message>")
    """

    def __init__(self, token, operands):
        self.command_token = token
        self.operands = operands # List of operands. May hold another command

class Target(AST):
    """
    Holds target with identifier and attributes.
    """

    def __init__(self, token, attributes):
        self.token = token
        self.id = token.value
        self.attr = attributes

class Attribute(AST):

    def __init__(self, token, attr):
        self.token = token
        self.attr = attr


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
