from lrparser import LRParser

class SDT:
    def __init__(self, source_code):
        self.parser = LRParser(source_code)
        self.tmp_var_pointer = 0

    def analysis(self):
        self.parser.parse()

        def new_var():
            self.tmp_var_pointer += 1
            return f"tmp_var_{self.tmp_var_pointer}"

        def top_down(ast_node, depth):
            if ast_node.value in ["id", "digits"]:
                return [], ast_node.children[0].value
            elif ast_node.value == "F":
                if ast_node.children[0].value != "(": # F→id|digits
                    return top_down(ast_node.children[0], depth + 1)
                else: # F→(E)
                    return top_down(ast_node.children[1], depth + 1)
            elif ast_node.value == "T":
                if ast_node.children[0].value == "F": # T→F
                    return top_down(ast_node.children[0], depth + 1)
                else: # T→T*F|T/F
                    code_left, var_left = top_down(ast_node.children[0], depth + 1)
                    code_right, var_right = top_down(ast_node.children[2], depth + 1)
                    var = new_var()
                    code = [*code_left, *code_right, f"{var}={var_left}{ast_node.children[1].value}{var_right};"]
                    return code, var
            elif ast_node.value == "E":
                if ast_node.children[0].value == "T": # E→T
                    return top_down(ast_node.children[0], depth + 1)
                else: # E→E+T|E-T
                    code_left, var_left = top_down(ast_node.children[0], depth + 1)
                    code_right, var_right = top_down(ast_node.children[2], depth + 1)
                    var = new_var()
                    code = [*code_left, *code_right, f"{var}={var_left}{ast_node.children[1].value}{var_right};"]
                    return code, var
            elif ast_node.value == "C":
                code_left, var_left = top_down(ast_node.children[0], depth + 1)
                code_right, var_right = top_down(ast_node.children[2], depth + 1)
                var = f"{var_left}{ast_node.children[1].value}{var_right}"
                code = [*code_left, *code_right]
                return code, var
            elif ast_node.value == "S":
                if ast_node.children[0].value == "id": # S→id=E;
                    code_left, var_left = top_down(ast_node.children[0], depth + 1)
                    code_right, var_right = top_down(ast_node.children[2], depth + 1)
                    code = [*code_left, *code_right, f"{var_left}={var_right};"]
                    return code, None
                elif ast_node.children[0].value == "S": # S→SS
                    code_left, var_left = top_down(ast_node.children[0], depth + 1)
                    code_right, var_right = top_down(ast_node.children[1], depth + 1)
                    code = [*code_left, *code_right]
                    return code, None
                elif ast_node.children[0].value == "if" and len(ast_node.children) == 5: # S→if(C)S
                    code_left, var_left = top_down(ast_node.children[2], depth + 1)
                    code_right, var_right = top_down(ast_node.children[4], depth + 1)
                    code = [*code_left, f"if({var_left})goto$+2", f"goto$+{len(code_right) + 1}", *code_right]
                    return code, None
                elif ast_node.children[0].value == "if" and len(ast_node.children) == 7: # S→if(C)SelseS
                    code_left, var_left = top_down(ast_node.children[2], depth + 1)
                    code_mid, var_mid = top_down(ast_node.children[4], depth + 1)
                    code_right, var_right = top_down(ast_node.children[6], depth + 1)
                    code = [*code_left, f"if({var_left})goto$+2", f"goto$+{len(code_mid) + 2}", *code_mid, f"goto$+{len(code_right) + 1}", *code_right]
                    return code, None
                elif ast_node.children[0].value == "while": # S→while(C)S
                    code_left, var_left = top_down(ast_node.children[2], depth + 1)
                    code_right, var_right = top_down(ast_node.children[4], depth + 1)
                    code = [*code_left, f"if({var_left})goto$+2", f"goto$+{len(code_right) + 2}", *code_right, f"goto$-{len(code_right) + 2}"]
                    return code, None
            elif ast_node.value in ["L", "D"]:
                return [], None
            elif ast_node.value == "P":
                code, var = top_down(ast_node.children[1], depth + 1)
                return ["[BEGIN]", *code], var

        code, var = top_down(self.parser.prefix[0], 0)
        intermediate_code = ""
        for index, line in enumerate(code):
            pos = line.find("$")
            if pos != -1:
                op, delta = line[pos + 1], int(line[pos + 2:])
                if op == "+": to_index = index + delta
                else: to_index = index - delta;
                line = line[:pos] + f"{to_index};"
            intermediate_code += f"{index}: {line}\n"
        intermediate_code += f"{len(code)}: [END]\n"
        return intermediate_code