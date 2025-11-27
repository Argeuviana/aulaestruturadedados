from graphviz import Digraph
import random

# -----------------------------------------------------------
# NÓ DA ÁRVORE AVL
# -----------------------------------------------------------
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.left = None
        self.right = None
        self.height = 1  # Altura inicial


# -----------------------------------------------------------
# ÁRVORE AVL
# -----------------------------------------------------------
class AVLTree:

    def insert(self, root, key):
        """
        Inserção padrão de BST + rebalanceamento AVL
        """
        # 1 — Inserção normal de BST
        if not root:
            return Node(key)
        elif key < root.valor:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        # 2 — Atualizar altura
        root.height = 1 + max(self.get_height(root.left),
                              self.get_height(root.right))

        # 3 — Calcular fator de balanceamento
        balance = self.get_balance(root)

        # 4 — Casos de desbalanceamento
        # Caso LL → Rotação direita
        if balance > 1 and key < root.left.valor:
            return self.rotate_right(root)

        # Caso RR → Rotação esquerda
        if balance < -1 and key > root.right.valor:
            return self.rotate_left(root)

        # Caso LR → Rotação esquerda no filho + rotação direita
        if balance > 1 and key > root.left.valor:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)

        # Caso RL → Rotação direita no filho + rotação esquerda
        if balance < -1 and key < root.right.valor:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    # -----------------------------------------------------------
    # ALTURA E FATOR DE BALANCEAMENTO
    # -----------------------------------------------------------
    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # -----------------------------------------------------------
    # ROTAÇÃO À DIREITA
    # -----------------------------------------------------------
    def rotate_right(self, z):
        y = z.left
        T3 = y.right

        # Rotação
        y.right = z
        z.left = T3

        # Atualizar alturas
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # -----------------------------------------------------------
    # ROTAÇÃO À ESQUERDA
    # -----------------------------------------------------------
    def rotate_left(self, z):
        y = z.right
        T2 = y.left

        # Rotação
        y.left = z
        z.right = T2

        # Atualizar alturas
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    # -----------------------------------------------------------
    # VISUALIZAÇÃO COM GRAPHVIZ
    # -----------------------------------------------------------
    def visualize(self, root, filename):
        graph = Digraph()
        graph.attr("node", shape="circle", fontsize="14")

        def add_nodes(node):
            if not node:
                return

            graph.node(str(id(node)), label=str(node.valor))

            if node.left:
                graph.edge(str(id(node)), str(id(node.left)))
                add_nodes(node.left)

            if node.right:
                graph.edge(str(id(node)), str(id(node.right)))
                add_nodes(node.right)

        add_nodes(root)
        graph.render(filename, format="png", cleanup=True)


# -----------------------------------------------------------
# DEMONSTRAÇÃO COMPLETA
# -----------------------------------------------------------
if __name__ == "__main__":

    avl = AVLTree()

    print("\n=== DEMONSTRAÇÃO DE ROTAÇÃO SIMPLES ===")
    root = None
    seq1 = [10, 20, 30]   # Força rotação RR

    for i, v in enumerate(seq1, start=1):
        root = avl.insert(root, v)
        avl.visualize(root, f"avl_rotacao_simples_step{i}")
        print(f"Inserido {v} → imagem gerada: avl_rotacao_simples_step{i}.png")

    print("\n=== DEMONSTRAÇÃO DE ROTAÇÃO DUPLA ===")
    avl2 = AVLTree()
    root2 = None
    seq2 = [10, 30, 20]   # Força rotação RL

    for i, v in enumerate(seq2, start=1):
        root2 = avl2.insert(root2, v)
        avl2.visualize(root2, f"avl_rotacao_dupla_step{i}")
        print(f"Inserido {v} → imagem gerada: avl_rotacao_dupla_step{i}.png")

    print("\n=== ÁRVORE AVL COM VALORES ALEATÓRIOS ===")
    avl3 = AVLTree()
    root3 = None
    valores = random.sample(range(1, 200), 20)
    print("Valores aleatórios inseridos:", valores)

    for v in valores:
        root3 = avl3.insert(root3, v)

    # Visualização da árvore final
    avl3.visualize(root3, "avl_random_final")
    print("Árvore AVL final aleatória → avl_random_final.png")
