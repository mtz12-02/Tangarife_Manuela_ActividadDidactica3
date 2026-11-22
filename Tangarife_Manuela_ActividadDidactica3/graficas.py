import matplotlib.pyplot as plt
import numpy as np


# Graficar el tiempo promedio de espera de cada escenario
def graficar_tiempos_espera(resumen_escenarios):

    nombres = []
    promedios = []
    errores_inferiores = []
    errores_superiores = []

    # Obtener los resultados de cada escenario
    for escenario in resumen_escenarios:

        nombres.append(
            escenario["Escenario"].replace(" - ", "\n")
        )

        espera = escenario["Espera_general"]

        promedio = espera["Promedio"]
        inferior = espera["IC_inferior"]
        superior = espera["IC_superior"]

        promedios.append(promedio)

        # Calcular los intervalos de confianza disponibles
        if np.isfinite(inferior) and np.isfinite(superior):
            errores_inferiores.append(max(0, promedio - inferior))
            errores_superiores.append(max(0, superior - promedio))
        else:
            errores_inferiores.append(0)
            errores_superiores.append(0)

    # Crear la gráfica
    plt.figure(figsize=(10, 6))

    barras = plt.bar(
        nombres,
        promedios,
        yerr=[errores_inferiores, errores_superiores],
        capsize=5
    )

    # Mostrar los valores sobre las barras
    for barra, promedio in zip(barras, promedios):

        plt.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height(),
            f"{promedio:.2f}",
            ha="center",
            va="bottom"
        )

    plt.title("Tiempo promedio de espera por escenario")
    plt.xlabel("Escenarios")
    plt.ylabel("Tiempo de espera (minutos)")
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()


# Graficar los tiempos de espera según la operación
def graficar_espera_por_operacion(resumen_escenarios):

    nombres = []
    esperas_retiro = []
    esperas_pago = []

    # Obtener los resultados de cada escenario
    for escenario in resumen_escenarios:

        nombres.append(
            escenario["Escenario"].replace(" - ", "\n")
        )

        esperas_retiro.append(
            escenario["Espera_retiro"]["Promedio"]
        )

        esperas_pago.append(
            escenario["Espera_pago"]["Promedio"]
        )

    # Crear la gráfica
    posiciones = np.arange(len(nombres))
    ancho = 0.35

    plt.figure(figsize=(11, 6))

    barras_retiro = plt.bar(
        posiciones - ancho / 2,
        esperas_retiro,
        ancho,
        label="Retiros"
    )

    barras_pago = plt.bar(
        posiciones + ancho / 2,
        esperas_pago,
        ancho,
        label="Pagos"
    )

    # Mostrar los valores sobre las barras
    for barras in [barras_retiro, barras_pago]:

        for barra in barras:

            altura = barra.get_height()

            if np.isfinite(altura):
                plt.text(
                    barra.get_x() + barra.get_width() / 2,
                    altura,
                    f"{altura:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

    plt.title("Tiempo promedio de espera por operación")
    plt.xlabel("Escenarios")
    plt.ylabel("Tiempo de espera (minutos)")
    plt.xticks(posiciones, nombres)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()


# Graficar el tiempo promedio de servicio por cajero
def graficar_tiempo_servicio(resumen_escenarios):

    nombres = []
    promedios = []

    # Recorrer los escenarios
    for escenario in resumen_escenarios:

        # Recorrer los cajeros de cada escenario
        for cajero in escenario["Servicios_cajeros"]:

            nombres.append(
                escenario["Escenario"].split(" - ")[0]
                + " - Cajero "
                + str(cajero["Cajero"])
            )

            promedios.append(
                cajero["Servicio"]["Promedio"]
            )

    # Crear la gráfica
    plt.figure(figsize=(12, 7))

    barras = plt.barh(nombres, promedios)

    # Mostrar los valores al final de las barras
    for barra, promedio in zip(barras, promedios):

        plt.text(
            promedio,
            barra.get_y() + barra.get_height() / 2,
            f" {promedio:.2f}",
            va="center"
        )

    plt.title("Tiempo promedio de servicio por cajero")
    plt.xlabel("Tiempo de servicio (minutos)")
    plt.ylabel("Cajeros")
    plt.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.show()
