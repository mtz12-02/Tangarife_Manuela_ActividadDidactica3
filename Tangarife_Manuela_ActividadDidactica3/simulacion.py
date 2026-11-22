import numpy as np


# Configurar las probabilidades de cada operación
probabilidad_retiro = 0.70
probabilidad_pago = 0.30


# Definir las categorías y sus parámetros para cada operación
parametros_usuarios = {
    "Retiro": {
        "categorias": ["Rápido", "Normal", "Lento", "Muy lento"],
        "probabilidades": [0.23, 0.40, 0.17, 0.20],
        "tiempos_servicio": [1, 2, 3, 4],
        "tiempos_llegada": [1, 2, 3, 3]
    },

    "Pago": {
        "categorias": ["Rápido", "Normal", "Lento", "Muy lento"],
        "probabilidades": [0.10, 0.20, 0.30, 0.40],
        "tiempos_servicio": [3, 3, 5, 7],
        "tiempos_llegada": [1, 2, 3, 4]
    }
}


# Definir los escenarios de distribución de los cajeros
escenarios = {
    "Escenario 1 - Tres cajeros mixtos": {
        "cajeros": ["Mixto", "Mixto", "Mixto"]
    },

    "Escenario 2 - Un cajero de retiros y dos de pagos": {
        "cajeros": ["Retiro", "Pago", "Pago"]
    },

    "Escenario 3 - Dos cajeros de retiros y uno de pagos": {
        "cajeros": ["Retiro", "Retiro", "Pago"]
    },

    "Escenario 4 - Dos cajeros de retiros y dos de pagos": {
        "cajeros": ["Retiro", "Retiro", "Pago", "Pago"]
    }
}


# Generar los clientes que llegan durante la jornada
def generar_clientes(tiempo_simulacion, semilla):

    # Configurar la semilla para reproducir los resultados
    generador = np.random.default_rng(semilla)

    # Guardar los clientes generados
    clientes = []

    # Inicializar el tiempo de llegada y el identificador
    tiempo_llegada = 0
    id_cliente = 1

    # Generar clientes hasta completar el tiempo de simulación
    while True:

        # Seleccionar el tipo de operación
        operacion = str(generador.choice(
            ["Retiro", "Pago"],
            p=[probabilidad_retiro, probabilidad_pago]
        ))

        # Obtener los parámetros de la operación seleccionada
        parametros = parametros_usuarios[operacion]

        # Seleccionar la categoría del usuario
        categoria = str(generador.choice(
            parametros["categorias"],
            p=parametros["probabilidades"]
        ))

        # Buscar los tiempos medios correspondientes a la categoría
        indice = parametros["categorias"].index(categoria)

        media_servicio = parametros["tiempos_servicio"][indice]
        media_llegada = parametros["tiempos_llegada"][indice]

        # Generar el tiempo entre llegadas
        tiempo_entre_llegadas = generador.exponential(media_llegada)

        # Calcular el momento de llegada del cliente
        tiempo_llegada += tiempo_entre_llegadas

        # Detener la generación cuando termine la jornada
        if tiempo_llegada > tiempo_simulacion:
            break

        # Generar el tiempo de servicio del cliente
        tiempo_servicio = generador.exponential(media_servicio)

        # Guardar la información del cliente
        clientes.append({
            "ID": id_cliente,
            "Operacion": operacion,
            "Categoria": categoria,
            "Llegada": tiempo_llegada,
            "Tiempo_servicio": tiempo_servicio
        })

        # Actualizar el identificador del cliente
        id_cliente += 1

    return clientes


# Asignar un cliente a uno de los cajeros disponibles
def asignar_cajero(cliente, cajeros, generador):

    # Buscar los cajeros que pueden atender la operación del cliente
    cajeros_disponibles = []

    for indice, tipo_cajero in enumerate(cajeros):

        # Permitir ambos tipos de operación en los cajeros mixtos
        if tipo_cajero == "Mixto" or tipo_cajero == cliente["Operacion"]:
            cajeros_disponibles.append(indice + 1)

    # Seleccionar aleatoriamente uno de los cajeros disponibles
    cajero_asignado = int(generador.choice(cajeros_disponibles))

    return cajero_asignado


