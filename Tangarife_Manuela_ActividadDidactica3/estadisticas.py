import numpy as np
from scipy import stats


# Calcular el promedio, la desviación estándar y el intervalo de confianza
def calcular_resumen(valores):

    # Convertir los valores en una lista
    valores = np.asarray(valores, dtype=float)

    # Evitar errores cuando no hay datos
    if len(valores) == 0:
        return {
            "Promedio": np.nan,
            "Desviacion": np.nan,
            "IC_inferior": np.nan,
            "IC_superior": np.nan
        }

    promedio = np.mean(valores)

    # Calcular la desviación estándar
    if len(valores) > 1:
        desviacion = np.std(valores, ddof=1)

        # Calcular el intervalo de confianza del 95 %
        margen_error = stats.t.ppf(
            0.975,
            len(valores) - 1
        ) * desviacion / np.sqrt(len(valores))

        limite_inferior = promedio - margen_error
        limite_superior = promedio + margen_error

    else:
        desviacion = 0
        limite_inferior = np.nan
        limite_superior = np.nan

    return {
        "Promedio": promedio,
        "Desviacion": desviacion,
        "IC_inferior": limite_inferior,
        "IC_superior": limite_superior
    }


# Calcular el promedio evitando errores cuando no hay datos
def calcular_promedio(valores):

    if len(valores) > 0:
        return np.mean(valores)

    return np.nan


# Analizar los resultados de cada escenario
def analizar_escenarios(resultados_replicas):

    resumen_escenarios = []

    # Obtener los nombres de los escenarios
    escenarios = list(dict.fromkeys(
        resultado["Escenario"]
        for resultado in resultados_replicas
    ))

    # Recorrer cada escenario
    for escenario in escenarios:

        # Obtener las réplicas del escenario
        replicas = [
            resultado for resultado in resultados_replicas
            if resultado["Escenario"] == escenario
        ]

        esperas_generales = []
        esperas_retiro = []
        esperas_pago = []

        # Guardar el tiempo promedio de servicio de cada cajero
        servicios_cajeros = {}

        # Recorrer las réplicas
        for replica in replicas:

            resultados_atencion = replica["Resultados_atencion"]

            # Calcular la espera promedio de todos los clientes
            esperas_generales.append(calcular_promedio([
                cliente["Tiempo_espera"]
                for cliente in resultados_atencion
            ]))

            # Separar las esperas según la operación
            clientes_retiro = [
                cliente for cliente in resultados_atencion
                if cliente["Operacion"] == "Retiro"
            ]

            clientes_pago = [
                cliente for cliente in resultados_atencion
                if cliente["Operacion"] == "Pago"
            ]

            esperas_retiro.append(calcular_promedio([
                cliente["Tiempo_espera"]
                for cliente in clientes_retiro
            ]))

            esperas_pago.append(calcular_promedio([
                cliente["Tiempo_espera"]
                for cliente in clientes_pago
            ]))

            # Obtener el promedio de servicio de cada cajero
            for cajero in replica["Estadisticas"]:

                numero = cajero["Cajero"]

                if numero not in servicios_cajeros:
                    servicios_cajeros[numero] = []

                servicios_cajeros[numero].append(
                    cajero["Promedio_servicio"]
                )

        # Calcular el resumen de los tiempos de servicio por cajero
        resumen_servicios = []

        for numero, valores in servicios_cajeros.items():

            resumen_servicios.append({
                "Cajero": numero,
                "Servicio": calcular_resumen(valores)
            })

        # Guardar los resultados del escenario
        resumen_escenarios.append({
            "Escenario": escenario,
            "Espera_general": calcular_resumen(esperas_generales),
            "Espera_retiro": calcular_resumen(esperas_retiro),
            "Espera_pago": calcular_resumen(esperas_pago),
            "Servicios_cajeros": resumen_servicios
        })

    return resumen_escenarios


# Identificar los cajeros con menor y mayor tiempo promedio de servicio
def analizar_tiempos_servicio(resultados_replicas):

    resultados_cajeros = []

    # Obtener los escenarios
    escenarios = list(dict.fromkeys(
        resultado["Escenario"]
        for resultado in resultados_replicas
    ))

    # Recorrer cada escenario
    for escenario in escenarios:

        # Obtener los resultados de ese escenario
        replicas = [
            resultado for resultado in resultados_replicas
            if resultado["Escenario"] == escenario
        ]

        # Obtener la cantidad de cajeros
        cantidad_cajeros = len(replicas[0]["Estadisticas"])

        # Recorrer cada cajero
        for numero in range(1, cantidad_cajeros + 1):

            tiempos_servicio = []

            # Recopilar los tiempos de servicio de las réplicas
            for replica in replicas:

                for cliente in replica["Resultados_atencion"]:

                    if cliente["Cajero"] == numero:
                        tiempos_servicio.append(
                            cliente["Tiempo_servicio"]
                        )

            # Calcular el promedio si el cajero atendió clientes
            if len(tiempos_servicio) > 0:

                resultados_cajeros.append({
                    "Escenario": escenario,
                    "Cajero": numero,
                    "Cantidad_clientes": len(tiempos_servicio),
                    "Promedio_servicio": np.mean(tiempos_servicio)
                })

    # Identificar el menor y el mayor promedio
    if len(resultados_cajeros) == 0:
        return resultados_cajeros, None, None

    menor = min(
        resultados_cajeros,
        key=lambda resultado: resultado["Promedio_servicio"]
    )

    mayor = max(
        resultados_cajeros,
        key=lambda resultado: resultado["Promedio_servicio"]
    )

    return resultados_cajeros, menor, mayor


