import csv
import hashlib

class HashTree:
    def __init__(self):  # Corregir la definición del constructor
        self.tree = {}

    def insert(self, key, value):
        hash_key = self._hash(key)
        self.tree[hash_key] = value

    def manual_insert(self):
        key = input("Ingrese la clave: ")
        value = input("Ingrese el valor: ")
        self.insert(key, value)

    def load_from_csv(self, filename, key_column=None):
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            if not key_column:
                key_column = input("Ingrese el nombre de la columna que contiene las claves: ")
            for row in reader:
                key = row[key_column]
                self.insert(key, dict(row))

    def _hash(self, key):
        return hashlib.sha256(key.encode()).hexdigest()

    def get_by_key(self, key):
        hash_key = self._hash(key)
        return self.tree.get(hash_key)

    def search_by_value(self, value):
        print("Contenido del árbol hash:")
        found = False
        for key, val in self.tree.items():
            if val == value:
                found = True
                print(f"Clave: {key}, Valor: {val}")
        if not found:
            print("El valor no existe en el árbol hash.")

# Crear una instancia de HashTree
hash_tree = HashTree()

# Funciones del menú
def menu():
    print("1. Cargar datos desde un archivo CSV")
    print("2. Insertar manualmente valores en el árbol hash")
    print("3. Buscar por clave")
    print("4. Buscar por valor")
    print("5. Salir")

def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            csv_filename = input("Ingrese el nombre del archivo CSV (no olvide incluir la extensión .csv): ")
            hash_tree.load_from_csv(csv_filename)

        elif opcion == "2":
            hash_tree.manual_insert()

        elif opcion == "3":
            key_to_find = input("Ingrese la clave que desea buscar: ")
            result = hash_tree.get_by_key(key_to_find)
            if result:
                print("Valores encontrados:", result)
            else:
                print("La clave no existe en el árbol hash.")

        elif opcion == "4":
            value_to_find = input("Ingrese el valor que desea buscar: ")
            hash_tree.search_by_value(value_to_find)

        elif opcion == "5":
            print("¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":  # Corregir la verificación del módulo principal
    main()
