import csv
from graphviz import Digraph

class MatrizDispersa:
    def __init__(self):
        self.matriz = None

    def cargar_desde_csv(self, nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)  # Omitir la primera fila (encabezados)
            self.matriz = [[float(valor) for valor in fila] for fila in lector_csv]

    def entrada_manual(self):
        print("Ingrese los datos para cada fila. Presione enter para valores vacíos.")
        self.matriz = []
        while True:
            fila = input("Ingrese la fila (valores separados por coma): ")
            if not fila:
                break
            valores = [float(valor) for valor in fila.split(',')]
            self.matriz.append(valores)

    def visualizar_consola(self):
        if self.matriz:
            for fila in self.matriz:
                print(fila)
        else:
            print("La matriz está vacía.")

    def generar_grafo(self):
        if self.matriz:
            grafo = Digraph()

            for fila in self.matriz:
                nodo_anterior = None
                for columna, valor in enumerate(fila):
                    if valor != 0:
                        nodo_actual = f"{fila[0]}_{columna}"
                        grafo.node(nodo_actual, label=f"({fila[0]}, {columna}): {valor}")
                        if nodo_anterior is not None:
                            grafo.edge(nodo_anterior, nodo_actual)
                        nodo_anterior = nodo_actual

            return grafo
        else:
            print("La matriz está vacía.")
            return None

    def guardar_grafo(self, nombre_archivo):
        grafo = self.generar_grafo()
        if grafo:
            grafo.render(nombre_archivo, format='png', view=False)

    def visualizar_graphviz(self):
        print("Grafo generado. El archivo de imagen se ha guardado.")
        self.guardar_grafo('matriz_dispersa')


def main():
    matriz_dispersa = MatrizDispersa()
    opcion = input("Elige una opción:\n1. Cargar datos desde CSV\n2. Entrada manual\n")

    if opcion == '1':
        filename = input("Ingresa el nombre del archivo CSV: ")
        matriz_dispersa.cargar_desde_csv(filename)
    elif opcion == '2':
        matriz_dispersa.entrada_manual()

    matriz_dispersa.visualizar_consola()
    matriz_dispersa.visualizar_graphviz()

if __name__ == "__main__":
    main()
