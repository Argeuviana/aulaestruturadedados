from graphviz import Digraph
import random

# -----------------------------
# CLASSE DO NÓ DA ÁRVORE
# -----------------------------
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# -----------------------------
# PARSER DE EXPRESSÃO PARA ÁRVORE
# -----------------------------
def parse_expression(expr):
    tokens = expr.replace("(", " ( ").replace(")", " ) ").split()
    return build_tree(tokens)


def build_tree(tokens):
    token = tokens.pop(0)

    if token == "(":
        left = build_tree(tokens)
        op = tokens.pop(0)
        right = build_tree(tokens)
        tokens.pop(0)  # remove ')'
        return Node(op, left, right)

    else:
        return Node(token)


# -----------------------------
# FUNÇÃO PARA DESENHAR A ÁRVORE COM GRAPHVIZ
# -----------------------------
def draw_tree(node, graph=None, parent=None):
    if graph is None:
        graph = Digraph()
        graph.attr("node", shape="circle", fontsize="14")

    graph.node(str(id(node)), label=str(node.value))

    if parent:
        graph.edge(str(id(parent)), str(id(node)))

    if node.left:
        draw_tree(node.left, graph, node)
    if node.right:
        draw_tree(node.right, graph, node)

    return graph


# -----------------------------
# GERAR EXPRESSÃO ALEATÓRIA
# -----------------------------
def gerar_expressao_randomica():
    operadores = ["+", "-", "*", "/"]
    nums = [str(random.randint(1, 9)) for _ in range(3)]

    # Garante ao menos 2 operadores
    op1 = random.choice(operadores)
    op2 = random.choice(operadores)

    # Expressão parentizada
    expr = f"( ( {nums[0]} {op1} {nums[1]} ) {op2} {nums[2]} )"
    return expr


# -----------------------------
# PARTE 1 – ÁRVORE FIXA
# -----------------------------
expr_fixa = "( ( 7 + 3 ) * ( 5 - 2 ) )"
arvore_fixa = parse_expression(expr_fixa)
graph_fixa = draw_tree(arvore_fixa)
graph_fixa.render("arvore_fixa", format="png", cleanup=True)


# -----------------------------
# PARTE 2 – ÁRVORE RANDÔMICA
# -----------------------------
expr_random = gerar_expressao_randomica()
arvore_random = parse_expression(expr_random)
graph_random = draw_tree(arvore_random)
graph_random.render("arvore_random", format="png", cleanup=True)

print("Árvore fixa e árvore randômica geradas com sucesso!")
print(f"Expressão randômica utilizada: {expr_random}")
