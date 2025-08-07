import os
import graphviz

# Prioridad de los operadores
precedencia = {
    '*': 3,
    '?': 3,
    '+': 3,
    '.': 2,
    '|': 1
}

# Agrega concatenación explícita
def agregar_concatenacion(expresion):
    resultado = ""
    simbolos_binarios = set(['|', ')'])
    simbolos_unarios = set(['*', '+', '?'])
    for i in range(len(expresion)):
        c1 = expresion[i]
        resultado += c1
        if i + 1 < len(expresion):
            c2 = expresion[i + 1]
            if (c1 not in "(|" and c2 not in ")*+?|)"):
                resultado += "."
            elif (c1 in ['*', '+', '?'] and c2 not in "|)*+?"):
                resultado += "."
            elif (c1 == ')' and c2 not in "|)*+?)"):
                resultado += "."
    return resultado

# Convierte infija a postfija
def infija_a_postfija(expresion):
    salida = ""
    pila = []
    for caracter in expresion:
        if caracter.isalnum() or caracter == 'ε':
            salida += caracter
        elif caracter == '(':
            pila.append(caracter)
        elif caracter == ')':
            while pila and pila[-1] != '(':
                salida += pila.pop()
            pila.pop()
        else:
            while (pila and pila[-1] != '(' and
                   precedencia.get(caracter, 0) <= precedencia.get(pila[-1], 0)):
                salida += pila.pop()
            pila.append(caracter)
    while pila:
        salida += pila.pop()
    return salida

# Nodo para el árbol
class Nodo:
    def __init__(self, valor, izquierda=None, derecha=None):
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

# Construcción del árbol sintáctico desde postfija
def construir_arbol(postfija):
    pila = []
    for c in postfija:
        if c.isalnum() or c == 'ε':
            pila.append(Nodo(c))
        elif c in ['*', '+', '?']:
            if not pila:
                raise ValueError(f"Error: '{c}' necesita 1 operando")
            nodo = Nodo(c, izquierda=pila.pop())
            pila.append(nodo)
        elif c in ['|', '.']:
            if len(pila) < 2:
                raise ValueError(f"Error: '{c}' necesita 2 operandos")
            derecha = pila.pop()
            izquierda = pila.pop()
            pila.append(Nodo(c, izquierda, derecha))
    if len(pila) != 1:
        raise ValueError("Error: expresión inválida")
    return pila[0]

# Genera el árbol con Graphviz
def graficar_arbol(nodo, nombre_archivo):
    dot = graphviz.Digraph()
    def recorrer(n, id_nodo=0):
        actual_id = str(id(n))
        dot.node(actual_id, n.valor)
        if n.izquierda:
            izq_id = str(id(n.izquierda))
            dot.edge(actual_id, izq_id)
            recorrer(n.izquierda)
        if n.derecha:
            der_id = str(id(n.derecha))
            dot.edge(actual_id, der_id)
            recorrer(n.derecha)
    recorrer(nodo)
    dot.render(nombre_archivo, format='png', cleanup=True)

# Procesamiento de cada línea
def procesar_expresiones(path_archivo):
    with open(path_archivo, 'r', encoding='utf-8') as archivo:
        lineas = archivo.readlines()
        for i, linea in enumerate(lineas, 1):
            expresion = linea.strip()
            if not expresion:
                continue
            print(f"=== Línea {i}: {expresion} ===")
            try:
                con_concat = agregar_concatenacion(expresion)
                postfija = infija_a_postfija(con_concat)
                print(f"(a) Postfija: {postfija}")
                arbol = construir_arbol(postfija)
                nombre_archivo = f"tree_line_{i}"
                graficar_arbol(arbol, nombre_archivo)
                print(f"(b) Árbol sintáctico guardado en '{nombre_archivo}.png'")
            except Exception as e:
                print(f"Error línea {i}: {e}")

# Ejecutar
if __name__ == "__main__":
    procesar_expresiones("Lab3.txt")
