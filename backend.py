import pandas as pd

from lexer import Lexer
from lrparser import LRParser, items_list, keywords, symbols, action, goto, productions
from sdt import SDT

def tokenize(source_code):
    lexer = Lexer(source_code)
    tokens = []
    token_type, token = lexer.next_token()
    while token is not None:
        tokens.append((token_type, token))
        token_type, token = lexer.next_token()
    symbol_table = {
        "name": [],
        "type": [],
        "kind": [],
        "scope": [],
        "addr": []
    }
    for symbol in lexer.symbol_table:
        symbol_table["name"].append(symbol["name"])
        symbol_table["type"].append(symbol["type"])
        symbol_table["kind"].append(symbol["kind"])
        symbol_table["scope"].append(symbol["scope"])
        symbol_table["addr"].append(symbol["addr"])

    return "\n".join([f"{token[0]}: {token[1]}" for token in tokens]), pd.DataFrame(symbol_table)

def get_productions():
    productions_table = {
        "id": list(range(5))
    }
    for symbol in symbols:
        productions_table[symbol] = [""] * 5
        for index, production in enumerate(productions[symbol]):
            productions_table[symbol][index] = production
    return pd.DataFrame(productions_table)

def get_SLR_table():
    SLR_table = {
        "state": list(range(len(items_list))),
    }
    for keyword in keywords:
        lst = []
        for index in range(len(items_list)):
            if keyword in action[index].keys():
                lst.append(action[index][keyword])
            else:
                lst.append("")
        SLR_table[keyword] = lst

    for symbol in symbols:
        lst = []
        for index in range(len(items_list)):
            if symbol in goto[index].keys():
                lst.append(goto[index][symbol])
            else:
                lst.append("")
        SLR_table[symbol] = lst

    return pd.DataFrame(SLR_table)

def translate(source_code):
    input_code = source_code.strip()
    parser = LRParser(source_code + "$")
    success = parser.parse()
    reduction_logs = [
        "→".join(list(reduction)) for reduction in parser.logs["reductions"]
    ]
    reduction_code = "\n".join(reduction_logs)
    transition_logs = [
       f"{transition[0]}({transition[1]},{transition[2]})={transition[3]}" for transition in parser.logs["transitions"]
    ]
    transition_code = "\n".join(transition_logs)
    return input_code, reduction_code, transition_code, success

def analysis(source_code):
    input_code = source_code.strip()
    sdt = SDT(input_code + "$")
    intermediate_code = sdt.analysis()
    ast_code = sdt.parser.prefix[0].get_AST(0)
    return ast_code, intermediate_code
