import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text
import random
import pydot
from graphviz import Source

# Clase que representa un nodo del árbol AVL
class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

# Clase que representa un árbol AVL
class AVLTree:
    # Inserta un nodo en el árbol AVL y lo balancea si es necesario
    def insert(self, root, key, value):
        if not root:
            return AVLNode(key, value)
        elif key < root.key:
            root.left = self.insert(root.left, key, value)
        else:
            root.right = self.insert(root.right, key, value)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Balancea el árbol
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # Realiza una rotación a la izquierda
    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Realiza una rotación a la derecha
    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Obtiene la altura de un nodo
    def get_height(self, root):
        if not root:
            return 0
        return root.height

    # Obtiene el balance de un nodo
    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    # Realiza un recorrido en preorden del árbol AVL
    def pre_order(self, root):
        res = []
        if root:
            res.append((root.key, root.value))
            res = res + self.pre_order(root.left)
            res = res + self.pre_order(root.right)
        return res

    # Guarda el árbol AVL como una imagen
    def save_to_graph(self, root, filename="avl_tree.png"):
        def add_edges(node, graph):
            if node.left:
                graph.add_edge(pydot.Edge(f"{node.key}\n{node.value}", f"{node.left.key}\n{node.left.value}"))
                add_edges(node.left, graph)
            if node.right:
                graph.add_edge(pydot.Edge(f"{node.key}\n{node.value}", f"{node.right.key}\n{node.right.value}"))
                add_edges(node.right, graph)

        graph = pydot.Dot(graph_type="digraph")
        if root:
            graph.add_node(pydot.Node(f"{root.key}\n{root.value}"))
            add_edges(root, graph)
        graph.write_png(filename)