# Asignar todos los clientes de acuerdo con el escenario
def asignar_clientes(clientes, parametros_escenario, semilla):

    # Configurar la semilla para reproducir la asignación
    generador = np.random.default_rng(semilla)

    # Guardar los clientes con su cajero asignado
    clientes_asignados = []

    # Recorrer los clientes generados
    for cliente in clientes:

        # Crear una copia para conservar los datos originales
        nuevo_cliente = cliente.copy()

        # Asignar un cajero según la operación del cliente
        nuevo_cliente["Cajero"] = asignar_cajero(
            nuevo_cliente,
            parametros_escenario["cajeros"],
            generador
        )

        # Guardar el cliente asignado
        clientes_asignados.append(nuevo_cliente)

    return clientes_asignados


# Simular la atención de los clientes en cada cajero
def simular_atencion(clientes_asignados, parametros_escenario):

    # Crear una lista para guardar los resultados
    resultados = []

    # Registrar la disponibilidad inicial de cada cajero
    disponibilidad = [0] * len(parametros_escenario["cajeros"])

    # Recorrer los clientes en orden de llegada
    for cliente in clientes_asignados:

        # Obtener el cajero asignado al cliente
        cajero = cliente["Cajero"]

        # Identificar la disponibilidad del cajero
        disponibilidad_cajero = disponibilidad[cajero - 1]

        # Calcular el inicio de la atención
        inicio_servicio = max(
            cliente["Llegada"],
            disponibilidad_cajero
        )

        # Calcular el tiempo de espera
        tiempo_espera = inicio_servicio - cliente["Llegada"]

        # Calcular el final de la atención
        fin_servicio = inicio_servicio + cliente["Tiempo_servicio"]

        # Actualizar la disponibilidad del cajero
        disponibilidad[cajero - 1] = fin_servicio

        # Copiar los datos del cliente
        nuevo_cliente = cliente.copy()

        # Guardar los tiempos de atención
        nuevo_cliente["Inicio_servicio"] = inicio_servicio
        nuevo_cliente["Fin_servicio"] = fin_servicio
        nuevo_cliente["Tiempo_espera"] = tiempo_espera
        nuevo_cliente["Tiempo_sistema"] = (
            tiempo_espera + cliente["Tiempo_servicio"]
        )

        resultados.append(nuevo_cliente)

    return resultados


# Calcular las estadísticas de cada cajero
def calcular_estadisticas(resultados, parametros_escenario, tiempo_simulacion=480):

    # Guardar las estadísticas de cada cajero
    estadisticas = []

    # Recorrer todos los cajeros del escenario
    for numero in range(1, len(parametros_escenario["cajeros"]) + 1):

        # Obtener los clientes asignados a este cajero
        clientes_cajero = [
            cliente for cliente in resultados
            if cliente["Cajero"] == numero
        ]

        # Calcular la cantidad de clientes atendidos
        cantidad_clientes = len(clientes_cajero)

        # Evitar cálculos cuando un cajero no recibe clientes
        if cantidad_clientes > 0:

            # Calcular los tiempos promedio
            promedio_servicio = np.mean([
                cliente["Tiempo_servicio"]
                for cliente in clientes_cajero
            ])

            promedio_espera = np.mean([
                cliente["Tiempo_espera"]
                for cliente in clientes_cajero
            ])

            promedio_sistema = np.mean([
                cliente["Tiempo_sistema"]
                for cliente in clientes_cajero
            ])

            # Calcular el tiempo ocupado dentro de la jornada
            tiempo_ocupado = sum(
                max(
                    0,
                    min(cliente["Fin_servicio"], tiempo_simulacion)
                    - cliente["Inicio_servicio"]
                )
                for cliente in clientes_cajero
            )

        else:
            promedio_servicio = 0
            promedio_espera = 0
            promedio_sistema = 0
            tiempo_ocupado = 0

        # Calcular el porcentaje de utilización
        utilizacion = (tiempo_ocupado / tiempo_simulacion) * 100

        # Guardar los resultados del cajero
        estadisticas.append({
            "Cajero": numero,
            "Tipo": parametros_escenario["cajeros"][numero - 1],
            "Clientes_atendidos": cantidad_clientes,
            "Promedio_servicio": promedio_servicio,
            "Promedio_espera": promedio_espera,
            "Promedio_sistema": promedio_sistema,
            "Utilizacion": utilizacion
        })

    return estadisticas


