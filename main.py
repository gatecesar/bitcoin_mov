from pyspark.sql.functions import col,from_unixtime,to_date,avg
from pyspark.sql import SparkSession,Row
from datetime import datetime, timedelta
from pyspark.sql.window import Window
import os,json,requests,sys

def main():

    # Configurar entorno
    os.environ["JAVA_HOME"] = "C:\\Program Files\\Eclipse Adoptium\\jdk-11.0.27.6-hotspot"
    os.environ["HADOOP_HOME"] = "C:\\hadoop"
    os.environ["PYSPARK_PYTHON"] = os.environ.get("PYSPARK_PYTHON", "python")

    # Crear SparkSession
    spark = (
        SparkSession.builder
        .appName("SparkToMySQL")
        .config("spark.jars", "file:///C:/Users/cesar/Documents/bitcoin_mov/mysql-connector-j-8.0.33.jar")
        .config("spark.driver.extraClassPath", "file:///C:/Users/cesar/Documents/bitcoin_mov/mysql-connector-j-8.0.33.jar")
        .config("spark.sql.legacy.timeParserPolicy", "LEGACY")
        .config("spark.cleaner.referenceTracking.cleanCheckpoints", "false")
        .getOrCreate()
    )

    ############################################
    # Parametros MySQL
    ############################################

    # Definir propiedades de conexión a MySQL
    mysql_url = "jdbc:mysql://localhost:3306/bitcoin_db"
    mysql_properties = {
        "user": "root",
        "password": "123456", 
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    ############################################################################################################################################################################
    # Recupera una lista de todas las criptomonedas con su id, nombre y símbolo
    ############################################################################################################################################################################

    # Obtener la lista desde la API
    df = requests.get("https://api.coingecko.com/api/v3/coins/list").json()

    # Convertir directamente a PySpark DataFrame
    df = spark.createDataFrame(df)

    # Mostrar primeros registros
    print("\n lista de criptomonedas - id,nombre simbolo")
    df.show(10,truncate=False)

    # Escribir el DataFrame a MySQL
    df.write.jdbc(
        url=mysql_url,
        table="list_criptomonedas",
        mode="overwrite",
        properties=mysql_properties
    )

    # Filtrar el id de bitcoin
    print("id de la criptomoneda Bitcoin")
    df.filter(col("name") == 'Bitcoin').show(truncate=False)


    ###############################################################################################################################################################################
    # Recupera el precio de Bitcoin en USD y por fecha para el primer trimestre de 2025
    ###############################################################################################################################################################################

    # 1. Leer precios desde la API de CoinGecko (últimos 365 días — rango válido)
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"

    # Primer trimestre de 2025
    start_date = "2025-01-01"
    end_date = "2025-03-31"

    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

    params = {
        "vs_currency": "usd",
        "from": start_timestamp,  # Fecha de inicio (01-01-2025)
        "to": end_timestamp       # Fecha de fin (31-03-2025)
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Obtener la lista de precios (formato: [timestamp_ms, price])
    prices = data.get("prices", []) 

    # 3. Crear DataFrame de PySpark a partir del JSON
    df_raw = spark.createDataFrame(prices, ["timestamp_ms", "price"])

    # 4. Convertir timestamp a fecha legible
    df_precio = df_raw \
        .withColumn("timestamp", from_unixtime(col("timestamp_ms") / 1000).cast("timestamp")) \
        .withColumn("date", to_date("timestamp")) \
        .select("date", "price")
        
        
    # Escribir el DataFrame a MySQL
    df_precio.write.jdbc(
        url=mysql_url,
        table="precio_bitcoin",
        mode="overwrite", 
        properties=mysql_properties
    )

    # Leer la tabla
    df_precio_avg = spark.read.jdbc(
        url=mysql_url,
        table="precio_bitcoin",
        properties=mysql_properties
    )

    # Mostrar los datos
    print("lectura de tabla precios")
    df_precio_avg.show()

    # Agrupar por fecha para obtencion de precio promedio por dia

    df_gb_fecha= df_precio_avg.groupBy("date").agg(
        avg(col("price")).alias("precio_promedio_fecha")
        ).orderBy("date")

    print("Agrupar por fecha para promedio")
    df_gb_fecha.show(10, truncate=False)


    ## Obtencion promedio movil de cinco dias
    ventana = Window.orderBy("date").rowsBetween(-4, 0)
    df_avg_m5 = df_gb_fecha.withColumn("avg_movil", avg(col("precio_promedio_fecha")).over(ventana))

    print("Promedio de cinco dias atras")
    df_avg_movil = df_avg_m5.orderBy("date").show(truncate=False) 

    # Parar SparkSession
    spark.stop()
    sys.exit(0)


if __name__ == "__main__":
    main()
