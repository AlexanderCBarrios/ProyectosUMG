import os
import graphviz

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        self.root = self._insert_rec(self.root, key)
    
    def _insert_rec(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.key:
            root.left = self._insert_rec(root.left, key)
        elif key > root.key:
            root.right = self._insert_rec(root.right, key)
        return root
    
    def search(self, key):
        return self._search_rec(self.root, key)
    
    def _search_rec(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search_rec(root.left, key)
        return self._search_rec(root.right, key)
    
    def delete(self, key):
        self.root = self._delete_rec(self.root, key)
    
    def _delete_rec(self, root, key):
        if root is None:
            return root
        if key < root.key:
            root.left = self._delete_rec(root.left, key)
        elif key > root.key:
            root.right = self._delete_rec(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            root.key = self._min_value_node(root.right).key
            root.right = self._delete_rec(root.right, root.key)
        return root
    
    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def to_graphviz(self):
        # Obtenemos la ruta completa del directorio donde se encuentra el script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dot_file = os.path.join(current_dir, "grafo.dot")

        dot = graphviz.Digraph()
        self._to_graphviz_rec(dot, self.root)
        dot.render(dot_file, format='png', cleanup=True)
        return dot
    
    def _to_graphviz_rec(self, dot, node):
        if node is not None:
            dot.node(str(node.key))
            if node.left is not None:
                dot.edge(str(node.key), str(node.left.key))
                self._to_graphviz_rec(dot, node.left)
            if node.right is not None:
                dot.edge(str(node.key), str(node.right.key))
                self._to_graphviz_rec(dot, node.right)

def load_from_file(filename, tree):
    with open(filename, 'r') as file:
        for line in file:
            key = int(line.strip())
            tree.insert(key)

def display_menu():
    print("1. Insertar")
    print("2. Buscar")
    print("3. Eliminar")
    print("4. Cargar desde archivo")
    print("5. Generar representación en Graphviz")
    print("6. Salir")

def main():
    tree = BinarySearchTree()
    while True:
        display_menu()
        choice = input("Selecciona una opción: ")
        if choice == '1':
            key = int(input("Ingrese el número a insertar: "))
            tree.insert(key)
            print(f"Número {key} insertado correctamente.")
        elif choice == '2':
            key = int(input("Ingrese el número a buscar: "))
            if tree.search(key):
                print(f"El número {key} está presente en el árbol.")
            else:
                print(f"El número {key} no está presente en el árbol.")
        elif choice == '3':
            key = int(input("Ingrese el número a eliminar: "))
            if tree.search(key):
                tree.delete(key)
                print(f"Número {key} eliminado correctamente.")
            else:
                print(f"El número {key} no está presente en el árbol.")
        elif choice == '4':
            filename = input("Ingrese el nombre del archivo: ")
            load_from_file(filename, tree)
            print("Datos cargados desde el archivo.")
        elif choice == '5':
            dot = tree.to_graphviz()
            print("Representación en Graphviz generada como 'grafo.png' en la misma carpeta que el script.")
        elif choice == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione nuevamente.")

if __name__ == "__main__":
    main()
