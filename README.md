# Simulación de un sistema bancario mediante modelos de colas

## Manuela Tangarife Zapata

## Descripción

En este proyecto desarrollé una simulación de un sistema bancario mediante modelos de colas, utilizando Python. La actividad se realizó de manera individual y tiene como propósito analizar el funcionamiento de tres cajeros que atienden operaciones de retiro y pago.

A partir de las condiciones planteadas en el problema, representé la llegada de los usuarios, sus diferentes tipos de operación y los tiempos de atención. También comparé distintas configuraciones de los cajeros para identificar cuál ofrece mejores condiciones de servicio y evaluar si es conveniente incorporar un cajero adicional.

## Objetivos

- Representar el funcionamiento de un sistema bancario mediante modelos de colas.
- Simular la llegada y atención de usuarios que realizan retiros y pagos.
- Comparar diferentes configuraciones de cajeros.
- Analizar los tiempos de espera, los tiempos de servicio y la utilización de los cajeros.
- Evaluar la necesidad de incorporar un cajero adicional a partir de los resultados obtenidos.

## Metodología

Para desarrollar la simulación, tomé como referencia una jornada bancaria de 8 horas, equivalente a 480 minutos.

Definí que el 70 % de los usuarios realiza retiros y el 30 % realiza pagos. Además, tuve en cuenta cuatro categorías de usuarios para cada operación: rápido, normal, lento y muy lento, utilizando las probabilidades y los tiempos establecidos en el enunciado de la actividad.

Representé cada cajero mediante un modelo M/M/1, con una cola independiente para cada uno. Los tiempos entre llegadas y los tiempos de servicio se generaron mediante distribuciones exponenciales, de acuerdo con los parámetros definidos para cada categoría.

Finalmente, realicé 10 réplicas por cada escenario, para un total de 40 simulaciones, con el propósito de comparar los resultados y analizar el comportamiento del sistema.

## Desarrollo del proyecto

### Modelo de simulación

Implementé un modelo que representa la llegada de los usuarios, la asignación de los cajeros y el proceso de atención. Cada usuario se clasifica según el tipo de operación que realiza y su respectiva categoría.

Para la asignación, tuve en cuenta la configuración de cada escenario, de manera que los usuarios fueran atendidos por los cajeros habilitados para su tipo de operación.

### Comparación de escenarios

Evalué cuatro configuraciones para analizar cómo cambia el comportamiento del sistema según la distribución de los cajeros:

- Escenario 1: tres cajeros mixtos, que atienden retiros y pagos.
- Escenario 2: un cajero exclusivo para retiros y dos exclusivos para pagos.
- Escenario 3: dos cajeros exclusivos para retiros y uno exclusivo para pagos.
- Escenario 4: dos cajeros exclusivos para retiros y dos exclusivos para pagos.

### Análisis estadístico

Para comparar los escenarios, calculé diferentes indicadores que permiten analizar el funcionamiento del sistema:

- Tiempos promedio de espera.
- Tiempos promedio de servicio por cajero.
- Cantidad de usuarios por tipo de operación y categoría.
- Porcentaje de utilización de los cajeros.
- Comportamiento de las colas y cantidad de usuarios que permanecen esperando al finalizar la jornada.

También calculé promedios, desviaciones estándar e intervalos de confianza del 95 % para analizar los resultados de las réplicas.

### Herramientas utilizadas

- Python.
- NumPy.
- Pandas.
- SciPy.
- Matplotlib.

### Resultados

A partir de las simulaciones, comparé el comportamiento de las cuatro configuraciones de cajeros. Los resultados mostraron diferencias en los tiempos de espera, la utilización y el comportamiento de las colas.

El escenario de dos cajeros exclusivos para retiros y dos para pagos presentó el menor tiempo promedio de espera general, con aproximadamente 1,73 minutos. Por su parte, el escenario de tres cajeros mixtos presentó un promedio de 3,41 minutos.

Estos resultados me permitieron identificar que la incorporación de un cuarto cajero, distribuido entre las dos operaciones, representa una alternativa favorable para mejorar las condiciones de atención y reducir los tiempos de espera.

Las gráficas y los resultados estadísticos se generan al ejecutar el programa principal.

## Estructura del proyecto

- `main.py`: ejecuta las simulaciones, organiza los resultados y presenta los análisis estadísticos.
- `simulacion.py`: contiene los parámetros, genera los usuarios, asigna los cajeros y simula los procesos de atención y las colas.
- `estadisticas.py`: calcula los indicadores estadísticos y realiza la comparación de los escenarios.
- `graficas.py`: contiene las funciones para generar las gráficas de los resultados.
- `requirements.txt`: contiene las bibliotecas necesarias para ejecutar el proyecto.

## Instalación y ejecución

Para ejecutar el proyecto, es necesario tener Python instalado y seguir estos pasos desde la carpeta principal del repositorio.

#### 1. Crear un entorno virtual

```bash
python -m venv venv
```

#### 2. Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

#### 3. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

#### 4. Ejecutar las simulaciones

```bash
python main.py
```

Este archivo ejecuta las 40 simulaciones, presenta los resultados estadísticos y genera las gráficas correspondientes.
