# Bitcoin Data Challenge – CoinGecko API + PySpark

Este proyecto resuelve un reto técnico que consiste en obtener información histórica del precio de Bitcoin utilizando la API de CoinGecko, almacenar los datos en una base de datos y calcular un promedio móvil de 5 días utilizando PySpark o Pandas.



## 🧱 Estructura del Proyecto

BITCOIN_MOV/ 
  ├── .vscode/ # Configuración del entorno de VSCode
  ├── img_pruebas_unitarias/ # Carpeta de pruebas 
  ├── venv/ # Entorno virtual de Python
  ├── iceberg-spark-runtime-*.jar # (opcional) Soporte para Apache Iceberg
  ├── mysql-connector-j-8.0.33.jar # Driver JDBC para MySQL
  ├── main.py # Script principal que contiene toda la lógica
  ├── README.md # Este archivo de documentación 


## Recuperar la informacion de la API CoinGecko

Se utilizó el endpoint público de CoinGecko para obtener el listado completo de criptomonedas:

https://api.coingecko.com/api/v3/coins/list
https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range


## Data Engineer Challenge – Promedio Móvil del Precio de Bitcoin

Este proyecto resuelve el siguiente reto:
 * calcular el promedio móvil de 5 días
 * Precio de Bitcoin durante el primer trimestre de 2025, utilizando la API de CoinGecko, PySpark y MySQL como base de datos.


## 🚀 Cómo Ejecutar

Se preparo el ambiente en VScode con la estructura mencionada anteriormente, desde la terminal de VSCode se ejecuta el script main.py

ejemplo :  python main.py

### Requisitos

- Python 3.8+
- Java 11 ()
- PySpark
- MySQL local (puerto 3306)
- Archivo JDBC de MySQL: `mysql-connector-j-8.0.33.jar`
- API pública de CoinGecko

Nota : Se decidio trabajar con el primer trimestre del año 2025, ya que la API solo te permite leer un año con cuenta gratuita.

## "error_message": "Your request exceeds the allowed time range. Public API users are limited to querying historical data within the past 365 days."

### Crear entorno virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


##########################################################################################################################################################

#########################################################################
-- Plan de escalabilidad
#########################################################################

-- Yo utilizaria apache kafka como un sistema de mensajería en tiempo real para consumir los precios de las criptomonedas de múltiples fuentes como la API de CoinGecko. He tenido la oportunidad de trabajar con Kafka, y me ha permitido manejar flujos de datos en tiempo real de manera eficiente.

-- Mi propuesta seria que cada vez que un nuevo precio de criptomoneda esté disponible , este se publicaría en un topico de Kafka. Los consumidores de este topico leerían los datos en tiempo real y realizarían las transformaciones necesarias en spark.



#########################################################################
-- Análisis de datos - promedio movil
#########################################################################

-- En mi expericiencia puedo decir, que el promedio móvil de 5 días muestra cómo ha estado cambiando el precio de Bitcoin en los últimos días. Si el promedio sube, significa que el precio está subiendo. Si baja, significa que está bajando. Este análisis también nos ayuda a ver la volatilidad, porque cuando el mercado es muy inestable, el promedio puede subir y bajar rápido.

