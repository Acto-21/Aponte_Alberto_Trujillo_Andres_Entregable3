def leer_empleados(ruta):
    empleados = []
    try:
        with open(ruta, 'r', encoding='utf-8') as file:
            for linea in file:
                elementos = linea.strip().split(';')
                
                if len(elementos) != 3:
                    print(f"El empleado '{linea.strip()}' no tiene todos los datos, no fue agregado.")
                else:
                    nombre = elementos[0]
                    ocupacion = elementos[1].lower()
                    
                    try:
                        precio = int(elementos[2])
                    except ValueError:
                        print("Hubo un error al leer el precio, se tomará el precio del empleado como máximo")
                        precio = float('inf')
                    
                    empleado = { "nombre": nombre, "ocupacion": ocupacion, "precio": precio }

                    empleados.append(empleado)

    except FileNotFoundError:
        print("Error: El archivo no fue encontrado")
        # Si no encuentra el archivo, saldrá de la función devolviendo la lista vacía
        return empleados

    return empleados

def leer_clientes(ruta):
    clientes = []
    try:
        with open(ruta, 'r', encoding='utf-8') as file:
            for linea in file:
                elementos = linea.strip().split(';')
                
                if len(elementos) != 3:
                    print(f"El cliente '{linea.strip()}' no tiene todos los datos, no fue agregado.")
                else:
                    nombre = elementos[0]
                    ocupacionRequerida = elementos[1].lower()
                    
                    try:
                        presupuesto = int(elementos[2])
                    except ValueError:
                        print("Hubo un error al leer el presupuesto, se tomará el presupuesto del cliente como 0")
                        presupuesto = 0
                    
                    cliente = { "nombre": nombre, "ocupacion": ocupacionRequerida, "precio": presupuesto}

                    clientes.append(cliente)

    except FileNotFoundError:
        print("Error: El archivo no fue encontrado")
        # Si no encuentra el archivo, saldrá de la función devolviendo la lista vacía
        return clientes

    return clientes

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.adyacentes = {}

    def agregar_arista(self, destino, capacidad):
        self.adyacentes[destino] = capacidad

    def __str__(self):
        return f"Nodo({self.dato})"


class Grafo:
    def __init__(self):
        self.nodos = {}

    def agregar_nodo(self, dato):
        if dato not in self.nodos:
            self.nodos[dato] = Nodo(dato)

    def agregar_arista(self, origen, destino, capacidad):
        # Crear nodos si no existen
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        # Arista normal
        self.nodos[origen].agregar_arista(destino, capacidad)

        # Arista residual inversa
        if origen not in self.nodos[destino].adyacentes:
            self.nodos[destino].agregar_arista(origen, 0)


    def mostrar_grafo(self):
        for nombre, nodo in self.nodos.items():
            print(f"\n{nombre}:")
            for vecino, capacidad in nodo.adyacentes.items():
                print(f"  -> {vecino} | capacidad = {capacidad}")

    def bfs(self, fuente, sumidero, padres):
    
        #Retorna True si existe un camino desde fuente hasta sumidero.

        visitados = set()
        cola = []

        cola.append(fuente)
        visitados.add(fuente)

        while cola:
            actual = cola.pop(0)

            for vecino, capacidad in self.nodos[actual].adyacentes.items():

                # Solo visitar si tiene capacidad disponible
                if vecino not in visitados and capacidad > 0:

                    cola.append(vecino)
                    visitados.add(vecino)

                    # Guardar el padre para reconstruir el camino
                    padres[vecino] = actual

                    # Si llegamos al sumidero
                    if vecino == sumidero:
                        return True

        return False
    def ford_fulkerson(self, fuente, sumidero):
        flujo_total = 0
 
        while True:
            # Diccionario para guardar el camino encontrado por BFS
            padres = {}
            if not self.bfs(fuente, sumidero, padres):
                break
 
            flujo_camino = float('inf')
            nodo_actual = sumidero
 
            while nodo_actual != fuente:
                padre = padres[nodo_actual]
                capacidad = self.nodos[padre].adyacentes[nodo_actual]
                flujo_camino = min(flujo_camino, capacidad)
                nodo_actual = padre
 
            nodo_actual = sumidero
            while nodo_actual != fuente:
                padre = padres[nodo_actual]
                self.nodos[padre].adyacentes[nodo_actual] -= flujo_camino
                self.nodos[nodo_actual].adyacentes[padre] += flujo_camino
                nodo_actual = padre
 
            flujo_total += flujo_camino
        return flujo_total
 
    
def obtener_emparejamientos(grafo, lista_clientes):
    # Si las aristas que van de cliente a empleado tienen capacidad 0, significa que el flujo pasó por esa arista
    emparejamientos = []

    for cliente in lista_clientes:
        id_cliente = f"C:{cliente['nombre']}"

        for vecino, capacidad in grafo.nodos[id_cliente].adyacentes.items():
            if vecino.startswith("E:") and capacidad == 0:
                if grafo.nodos[vecino].adyacentes.get(id_cliente, 0) == 1:
                    nombre_empleado = vecino[2:]
                    nombre_cliente = cliente['nombre']
                    emparejamientos.append((nombre_cliente, nombre_empleado))

    return emparejamientos
    
def main():

    #Cargar los datos
    lista_empleados = leer_empleados("datos_de_entrada/empleados.txt")
    lista_clientes = leer_clientes("datos_de_entrada/clientes.txt")
    
    if not lista_empleados or not lista_clientes:
        print("No se puede proceder sin datos válidos en ambos archivos.")
        exit()
    

    # 2. Construir el Grafo Residual
    grafo = Grafo()
    FUENTE = "PROV_FUENTE"
    SUMIDERO = "PROV_SUMIDERO"
    # Para evitar colisiones si un cliente y empleado se llaman igual, usamos prefijos
    for cliente in lista_clientes:
        id_cliente = f"C:{cliente['nombre']}"
        grafo.agregar_arista(FUENTE, id_cliente, 1) # Fuente a Cliente
        
        for empleado in lista_empleados:
            id_empleado = f"E:{empleado['nombre']}"
            
            # Condición de emparejamiento: misma ocupación y presupuesto >= precio por hora
            if cliente['ocupacion'] == empleado['ocupacion'] and cliente['precio'] >= empleado['precio']:
                grafo.agregar_arista(id_cliente, id_empleado, 1) # Cliente a Empleado

    for empleado in lista_empleados:
        id_empleado = f"E:{empleado['nombre']}"
        grafo.agregar_arista(id_empleado, SUMIDERO, 1) # Empleado a Sumidero
    grafo.mostrar_grafo()

    # 3. Se ejecuta Ford-Fulkerson para encontrar el flujo máximo (numero total de emparejamientos máximos)
    print("\n--- Ford-Fulkerson ---")
    total = grafo.ford_fulkerson(FUENTE, SUMIDERO)
 
    # 4. Se sacan los emparejamientos del grafo residual y se muestran
    emparejamientos = obtener_emparejamientos(grafo, lista_clientes)
 
    print("\nEmparejamientos encontrados: ")
    for cliente, empleado in emparejamientos:
        print(f"{cliente} - {empleado}")
 
    print(f"\nTotal de emparejamientos: {total}")

main()