# Clase que representa el juego del TicTacToe
class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Totito - Proyecto Final")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.player_wins = 0
        self.machine_wins = 0
        self.draws = 0
        self.player_win_moves = []  # Historial de movimientos ganadores del jugador
        self.move_history = []  # Historial de movimientos
        self.avl_tree = AVLTree()
        self.avl_root = None
        self.create_widgets()

    # Crea los widgets de la interfaz
    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        # Agregar los nombres y carnets
        names_label = tk.Label(self.root, text="Francisco Alexander Chic Barrios 9490-22-2513\n"
                                               "Herbert Daniel Jocol Morataya 9490-22-423\n"
                                               "Eros Andre Motta Escobar 9490-21-1813", font=("Arial", 12))
        names_label.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

        self.reset_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game)
        self.reset_button.pack()

        self.score_label = tk.Label(self.root, text=f"Jugador: {self.player_wins} - Máquina: {self.machine_wins} - Empates: {self.draws}")
        self.score_label.pack()

        self.move_history_label = tk.Label(self.root, text="Movimientos: ")
        self.move_history_label.pack()

        self.avl_tree_label = tk.Label(self.root, text="Árbol AVL: ")
        self.avl_tree_label.pack()

    # Maneja el evento de clic en un botón
    def on_button_click(self, i, j):
        if self.board[i][j] == " ":
            self.board[i][j] = self.current_player
            self.buttons[i][j].config(text=self.current_player)
            self.move_history.append(f"{self.current_player}: ({i}, {j})")
            self.avl_root = self.avl_tree.insert(self.avl_root, len(self.move_history), f"{self.current_player}: ({i}, {j})")
            self.update_move_history()
            self.update_avl_tree()
            if self.check_winner(self.current_player):
                messagebox.showinfo("Fin del juego", f"¡{self.current_player} ha ganado!")
                if self.current_player == "X":
                    self.player_wins += 1
                    self.player_win_moves.append(self.get_player_moves())
                else:
                    self.machine_wins += 1
                self.update_score()
                self.ask_play_again()
            elif self.check_draw():
                messagebox.showinfo("Fin del juego", "¡Es un empate!")
                self.draws += 1
                self.update_score()
                self.ask_play_again()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.machine_turn()

    # Maneja el turno de la máquina
    def machine_turn(self):
        best_move = self.get_best_move()
        if best_move:
            i, j = best_move
        else:
            available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
            i, j = random.choice(available_moves)

        self.board[i][j] = "O"
        self.buttons[i][j].config(text="O")
        self.move_history.append(f"O: ({i}, {j})")
        self.avl_root = self.avl_tree.insert(self.avl_root, len(self.move_history), f"O: ({i}, {j})")
        self.update_move_history()
        self.update_avl_tree()
        if self.check_winner("O"):
            messagebox.showinfo("Fin del juego", "¡La máquina ha ganado!")
            self.machine_wins += 1
            self.update_score()
            self.ask_play_again()
        elif self.check_draw():
            messagebox.showinfo("Fin del juego", "¡Es un empate!")
            self.draws += 1
            self.update_score()
            self.ask_play_again()
        else:
            self.current_player = "X"

    # Obtiene el mejor movimiento para la máquina
    def get_best_move(self):
        # Primero, verifica si la máquina puede ganar en su próximo movimiento
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        return (i, j)
                    self.board[i][j] = " "

        # Si la máquina no puede ganar, intenta bloquear al jugador
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = "O"
                        return (i, j)
                    self.board[i][j] = " "

        # Si no se puede ganar ni bloquear, busca bloquear las estrategias ganadoras previas del jugador
        for move in self.player_win_moves:
            for i in range(3):
                for j in range(3):
                    if move[i][j] == "X" and self.board[i][j] == " ":
                        # Comprueba si el movimiento del jugador coincide con uno anterior
                        if self.check_duplicate_move(move):
                            continue  # Si es un movimiento duplicado, pasa al siguiente
                        self.board[i][j] = "O"
                        if self.check_winner("O"):
                            return (i, j)
                        self.board[i][j] = " "

        # Si no se puede bloquear ninguna estrategia previa, elige una casilla al azar
        available_moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == " "]
        return random.choice(available_moves) if available_moves else None

    # Verifica si un movimiento es duplicado
    def check_duplicate_move(self, move):
        for prev_move in self.player_win_moves:
            if prev_move == move:
                return True
        return False

    # Obtiene los movimientos del jugador
    def get_player_moves(self):
        return [[self.board[i][j] for j in range(3)] for i in range(3)]

    # Verifica si un jugador ha ganado
    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or \
           all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    # Verifica si hay un empate
    def check_draw(self):
        return all(self.board[i][j] != " " for i in range(3) for j in range(3))

    # Desactiva los botones del tablero
    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state=tk.DISABLED)

    # Reinicia el juego
    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.move_history = []
        self.avl_root = None
        self.update_move_history()
        self.update_avl_tree()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state=tk.NORMAL)

    # Pregunta al jugador si quiere jugar otra vez
    def ask_play_again(self):
        self.show_avl_tree()  # Muestra el árbol AVL en una nueva ventana
        self.avl_tree.save_to_graph(self.avl_root, "avl_tree.png")  # Guarda el árbol AVL como una imagen
        self.disable_buttons()
        play_again = messagebox.askyesno("Jugar de nuevo", "¿Quieres jugar otra vez?")
        if play_again:
            self.reset_game()
        else:
            self.root.quit()

    # Actualiza el marcador
    def update_score(self):
        self.score_label.config(text=f"Jugador: {self.player_wins} - Máquina: {self.machine_wins} - Empates: {self.draws}")

    # Actualiza el historial de movimientos
    def update_move_history(self):
        self.move_history_label.config(text="Movimientos: " + ", ".join(self.move_history))

    # Actualiza la visualización del árbol AVL
    def update_avl_tree(self):
        pre_order = self.avl_tree.pre_order(self.avl_root)
        avl_text = "Árbol AVL: " + ", ".join([f"{k}: {v}" for k, v in pre_order])
        self.avl_tree_label.config(text=avl_text)

    # Muestra el árbol AVL en una nueva ventana
    def show_avl_tree(self):
        new_window = Toplevel(self.root)
        new_window.title("Árbol AVL")

        scrollbar = Scrollbar(new_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        avl_text_widget = Text(new_window, wrap=tk.NONE, yscrollcommand=scrollbar.set)
        pre_order = self.avl_tree.pre_order(self.avl_root)
        avl_text = "\n".join([f"{k}: {v}" for k, v in pre_order])
        avl_text_widget.insert(tk.END, avl_text)
        avl_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=avl_text_widget.yview)

# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
