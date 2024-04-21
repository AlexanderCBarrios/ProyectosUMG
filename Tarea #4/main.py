import os
import csv
import graphviz
from flask import Flask, jsonify, request

app = Flask(__name__)

class Pokemon:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None
    
    def insert(self, root, number, name):
        if not root:
            return Pokemon(number, name)
        elif number < root.number:
            root.left = self.insert(root.left, number, name)
        else:
            root.right = self.insert(root.right, number, name)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and number < root.left.number:
            return self.rightRotate(root)

        if balance < -1 and number > root.right.number:
            return self.leftRotate(root)

        if balance > 1 and number > root.left.number:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and number < root.right.number:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def search(self, root, number):
        if not root or root.number == number:
            return root
        if root.number < number:
            return self.search(root.right, number)
        return self.search(root.left, number)

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

def load_csv_data():
    csv_file_path = "pokemon.csv"
    avl_tree = AVLTree()
    
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pokemon_number = int(row.get('#'))
                pokemon_name = row.get('Name')
                if pokemon_number and pokemon_name:
                    avl_tree.root = avl_tree.insert(avl_tree.root, pokemon_number, pokemon_name)
    else:
        print("El archivo CSV no se encontró en la ruta especificada.")
    
    return avl_tree

avl_tree = load_csv_data()

# Genera un archivo DOT con la representación del árbol AVL
def generate_dot_file(root, filename):
    dot = graphviz.Digraph(comment='AVL Tree', graph_attr={'size': '80,80'})  # Ajusta el tamaño de la imagen aquí
    add_nodes(root, dot)
    dot.render(filename, format='png', cleanup=True)  # No se ajusta el dpi aquí

def add_nodes(root, dot):
    if root:
        dot.node(str(root.number), label=str(root.number) + ': ' + root.name)
        if root.left:
            dot.edge(str(root.number), str(root.left.number))
            add_nodes(root.left, dot)
        if root.right:
            dot.edge(str(root.number), str(root.right.number))
            add_nodes(root.right, dot)

generate_dot_file(avl_tree.root, 'avl_tree')

@app.route('/list_pokemon', methods=['GET'])
def list_pokemon():
    list_pokemon = []
    inorder_traversal(avl_tree.root, list_pokemon)
    return jsonify({'list_pokemon': list_pokemon}), 200

@app.route('/search_pokemon/<int:number>', methods=['GET'])
def search_pokemon(number):
    pokemon = avl_tree.search(avl_tree.root, number)
    if pokemon:
        return jsonify({'number': pokemon.number, 'name': pokemon.name}), 200
    else:
        return jsonify({'message': 'No se encontró un Pokémon con el número: {}'.format(number)}), 404

@app.route('/insert_pokemon', methods=['POST'])
def insert_pokemon():
    data = request.get_json()
    if 'number' not in data or 'name' not in data:
        return jsonify({'error': 'Se requiere un número y un nombre para insertar un Pokémon'}), 400
    number = data['number']
    name = data['name']
    avl_tree.root = avl_tree.insert(avl_tree.root, number, name)
    return jsonify({'message': 'Pokémon insertado exitosamente'}), 200

@app.route('/group_info', methods=['GET'])
def group_info():
    group_info = {
        'members': [
            {
                'name': 'Francisco Alexander Chic Barrios',
                'carnet': '9490-22-2513',
                'contributions': 'Carga de archivo csv a programa'
            },
            {
                'name': 'Herbert Daniel',
                'carnet': '9490-22-403',
                'contributions': 'Estructura de los Arbol AVL'
            },
            {
                'name': 'Eros Motta',
                'carnet': '9490-19-4013',
                'contributions': 'Conexion con postman y uso de graphiz'
            }
            # Agrega más miembros si es necesario
        ]
    }
    return jsonify(group_info), 200



def inorder_traversal(root, pokemon_list):
    if root:
        inorder_traversal(root.left, pokemon_list)
        pokemon_list.append({'number': root.number, 'name': root.name})
        inorder_traversal(root.right, pokemon_list)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
