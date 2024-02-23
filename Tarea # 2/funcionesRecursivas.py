"""Alexander Barrios
    Ingenieria en sistemas
    Programacion 3
    Carnet: 9490-22-2513"""

def convertir_a_binario(numero):
    if numero <= 1:
        return str(numero)
    else:
        return convertir_a_binario(numero // 2) + str(numero % 2)


def contar_digitos(numero):
    if numero < 10:
        return 1
    else:
        return 1+contar_digitos(numero // 10)
    
    
def calcular_raiz_cuadrada(numero, candidato):
    """
    Función auxiliar recursiva para calcular la raíz cuadrada entera.
    """
    # Caso base: si el cuadrado del candidato es mayor que el número, retornamos el candidato anterior
    if candidato * candidato > numero:
        return candidato - 1
    else:
        return calcular_raiz_cuadrada(numero, candidato + 1)

def raiz_cuadrada_entera(numero):
    if numero in [0, 1]:
        return numero
    else:
        return calcular_raiz_cuadrada(numero, 1)



def convertir_a_decimal(numero_romano):
    romanos = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    if not numero_romano:
        return 0

    if len(numero_romano) == 1:
        return romanos[numero_romano]

    if romanos[numero_romano[0]] < romanos[numero_romano[1]]:
        return -romanos[numero_romano[0]] + convertir_a_decimal(numero_romano[1:])
    else:
        return romanos[numero_romano[0]] + convertir_a_decimal(numero_romano[1:])

def suma_numeros_enteros(numero):
    # Convertir la entrada del usuario a un número entero
    numero = int(numero)
    # Caso base: si el número es cero, la suma es cero
    if numero == 0:
        return 0
    # Llamada recursiva: suma el número actual con la suma de los números anteriores
    else:
        return numero + suma_numeros_enteros(numero - 1)


def mostrar_menu():
    print("**** Menú ****")
    print("1. Convertir a binario")
    print("2. Contar dígitos")
    print("3. Raíz cuadrada entera")
    print("4. Convertir a Decimal desde Romano")
    print("5. Suma de Números Enteros")
    print("6. Salir")

while True:
    mostrar_menu()
    seleccion = input("Selecciona una opción: ")

    if seleccion == "1":
        numero = int(input("Ingresa un número entero: "))
        binario = convertir_a_binario(numero)
        print(f"El número ingresado en binario es: {binario}")
    elif seleccion == "2":
        numeroDigitos = int(input("Ingrese su numero para contar los digitos: "))
        conteo = contar_digitos(numeroDigitos)
        print(f"El numero {numeroDigitos} tiene {conteo} digitos")
    elif seleccion == "3":
        number = int(input("Ingrese el numero para sacar raiz cuadrada: "))
        raiz = raiz_cuadrada_entera(number)
        print(f"El numero {number} su raiz entera es  {raiz} ")        
    elif seleccion == "4":
        numero_romano = input("Escriba su numero romano: ").upper()
        decimal =  convertir_a_decimal(numero_romano)
        print(f"El número romano {numero_romano} es equivalente a {decimal} en sistema decimal.")
    elif seleccion == "5":
        numero_entero = input("Escriba el numero a sumar: ")
        resultado = suma_numeros_enteros(numero_entero)
        print(f"La suma de los números enteros desde 0 hasta {numero_entero} es: {resultado}")
    elif seleccion == "6":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")
