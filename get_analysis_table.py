symbols = [
    "O", "P", "D", "L", "S", "C", "E", "T", "F"
]

keywords = [
    "id", "digits", "int", "float", "if", "else", "while", "=", "(", ")", "<", ">", "==", "+", "-", "*", "/", ";", "$"
]

first = {
    "O": ["int", "float", ""],
    "P": ["int", "float", ""],
    "D": ["int", "float", ""],
    "L": ["int", "float"],
    "S": ["id", "if", "while"],
    "C": ["id", "digits", "("],
    "E": ["id", "digits", "("],
    "T": ["id", "digits", "("],
    "F": ["id", "digits", "("]
}

follow = {
    "O": [],
    "P": ["$"],
    "D": ["id", "if", "while"],
    "L": ["id"],
    "S": ["id", "if", "else", "while", "$"],
    "C": [")"],
    "E": [";", ">", "<", "==", "+", "-", ")"],
    "T": [";", ">", "<", "==", "+", "-", "*", "/", ")"],
    "F": [";", ">", "<", "==", "+", "-", "*", "/", ")"],
}

productions = {
    "O": ["P$"],
    "P": ["DS"],
    "D": ["Lid;D", ""],
    "L": ["int", "float"],
    "S": ["id=E;", "SS", "if(C)S", "if(C)SelseS", "while(C)S"],
    "C": ["E>E", "E<E", "E==E"],
    "E": ["T", "E+T", "E-T"],
    "T": ["F", "T*F", "T/F"],
    "F": ["id", "digits", "(E)"]
}

lengths = {
    "O": [2],
    "P": [2],
    "D": [4, 0],
    "L": [1, 1],
    "S": [4, 2, 5, 7, 5],
    "C": [3, 3, 3],
    "E": [1, 3, 3],
    "T": [1, 3, 3],
    "F": [1, 1, 3]
}

def partition(item):
    for symbol in symbols:
        if item.find(symbol) == 0:
            parts = item.partition(symbol)
            return parts[1], parts[2].strip()
    return None

def closure(items):
    while True:
        flag = False
        for item in items:
            parts = partition(item[2])
            if parts is None: continue
            for production in productions[parts[0]]:
                new_item = (parts[0], "", production)
                if new_item not in items:
                    items.append(new_item)
                    flag = True
        if not flag:
            return sorted(items)

items_list = [
    closure([("O", "", "P")])
]

def go_keyword(items, keyword):
    new_items = []
    for item in items:
        if item[2].find(keyword) != 0:
            continue
        parts = item[2].partition(keyword)
        new_items.append((item[0], item[1] + parts[1], parts[2].strip()))
    new_items = closure(new_items)
    if items_list.count(new_items) == 0:
        items_list.append(new_items)
    return new_items

def go_symbol(items, symbol):
    new_items = []
    for item in items:
        if item[2].find(symbol) != 0:
            continue
        parts = item[2].partition(symbol)
        new_items.append((item[0], item[1] + parts[1], parts[2].strip()))
    new_items = closure(new_items)
    if items_list.count(new_items) == 0:
        items_list.append(new_items)
    return new_items

while True:
    ori_items_list = items_list.copy()
    for items in ori_items_list:
        for keyword in keywords:
            go_keyword(items, keyword)
        for symbol in symbols:
            go_symbol(items, symbol)
    if len(items_list) == len(ori_items_list):
        break


action = [{} for i in range(len(items_list))]
goto = [{} for i in range(len(items_list))]

for index, items in enumerate(items_list):
    for item in items:
        if item[2] != "":
            continue
        if item[0] != "O":
            for keyword in follow[item[0]]:
                action[index][keyword] = f"r{item[0]}{productions[item[0]].index(item[1])}"
        else:
            action[index]["$"] = "acc"
    for keyword in keywords:
        flag = False
        for item in items:
            if item[2].find(keyword) == 0:
                flag = True
                break
        if flag:
            items_o = go_keyword(items, keyword)
            action[index][keyword] = f"s{items_list.index(items_o)}"
    for symbol in symbols:
        flag = False
        for item in items:
            if item[2].find(symbol) == 0:
                flag = True
                break
        if flag:
            items_o = go_symbol(items, symbol)
            goto[index][symbol] = f"s{items_list.index(items_o)}"

# for i in range(len(items_list)):
#     print(i, items_list[i])
#
# print("s ", end="")
# for keyword in keywords:
#     print(keyword.rjust(6), end="")
# for symbol in symbols:
#     print(symbol.rjust(6), end="")
# print()
# for i in range(len(items_list)):
#     print(str(i).ljust(2), end="")
#     for keyword in keywords:
#         if keyword in action[i].keys():
#             print(action[i][keyword].rjust(6), end="")
#         else:
#             print("      ", end="")
#     for symbol in symbols:
#         if symbol in goto[i].keys():
#             print(goto[i][symbol].rjust(6), end="")
#         else:
#             print("      ", end="")
#     print()