# Analizar la cantidad de usuarios por categoría en cada réplica
def analizar_conteos_usuarios(resultados_replicas):

    resultados_por_replica = []
    cantidades_por_categoria = {}

    # Evitar contar varias veces la misma réplica
    replicas_procesadas = []

    for resultado in resultados_replicas:

        replica = resultado["Replica"]

        if replica not in replicas_procesadas:

            replicas_procesadas.append(replica)

            # Obtener los conteos de usuarios de la réplica
            for conteo in resultado["Conteos"]:

                resultados_por_replica.append({
                    "Replica": replica,
                    "Operacion": conteo["Operacion"],
                    "Categoria": conteo["Categoria"],
                    "Cantidad": conteo["Cantidad"]
                })

                # Agrupar las cantidades por operación y categoría
                clave = (
                    conteo["Operacion"],
                    conteo["Categoria"]
                )

                if clave not in cantidades_por_categoria:
                    cantidades_por_categoria[clave] = []

                cantidades_por_categoria[clave].append(
                    conteo["Cantidad"]
                )

    # Calcular el promedio de usuarios por categoría
    resumen_categorias = []

    for clave, cantidades in cantidades_por_categoria.items():

        resumen = calcular_resumen(cantidades)

        resumen_categorias.append({
            "Operacion": clave[0],
            "Categoria": clave[1],
            "Promedio": resumen["Promedio"],
            "Desviacion": resumen["Desviacion"],
            "IC_inferior": resumen["IC_inferior"],
            "IC_superior": resumen["IC_superior"]
        })

    return resultados_por_replica, resumen_categorias


# Analizar la utilización de cada cajero en los escenarios
def analizar_utilizacion(resultados_replicas):

    resumen_utilizacion = []

    # Obtener los nombres de los escenarios
    escenarios = list(dict.fromkeys(
        resultado["Escenario"]
        for resultado in resultados_replicas
    ))

    # Recorrer cada escenario
    for escenario in escenarios:

        # Obtener las réplicas del escenario
        replicas = [
            resultado for resultado in resultados_replicas
            if resultado["Escenario"] == escenario
        ]

        # Obtener la cantidad de cajeros
        cantidad_cajeros = len(replicas[0]["Estadisticas"])

        # Recorrer cada cajero
        for numero in range(1, cantidad_cajeros + 1):

            utilizaciones = []
            tipo_cajero = ""

            # Recopilar la utilización de las réplicas
            for replica in replicas:

                for cajero in replica["Estadisticas"]:

                    if cajero["Cajero"] == numero:

                        utilizaciones.append(
                            cajero["Utilizacion"]
                        )

                        tipo_cajero = cajero["Tipo"]

            # Calcular el resumen estadístico
            resumen = calcular_resumen(utilizaciones)

            # Guardar los resultados
            resumen_utilizacion.append({
                "Escenario": escenario,
                "Cajero": numero,
                "Tipo": tipo_cajero,
                "Utilizacion": resumen
            })

    return resumen_utilizacion


# Analizar las estadísticas de las colas
def analizar_colas(resultados_replicas):

    resumen_colas = []

    # Obtener los escenarios
    escenarios = list(dict.fromkeys(
        resultado["Escenario"]
        for resultado in resultados_replicas
    ))

    # Recorrer cada escenario
    for escenario in escenarios:

        # Obtener las réplicas del escenario
        replicas = [
            resultado for resultado in resultados_replicas
            if resultado["Escenario"] == escenario
        ]

        # Obtener la cantidad de cajeros
        cantidad_cajeros = len(replicas[0]["Estadisticas"])

        # Recorrer cada cajero
        for numero in range(1, cantidad_cajeros + 1):

            colas_promedio = []
            colas_maximas = []
            esperando_cierre = []

            # Recorrer las réplicas
            for replica in replicas:

                # Obtener las estadísticas de las colas
                for cajero in replica["Estadisticas_colas"]:

                    if cajero["Cajero"] == numero:

                        colas_promedio.append(
                            cajero["Cola_promedio"]
                        )

                        colas_maximas.append(
                            cajero["Cola_maxima"]
                        )

                        esperando_cierre.append(
                            cajero["Clientes_esperando_cierre"]
                        )

            # Guardar el resumen del cajero
            resumen_colas.append({
                "Escenario": escenario,
                "Cajero": numero,
                "Promedio_cola": calcular_resumen(colas_promedio),
                "Maximo_cola": calcular_resumen(colas_maximas),
                "Esperando_cierre": calcular_resumen(esperando_cierre)
            })

    return resumen_colas
