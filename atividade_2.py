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
    # BUSCAR
    # -----------------------------
    def search(self, valor):
        return self._search(self.root, valor)

    def _search(self, node, valor):
        if node is None:
            return False
        if valor == node.valor:
            return True
        elif valor < node.valor:
            return self._search(node.left, valor)
        else:
            return self._search(node.right, valor)

    # -----------------------------
    # REMOVER
    # -----------------------------
    def delete(self, valor):
        self.root = self._delete(self.root, valor)

    def _delete(self, node, valor):
        if node is None:
            return None

        if valor < node.valor:
            node.left = self._delete(node.left, valor)
        elif valor > node.valor:
            node.right = self._delete(node.right, valor)
        else:
            # Caso 1: nó folha
            if node.left is None and node.right is None:
                return None

            # Caso 2: nó com um filho
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            # Caso 3: dois filhos
            sucessor = self._min_value_node(node.right)
            node.valor = sucessor.valor
            node.right = self._delete(node.right, sucessor.valor)

        return node

    def _min_value_node(self, node):
        atual = node
        while atual.left:
            atual = atual.left
        return atual

    # -----------------------------
    # ALTURA DA ÁRVORE
    # -----------------------------
    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if not node:
            return -1  # altura da árvore vazia é -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # -----------------------------
    # PROFUNDIDADE DE UM NÓ
    # -----------------------------
    def depth(self, valor):
        return self._depth(self.root, valor, 0)

    def _depth(self, node, valor, nivel):
        if node is None:
            return None
        if node.valor == valor:
            return nivel

        if valor < node.valor:
            return self._depth(node.left, valor, nivel + 1)
        else:
            return self._depth(node.right, valor, nivel + 1)

    # -----------------------------
    # DESENHAR ÁRVORE COM GRAPHVIZ
    # -----------------------------
    def visualize(self, filename):
        graph = Digraph()
        graph.attr("node", shape="circle", fontsize="14")

        def add_nodes_edges(node):
            if node is None:
                return
            graph.node(str(id(node)), label=str(node.valor))
            if node.left:
                graph.edge(str(id(node)), str(id(node.left)))
                add_nodes_edges(node.left)
            if node.right:
                graph.edge(str(id(node)), str(id(node.right)))
                add_nodes_edges(node.right)

        add_nodes_edges(self.root)
        graph.render(filename, format="png", cleanup=True)


# -----------------------------------------------------------
# DEMONSTRAÇÃO
# -----------------------------------------------------------
if __name__ == "__main__":
    print("\n=== ÁRVORE COM VALORES FIXOS ===")

    valores_fixos = [55, 30, 80, 20, 45, 70, 90]
    bst1 = BinarySearchTree()

    for v in valores_fixos:
        bst1.insert(v)

    # Visualizar árvore inicial
    bst1.visualize("bst_fixa")
    print("Árvore fixa gerada: bst_fixa.png")

    # Busca
    print("Buscar 45:", bst1.search(45))

    # Remoção
    bst1.delete(30)
    bst1.visualize("bst_fixa_apos_delete")
    print("Árvore após remover 30: bst_fixa_apos_delete.png")

    # Nova inserção
    bst1.insert(25)
    bst1.visualize("bst_fixa_apos_insert")
    print("Árvore após inserir 25: bst_fixa_apos_insert.png")

    # Altura
    print("Altura da árvore fixa:", bst1.height())

    # Profundidade
    print("Profundidade do nó 45:", bst1.depth(45))

    # --------------------------------------------------------
    # ÁRVORE ALEATÓRIA
    # --------------------------------------------------------
    print("\n=== ÁRVORE COM VALORES RANDÔMICOS ===")

    valores_random = random.sample(range(1, 200), 15)
    print("Valores aleatórios:", valores_random)

    bst2 = BinarySearchTree()

    for v in valores_random:
        bst2.insert(v)

    bst2.visualize("bst_random")
    print("Árvore randômica gerada: bst_random.png")
    print("Altura:", bst2.height())