# Calcular las estadísticas de las colas de cada cajero
def calcular_estadisticas_colas(resultados, parametros_escenario, tiempo_simulacion):

    # Guardar las estadísticas de las colas
    estadisticas_colas = []

    # Recorrer todos los cajeros
    for numero in range(1, len(parametros_escenario["cajeros"]) + 1):

        # Obtener los clientes asignados al cajero
        clientes_cajero = [
            cliente for cliente in resultados
            if cliente["Cajero"] == numero
        ]

        # Guardar los eventos de llegada y comienzo de atención
        eventos = []

        # Contar los clientes que siguen esperando al cierre
        clientes_esperando = 0

        # Guardar el tiempo total que los clientes permanecen en cola
        area_cola = 0

        # Recorrer los clientes asignados al cajero
        for cliente in clientes_cajero:

            llegada = cliente["Llegada"]
            inicio = cliente["Inicio_servicio"]

            # Registrar las llegadas durante la jornada
            if llegada <= tiempo_simulacion:
                eventos.append((llegada, 1))

                # Calcular el tiempo de espera dentro de la jornada
                area_cola += max(
                    0,
                    min(inicio, tiempo_simulacion) - llegada
                )

            # Registrar cuando el cliente comienza su atención
            if inicio <= tiempo_simulacion:
                eventos.append((inicio, -1))

            # Verificar si el cliente seguía esperando al cierre
            if llegada <= tiempo_simulacion and inicio > tiempo_simulacion:
                clientes_esperando += 1

        # Ordenar los eventos por tiempo
        eventos.sort(key=lambda evento: evento[0])

        # Calcular la cantidad máxima de clientes en cola
        cantidad_en_cola = 0
        cola_maxima = 0

        indice = 0

        while indice < len(eventos):

            tiempo_actual = eventos[indice][0]

            # Agrupar los eventos que ocurren en el mismo instante
            cambios = 0

            while (
                indice < len(eventos)
                and eventos[indice][0] == tiempo_actual
            ):
                cambios += eventos[indice][1]
                indice += 1

            # Actualizar la cantidad de clientes en cola
            cantidad_en_cola += cambios

            # Registrar la cola máxima
            cola_maxima = max(cola_maxima, cantidad_en_cola)

        # Calcular la cantidad promedio de clientes en cola
        cola_promedio = area_cola / tiempo_simulacion

        # Guardar las estadísticas de la cola
        estadisticas_colas.append({
            "Cajero": numero,
            "Tipo": parametros_escenario["cajeros"][numero - 1],
            "Cola_promedio": cola_promedio,
            "Cola_maxima": cola_maxima,
            "Clientes_esperando_cierre": clientes_esperando
        })

    return estadisticas_colas


# Contar los usuarios de cada operación y categoría
def contar_usuarios_por_tipo(resultados):

    # Guardar las cantidades encontradas
    conteos = []

    # Recorrer cada operación
    for operacion in ["Retiro", "Pago"]:

        # Recorrer las categorías de usuarios
        for categoria in ["Rápido", "Normal", "Lento", "Muy lento"]:

            # Contar los usuarios que cumplen ambas condiciones
            cantidad = sum(
                cliente["Operacion"] == operacion and
                cliente["Categoria"] == categoria
                for cliente in resultados
            )

            # Guardar el resultado
            conteos.append({
                "Operacion": operacion,
                "Categoria": categoria,
                "Cantidad": cantidad
            })

    return conteos
