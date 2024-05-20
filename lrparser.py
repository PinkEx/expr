from astree import AST
from get_analysis_table import keywords, symbols, first, follow, productions, lengths, action, goto, items_list
from lexer import Lexer

class LRParser:
    def __init__(self, source_code):
        self.lexer = Lexer(source_code)
        self.check = False
        self.stack = []
        self.prefix = []
        self.logs = {
            "reductions": [],
            "transitions": [],
        }

    def get_action(self, state, token_type):
        if token_type not in action[state].keys(): return None
        self.logs["transitions"].append(("action", state, token_type, action[state][token_type]))
        return action[state][token_type]
    
    def get_goto(self, state, token_type):
        if token_type not in goto[state].keys(): return None
        self.logs["transitions"].append(("goto", state, token_type, goto[state][token_type]))
        return goto[state][token_type]

    def reduce(self, symbol, production, length):
        self.logs["reductions"].append((symbol, production))

        ast_node = AST(symbol)
        for t in range(length):
            self.stack.pop()
            self.prefix[-1].set_parent(ast_node)
            self.prefix.pop()
        ast_node.children.reverse()
        self.prefix.append(ast_node)

        state = self.stack[-1]
        new_state = int(self.get_goto(state, symbol)[1:])
        self.stack.append(new_state)

    def parse(self):
        self.stack.append(0)
        while True:
            state = self.stack[-1]
            if not self.check:
                token_type, token = self.lexer.next_token()
                if token_type in ["KEYWORD", "OPERATOR", "DELIMITER"]:
                    token_type = token
                elif token_type == "IDENTIFIER":
                    token_type = "id"
                elif token_type == "DIGITS":
                    token_type = "digits"
                elif token_type == "ERROR":
                    break

            a = self.get_action(state, token_type)
            if a is None: break
            if a[0] == "s":
                new_state = int(a[1:])
                self.stack.append(new_state)
                self.prefix.append(AST(token))
                if token_type in ["id", "digits"]:
                    self.prefix[-1].set_parent(AST(token_type))
                    self.prefix[-1] = self.prefix[-1].parent
                self.check = False
            elif a[0] == "r":
                for symbol in symbols:
                    if a.find(symbol) == 1:
                        production = productions[symbol][int(a.partition(symbol)[2])]
                        length = lengths[symbol][int(a.partition(symbol)[2])]
                        self.reduce(symbol, production, length)
                        self.check = True
                        break
            elif a == "acc": return True
            else: break
        return False