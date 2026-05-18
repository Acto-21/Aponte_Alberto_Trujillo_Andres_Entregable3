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