from graphviz import Digraph
import random

# -----------------------------------------------------------
# NÓ DA ÁRVORE
# -----------------------------------------------------------
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.left = None
        self.right = None


# -----------------------------------------------------------
# ÁRVORE BINÁRIA DE BUSCA
# -----------------------------------------------------------
class BinarySearchTree:
    def __init__(self):
        self.root = None

    # -----------------------------
    # INSERIR
    # -----------------------------
    def insert(self, valor):
        if self.root is None:
            self.root = Node(valor)
        else:
            self._insert(self.root, valor)

    def _insert(self, node, valor):
        if valor < node.valor:
            if node.left is None:
                node.left = Node(valor)
            else:
                self._insert(node.left, valor)
        else:
            if node.right is None:
                node.right = Node(valor)
            else:
                self._insert(node.right, valor)

    # -----------------------------
    # TRAVESSIAS DFS
    # -----------------------------
    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, node, lista):
        if node:
            self._inorder(node.left, lista)
            lista.append(node.valor)
            self._inorder(node.right, lista)
        return lista

    def preorder(self):
        return self._preorder(self.root, [])

    def _preorder(self, node, lista):
        if node:
            lista.append(node.valor)
            self._preorder(node.left, lista)
            self._preorder(node.right, lista)
        return lista

    def postorder(self):
        return self._postorder(self.root, [])

    def _postorder(self, node, lista):
        if node:
            self._postorder(node.left, lista)
            self._postorder(node.right, lista)
            lista.append(node.valor)
        return lista

    # -----------------------------
    # DESENHO COM GRAPHVIZ
    # -----------------------------
    def visualize(self, filename):
        graph = Digraph()
        graph.attr("node", shape="circle", fontsize="14")

        def add(node):
            if node is None:
                return
            graph.node(str(id(node)), label=str(node.valor))

            if node.left:
                graph.edge(str(id(node)), str(id(node.left)))
                add(node.left)

            if node.right:
                graph.edge(str(id(node)), str(id(node.right)))
                add(node.right)

        add(self.root)
        graph.render(filename, format="png", cleanup=True)


# -----------------------------------------------------------
# DEMONSTRAÇÃO — ÁRVORE FIXA E RANDÔMICA
# -----------------------------------------------------------
if __name__ == "__main__":

    print("\n=== ÁRVORE COM VALORES FIXOS ===")
    valores_fixos = [55, 30, 80, 20, 45, 70, 90]

    bst1 = BinarySearchTree()
    for v in valores_fixos:
        bst1.insert(v)

    # Visualizar
    bst1.visualize("bst_fixa_dfs")
    print("Imagem gerada: bst_fixa_dfs.png")

    # Travessias
    print("In-Order  :", bst1.inorder())
    print("Pre-Order :", bst1.preorder())
    print("Post-Order:", bst1.postorder())

    # -----------------------------------------------------------
    print("\n=== ÁRVORE COM VALORES RANDÔMICOS ===")
    valores_random = random.sample(range(1, 200), 10)
    print("Valores usados:", valores_random)

    bst2 = BinarySearchTree()
    for v in valores_random:
        bst2.insert(v)

    # Visualizar
    bst2.visualize("bst_random_dfs")
    print("Imagem gerada: bst_random_dfs.png")

    # Travessias
    print("In-Order  :", bst2.inorder())
    print("Pre-Order :", bst2.preorder())
    print("Post-Order:", bst2.postorder())
