import subprocess

class Nodo:
    """Clase para representar un nodo de la lista doblemente enlazada."""

    def __init__(self, nombre, apellido, carnet):
        """Inicializa un nuevo nodo con los datos proporcionados."""
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    """Clase para representar una lista doblemente enlazada."""

    def __init__(self):
        """Inicializa una lista doblemente enlazada vacía."""
        self.primero = None
        self.ultimo = None

    def insertar_al_principio(self, nombre, apellido, carnet):
        """Inserta un nuevo nodo al principio de la lista."""
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if not self.primero:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        self.generar_grafo()

    def insertar_al_final(self, nombre, apellido, carnet):
        """Inserta un nuevo nodo al final de la lista."""
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if not self.primero:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.ultimo
            self.ultimo = nuevo_nodo
        self.generar_grafo()

    def eliminar_por_valor(self, carnet):
        """Elimina el nodo con el carnet proporcionado."""
        actual = self.primero
        while actual:
            if actual.carnet == carnet:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.primero = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.ultimo = actual.anterior
                self.generar_grafo()
                return True
            actual = actual.siguiente
        return False

    def mostrar_lista(self):
        """Muestra los elementos de la lista."""
        actual = self.primero
        lista_str = "None <- "
        while actual:
            lista_str += f"{actual.nombre} {actual.apellido} ({actual.carnet}) <-> "
            actual = actual.siguiente
        lista_str += "None"
        print(lista_str)

    def generar_grafo(self):
        """Genera un gráfico de la lista doblemente enlazada."""
        dot_file = "grafo.dot"
        with open(dot_file, "w") as f:
            f.write("digraph G {\n")
            actual = self.primero
            while actual:
                f.write(f'"{actual.nombre} {actual.apellido} ({actual.carnet})" [shape=box];\n')
                if actual.siguiente:
                    f.write(f'"{actual.nombre} {actual.apellido} ({actual.carnet})" -> "{actual.siguiente.nombre} {actual.siguiente.apellido} ({actual.siguiente.carnet})";\n')
                if actual.anterior:
                    f.write(f'"{actual.nombre} {actual.apellido} ({actual.carnet})" -> "{actual.anterior.nombre} {actual.anterior.apellido} ({actual.anterior.carnet})";\n')
                actual = actual.siguiente
            f.write("}")

        # Llama a Graphviz para generar el gráfico
        subprocess.call(["dot", "-Tpng", dot_file, "-o", "grafo.png"])


def main():
    """Función principal que ejecuta el programa."""
    lista = ListaDoblementeEnlazada()

    while True:
        print("\nMenú:")
        print("1. Insertar al principio")
        print("2. Insertar al final")
        print("3. Eliminar por carnet")
        print("4. Mostrar lista")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            carnet = input("Ingrese el carnet: ")
            lista.insertar_al_principio(nombre, apellido, carnet)
        elif opcion == "2":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            carnet = input("Ingrese el carnet: ")
            lista.insertar_al_final(nombre, apellido, carnet)
        elif opcion == "3":
            carnet = input("Ingrese el carnet del estudiante a eliminar: ")
            if not lista.eliminar_por_valor(carnet):
                print("El estudiante con ese carnet no está en la lista.")
        elif opcion == "4":
            lista.mostrar_lista()
            print("Se ha generado el grafo de la lista doblemente enlazada.")
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()
