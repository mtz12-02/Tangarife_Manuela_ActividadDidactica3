import simulacion
import estadisticas
import graficas


# Configurar los parámetros de la simulación
tiempo_simulacion = 480
semilla = 42
numero_replicas = 10


# Guardar los resultados de todas las réplicas
resultados_replicas = []


# Ejecutar las réplicas de la simulación
for replica in range(1, numero_replicas + 1):

    print("\n====================================")
    print("RÉPLICA:", replica)
    print("====================================")

    # Generar un nuevo grupo de clientes
    semilla_replica = semilla + replica

    clientes = simulacion.generar_clientes(
        tiempo_simulacion,
        semilla_replica
    )

    print("Total de clientes:", len(clientes))

    # Evaluar los cuatro escenarios
    for indice, (nombre, parametros) in enumerate(
        simulacion.escenarios.items()
    ):

        # Asignar los clientes a los cajeros
        clientes_asignados = simulacion.asignar_clientes(
            clientes,
            parametros,
            semilla_replica + indice + 100
        )

        # Simular la atención de los clientes
        resultados_atencion = simulacion.simular_atencion(
            clientes_asignados,
            parametros
        )

        # Calcular las estadísticas de las colas
        estadisticas_colas = simulacion.calcular_estadisticas_colas(
            resultados_atencion,
            parametros,
            tiempo_simulacion
        )

        # Calcular las estadísticas de cada cajero
        estadisticas_cajeros = simulacion.calcular_estadisticas(
            resultados_atencion,
            parametros,
            tiempo_simulacion
        )

        # Contar los usuarios por operación y categoría
        conteos = simulacion.contar_usuarios_por_tipo(
            resultados_atencion
        )

        # Guardar los resultados de esta simulación
        resultados_replicas.append({
            "Replica": replica,
            "Escenario": nombre,
            "Estadisticas": estadisticas_cajeros,
            "Estadisticas_colas": estadisticas_colas,
            "Conteos": conteos,
            "Resultados_atencion": resultados_atencion
        })


# Mostrar el resumen general de las simulaciones
print("\n====================================")
print("RESUMEN DE LAS SIMULACIONES")
print("====================================")

print("Duración de cada jornada:", tiempo_simulacion, "minutos")
print("Réplicas realizadas:", numero_replicas)
print("Escenarios evaluados:", len(simulacion.escenarios))
print("Total de simulaciones:", len(resultados_replicas))


# Analizar los resultados de los escenarios
resumen_escenarios = estadisticas.analizar_escenarios(
    resultados_replicas
)


# Mostrar el análisis de los tiempos de espera
print("\n====================================")
print("ANÁLISIS DE LOS TIEMPOS DE ESPERA")
print("====================================")

for escenario in resumen_escenarios:

    print("\n", escenario["Escenario"])

    print("\nTiempo de espera general:")
    print(escenario["Espera_general"])

    print("\nTiempo de espera para retiros:")
    print(escenario["Espera_retiro"])

    print("\nTiempo de espera para pagos:")
    print(escenario["Espera_pago"])


# Identificar los cajeros con menor y mayor tiempo de servicio
resultados_cajeros, menor, mayor = estadisticas.analizar_tiempos_servicio(
    resultados_replicas
)

print("\n====================================")
print("COMPARACIÓN DE LOS TIEMPOS DE SERVICIO")
print("====================================")

for cajero in resultados_cajeros:
    print(cajero)

print("\nCajero con menor tiempo promedio de servicio:")
print(menor)

print("\nCajero con mayor tiempo promedio de servicio:")
print(mayor)


# Analizar la cantidad de usuarios por categoría
conteos_replicas, resumen_categorias = estadisticas.analizar_conteos_usuarios(
    resultados_replicas
)

print("\n====================================")
print("CANTIDAD DE USUARIOS POR RÉPLICA")
print("====================================")

for resultado in conteos_replicas:
    print(resultado)

print("\n====================================")
print("PROMEDIO DE USUARIOS POR CATEGORÍA")
print("====================================")

for resultado in resumen_categorias:
    print(resultado)


# Analizar la utilización de los cajeros
resumen_utilizacion = estadisticas.analizar_utilizacion(
    resultados_replicas
)

print("\n====================================")
print("UTILIZACIÓN DE LOS CAJEROS")
print("====================================")

for resultado in resumen_utilizacion:

    print("\nEscenario:", resultado["Escenario"])
    print("Cajero:", resultado["Cajero"])
    print("Tipo:", resultado["Tipo"])
    print("Utilización:", resultado["Utilizacion"])


# Mostrar las estadísticas de las colas por réplica
print("\n====================================")
print("ESTADÍSTICAS DE LAS COLAS POR RÉPLICA")
print("====================================")

for resultado in resultados_replicas:

    print("\nRéplica:", resultado["Replica"])
    print("Escenario:", resultado["Escenario"])

    for cajero in resultado["Estadisticas_colas"]:
        print(cajero)


# Resumir las estadísticas de las colas
resumen_colas = estadisticas.analizar_colas(
    resultados_replicas
)

print("\n====================================")
print("RESUMEN DE LAS COLAS POR ESCENARIO")
print("====================================")

for resultado in resumen_colas:

    print("\nEscenario:", resultado["Escenario"])
    print("Cajero:", resultado["Cajero"])
    print("Promedio de clientes en cola:", resultado["Promedio_cola"])
    print("Máximo de clientes en cola:", resultado["Maximo_cola"])
    print("Clientes esperando al cierre:", resultado["Esperando_cierre"])


# Generar las gráficas de los resultados
print("\n====================================")
print("GENERACIÓN DE GRÁFICAS")
print("====================================")

# Graficar el tiempo promedio de espera
graficas.graficar_tiempos_espera(resumen_escenarios)

# Graficar la espera según el tipo de operación
graficas.graficar_espera_por_operacion(resumen_escenarios)

# Graficar el tiempo promedio de servicio por cajero
graficas.graficar_tiempo_servicio(resumen_escenarios)


# Mostrar el escenario con menor tiempo promedio de espera
mejor_escenario = min(
    resumen_escenarios,
    key=lambda escenario: escenario["Espera_general"]["Promedio"]
)

print("\n====================================")
print("COMPARACIÓN GENERAL DE LOS ESCENARIOS")
print("====================================")

for escenario in resumen_escenarios:

    print(
        escenario["Escenario"],
        "- Espera promedio:",
        round(escenario["Espera_general"]["Promedio"], 3),
        "minutos"
    )

print("\nEscenario con menor tiempo promedio de espera:")
print(mejor_escenario["Escenario"])

print(
    "Tiempo promedio:",
    round(mejor_escenario["Espera_general"]["Promedio"], 3),
    "minutos"
)
