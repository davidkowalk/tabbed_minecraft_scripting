STRING, COMMAND, TARGET, NBT, NEWLINE, EOF = 'STRING', 'COMMAND', 'TARGET', 'NBT', 'NEWLINE', 'EOF'
ATTR_BEGIN, ATTR_END, ASSIGN, COMMA, OPERATION, NOT = 'ATTRIBUTE_START', 'ATTRIBUTE_END', 'ASSIGN', ',', 'OPERATION', 'NOT'
INTEGER, FLOAT, RANGE, BOOLEAN = 'INTEGER', 'FLOAT', 'RANGE', 'BOOL'


number_types = (INTEGER, FLOAT)
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
            type=self.type,
            value=self.value
        )

    def __repr__(self):
        return self.__str__()


# list reserved keywords (command keys)
KEYWORDS = {
    "true": Token(BOOLEAN, "true"),
    "false": Token(BOOLEAN, "false"),

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

    def __init__(self, text, line=1):
        self.text = text
        self.pos = 0
        self.line_pos = 0
        self.line = line
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception(
            f"Invalid Character: {self.current_char} at {self.line_pos} in line {self.line}")

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
                return self.get_num()

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

            if self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")

            if self.current_char == "=":
                self.advance()

                if self.current_char == "=":
                    self.advance()
                    return Token(OPERATION, "==")
                else:
                    return Token(ASSIGN, "=")

            if self.current_char == "{":
                return self.get_nbt()

            if self.current_char in ("<", ">", "-", "+"):
                return self.get_operation()

            if self.current_char == "!":
                self.advance()
                return Token(NOT, "!")

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

    def peek(self):

        if self.pos+1 >= len(self.text):
            return None
        else:
            return self.text[self.pos+1]

    def skip_whitespace(self):

        while self.current_char is not None and self.current_char.isspace() and self.current_char != "\n":
            self.advance()

    def get_num(self):

        num_str = ""
        dots = 0

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == "."):

            if self.current_char == ".":
                dots += 1

            num_str += self.current_char
            self.advance()

        if dots == 0:
            return Token(INTEGER, int(num_str))
        elif dots == 1:
            return Token(FLOAT, float(num_str))
        elif dots == 2:
            return Token(RANGE, num_str)

    def get_id(self):
        result = ""

        # Collect all characters
        # while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ["?", "-", "_", "."]):
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in ("-", "_", ":", ".")):
            result += self.current_char
            self.advance()

        # If result is in known keywords, return Token of that, otherwise generate and return token of id
        return KEYWORDS.get(result, Token(STRING, result))

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

    def get_operation(self):

        op = ""
        allowed = ("<", ">", "=")

        if self.current_char in allowed:
            op += self.current_char

        next_char = self.peek()

        if next_char in allowed:
            op += next_char
            self.advance()

        self.advance()

        return Token(OPERATION, op)


#from interpreter import print_stream
#
# func = """data modify entity @s name.text set value {"message": "{\"text\": \"hello\"}"}
# say test
# scoreboard players set @a[score = {}] obj 15
# scoreboard players operation @s obj >= @p obj
# """
#
# print_stream(func)


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

    def __init__(self, children=list()):
        self.children = children


class Command(AST):
    """
    Holds Command with head (like "say") and operands (like "<message>")
    """

    def __init__(self, token, operands):
        self.command_token = token
        self.operands = operands  # List of operands. May hold another command

    def __str__(self):

        operand_value_list = ""
        for operand in self.operands:
            operand_value_list += str(operand)+", "

        return f"Command({self.command_token.value}, {operand_value_list[:-2]})"

    def __repr__(self):
        return self.__str__()


class Target(AST):
    """
    Holds target with identifier and attributes.
    """

    def __init__(self, token: Token, attributes: list=None):
        self.token = token
        self.id = token.value
        self.attr = attributes

    def __str__(self):

        attr_str = ""

        if self.attr is None:
            return f"Target({self.id})"

        for attr in self.attr:
            attr_str += str(attr)

        return f"Target({self.id}[{attr_str}])"


class Attribute(AST):

    def __init__(self, key, attr):
        self.key = key
        self.attr = attr

    def __str__(self):
        return f"Attribute({self.key.value}={self.attr.value})"

    def __repr_(self):
        return self.__str__()

class Location(AST):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.raw = (x.value, y.value, z.value)

class Rotation(AST):

    def __init__(self, r, w):
        self.r = r
        self.w = w


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, expected):
        raise Exception(f"Parser Failure: Invalid Syntax.\nExpected token type {expected} but got {self.current_token.type} on token {self.current_token.value}")

    def generic_command_exception(self):
        raise Exception(
            f"PARSER FAILURE!\nThe parser encountered an unknown function: {self.current_token.value}\nPlease file a bug report at https://github.com/davidkowalk/tabbed_minecraft_scripting/issues")

    def eat(self, *token_type):
        """
        Checks if current token fits expected syntax (ie. token type) and advances to the next token.
        """
        if self.current_token.type in token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type)

    def read_op(self, list, type):
        list.append(self.current_token)
        self.eat(type)

    def read_op_optional(self, list, type):

        if self.current_token.type == type:
            list.append(self.current_token)
            self.current_token = self.lexer.get_next_token()
            return True

        return False

    # command wrappers

    def function(self):
        node = self.command_list()
        return node

    def command_list(self):
        """
        Returns a list of all commands
        """
        results = [self.command()]

        while self.current_token.type != EOF:
            self.eat(NEWLINE)
            results.append(self.command())

        return results

    def command(self):

        if self.current_token.type == COMMAND:
            method_name = "mc_command_"+self.current_token.value
            mc_method = getattr(self, method_name,
                               self.generic_command_exception)

            head = self.head()
            ops = list()

            return mc_method(head, ops)
        else:
            return self.empty()

    # command elemennts

    def target(self):

        token = self.current_token

        self.eat(TARGET, STRING)

        if not self.current_token.type == ATTR_BEGIN:
            return Target(token)

        self.eat(ATTR_BEGIN)
        attributes = self.attribute_list()
        self.eat(ATTR_END)

        return Target(token, attributes)


    def attribute_list(self):

        if self.current_token.type == ATTR_END:
            return list()

        attr_list = [self.attribute()]

        if self.current_token.type == COMMA:
            self.eat(COMMA)
            # This is recoursive. Could Probably be solved with a while loop but I'm lazy
            attr_list += self.attribute_list()

        return attr_list


    def attribute(self):

        key_token = self.current_token

        if self.current_token.value == "tag": #Tag is parsed as command. This is pretty hacky. Don't do this
            self.current_token.type = STRING

        self.eat(STRING)
        self.eat(ASSIGN)

        value_token = self.current_token
        self.eat(STRING, NBT)

        return Attribute(key_token, value_token)


    def list(self):
        self.eat(ATTR_BEGIN)
        gen_list = [generic_data()]

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            gen_list.append(generic_data())

        self.eat(ATTR_END)

        return gen_list


    def location(self):
        """
        Colects 3 numbers and puts them into Location element
        """
        x = number()
        y = number()
        z = number()

        return Location(x, y, z)


    def rotation(self):
        """
        Collects 2 numbers and returns rotation element
        """

        r = number()
        w = number()

        return Rotation(r, w)


    def data_storage(self):
        pass


    def generic_data(self):
        """
        Returns any STRING, number, Boolean, list or NBT
        """

        if self.current_token.type in (STRING, INTEGER, FLOAT, BOOLEAN, NBT):
            data = self.current_token
            self.eat(INTEGER, FLOAT, BOOLEAN, NBT)
            return data

        if self.current_token.type == ATTR_BEGIN:
            return self.list()

        self.error(STRING, INTEGER, FLOAT, BOOLEAN, NBT, "LIST")


    def data_source(self):

        src = self.current_token
        self.eat(STRING)

        storage = data_storage()

        self.eat(STRING)

    def number(self):
        """
        Collects any Integers or Floats and returns Token
        """

        num = self.current_token

        self.eat(INTEGER, FLOAT)

        return num

    def head(self):
        token = self.current_token
        self.eat(COMMAND)
        return token


    def empty(self):
        return NoOp()


    def no_operands_command(self):
        node = Command(self.current_token, None)
        self.eat(COMMAND)
        return node

    def single_operands_command(self, op_type):
        head = self.head()
        ops = (self.current_token)
        self.eat(op_type)

        return Command(head, op_type)

    # execute being overloaded

    def execute_command(self):
        pass


    # commands

    def mc_command_attribute(self, head, ops):
        head = self.head()
        operands = [self.target()]

        #operands.append(self.current_token)
        #self.eat(STRING)

        self.read_op(operands, STRING)

        if self.current_token.type == STRING:
            self.read_op(operands, STRING)

            if self.current_token.type == STRING:
                self.read_op(operands, STRING)

                if self.current_token.type == STRING:
                    self.read_op(operands, STRING)
                    operands.append(self.number())
                    self.read_op(operands, STRING)

                elif self.current_token.type in number_types:
                    operands.append(self.number())


            elif self.current_token.type in number_types:
                operands.append(self.number())


        elif self.current_token.type in number_types:
            operands.append(self.number())

        return Command(head, operands)




    def mc_command_bossbar(self, head, ops):
        head = self.head()

        operands = [self.current_token]
        self.eat(STRING)

        self.read_op(operands, STRING)
        self.read_op(operands, STRING)

        if self.current_token.type == STRING:
            self.read_op(operands, STRING)

            if self.current_token.type in (STRING, BOOLEAN):
                operands.append(self.current_token)
                self.eat(STRING, BOOLEAN)
            elif self.current_token.type in number_types:
                operands.append(self.number())

        return Command(head, operands)


    def mc_command_clear(self, head, ops):

        ops.append(self.target())

        if self.current_token.type == STRING:
            ops.append(self.current_token)
            self.eat(STRING)

            if self.current_token.type == INTEGER:
                ops.append(self.current_token)
                self.eat(INTEGER)

        return Command(head, ops)


    def mc_command_data(self, head, ops):
        self.read_op(ops, STRING)
        operands.append(self.data_storage())

        if self.read_op_optional(ops, STRING):

            if self.read_op_optional(ops, STRING):

                if self.current_token.type == INTEGER:
                    operands.append(self.number())

                elif False: #data source or data storage
                    pass
                else:
                    self.error((INTEGER, FLOAT, STRING))

            elif self.current_token.type in number_types:
                ops.append(self.number())

        elif self.current_token.type == NBT:
            ops.append(self.current_token)
            self.eat(NBT)
        else:
            self.error((STRING, NBT))


    def mc_command_effect(self, head, ops):

        self.read_op(ops, STRING)

        ops.append(self.target())

        if self.read_op_optional(ops, STRING):

            if self.current_token.type in number_types:
                ops.append(self.number())
                self.read_op(ops, INTEGER)
                self.read_op_optional(ops, BOOLEAN)

        return Command(head, ops)


    def mc_command_enchant(self, head, ops):

        ops.append(target())
        self.read_op(ops, STRING)
        self.read_op_optional(ops, INTEGER)

        return Command(head, ops)


    def mc_command_execute(self, head, ops):
        pass


    def mc_command_function(self, head, ops):

        return self.single_operands_command(STRING)


    def mc_command_gamemode(self, head, ops):

        self.read_op(ops, STRING)
        ops.append(self.target())

        return Command(head, ops)


    def mc_command_give(self, head, ops):

        ops.append(self.target())
        self.read_op(STRING)
        self.read_op_optional(INTEGER)

        return Command(head, ops)


    def mc_command_kill(self, head, ops):

        self.read_op(ops, STRING)

        return Command(head, ops)


    def mc_command_list(self, head, ops):
        return no_operands_command()


    def mc_command_say(self, head, ops):

        while self.current_token.type in (STRING, INTEGER, FLOAT, BOOLEAN, TARGET):

            self.read_op_optional(ops, STRING)
            self.read_op_optional(ops, INTEGER)
            self.read_op_optional(ops, FLOAT)
            self.read_op_optional(ops, BOOLEAN)
            self.read_op_optional(ops, NBT)

            if self.current_token.type == TARGET:
                ops.append(target())


    def mc_command_scoreboard(self, head, ops):
        pass


    def mc_command_stop(self, head, ops):
        return no_operands_command()


    def mc_command_summon(self, head, ops):

        self.read_op(ops, STRING)
        ops.append(self.location())
        self.read_op_optional(NBT)

        return Command(head, ops)


    def mc_command_tag(self, head, ops):

        ops.append(self.target())

        self.read_op(ops, STRING)
        self.read_op_optional(ops, STRING)

        return Command(head, ops)


    def mc_command_team(self, head, ops):

        self.read_op(ops, STRING)

        if self.current_token.type in (TARGET, STRING):
            ops.append(self.target())

        elif self.read_op_optional(ops, STRING):

            if self.current_token.type in (TARGET, STRING):
                ops.append(self.target())
            elif self.read_op_optional(ops, STRING):

                if self.current_token.type in number_types:
                    ops.append(self.number())

        return Command(head, ops)

    def mc_command_teleport(self, head, ops):

        ops.append(self.target())

        if self.current_token.type == TARGET or self.current_token.type == STRING: # TP to target
            ops.append(self.target())
        elif self.current_token in number_types: # TP To location
            ops.append(self.location())

            if self.read_op_optional(ops, STRING): # facing

                if self.current_token.type == TARGET or self.current_token.type == STRING:
                    ops.append(self.target())
                    self.read_op_optional(ops, ID)
                else:
                    ops.append(self.location())

            else:
                ops.append(self.location())


        return Command(head, ops)


    def mc_command_tellraw(self, head, ops):

        ops.append(self.target())

        if self.current_token.type == ATTR_BEGIN:
            ops.append(self.list())
        else:
            ops.read_op(STRING, NBT)

        return Command(head, ops)


    def mc_command_title(self, head, ops):

        ops.append(self.target())
        self.read_op(ops, STRING)

        if self.read_op_optional(STRING):
            pass
        elif self.current_token.type in number_types:
            ops.append(self.number())
            ops.append(self.number())
            ops.append(self.number())

        return Command(head, ops)




    # Ignored Commands

    def mc_command_advancement(self, head, ops):
        pass


    def mc_command_ban(self, head, ops):
        pass


    def mc_command_ban_ip(self, head, ops):
        pass


    def mc_command_defaultgamemode(self, head, ops):
        pass


    def mc_command_deop(self, head, ops):
        pass


    def mc_command_help(self, head, ops):
        return mc_command_list()


    def mc_command_kick(self, head, ops):
        pass


    def mc_command_locate(self, head, ops):
        pass


    def mc_command_locatebiome(self, head, ops):
        pass


    def mc_command_loot(self, head, ops):
        pass


    def mc_command_msg(self, head, ops):
        pass


    def mc_command_op(self, head, ops):
        pass


    def mc_command_pardon(self, head, ops):
        pass


    def mc_command_pardon_ip(self, head, ops):
        pass


    def mc_command_publish(self, head, ops):
        pass


    def mc_command_save_all(self, head, ops):
        pass


    def mc_command_save_off(self, head, ops):
        pass


    def mc_command_save_on(self, head, ops):
        pass


    def mc_command_setidletimeout(self, head, ops):
        pass


    def mc_command_setworldspawn(self, head, ops):
        pass


    def mc_command_spectate(self, head, ops):
        pass


    def mc_command_spreadplayers(self, head, ops):
        pass


    def mc_command_whitelist(self, head, ops):
        pass


    def mc_command_empty(self, head, ops):
        pass

    # ==================================================================
    # Parser

    def parse(self):
        return self.function()

def run_parser(string):
    lex = Lexer(string)
    parser = Parser(lex)

    return parser.parse()