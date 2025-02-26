import pandas as pd
import matplotlib.pyplot as plt
from connection_component import InfluxDBConnection

def plot_humidity_data():
    """Recupera y grafica los datos de humedad de los últimos 10 minutos."""
    connection = InfluxDBConnection(
        url="http://localhost:8086",
        token="BEQp0_xkmLW_Bwya6595hQGjHXlqbobHfpBf7myPKugSkOnnMAiRE3W-t3SLMMdLaDYIwmHhuUQeHd1NspXmgQ==",
        org="jhs",
        bucket="jhs"
    )
    client = connection.get_client()
    query_api = connection.get_query_api(client)

    query = f'''
    from(bucket: "{connection.bucket}")
        |> range(start: -10m)
        |> filter(fn: (r) => r._measurement == "hygrometer" and r._field == "humidity")
        |> yield(name: "humidity_data")
    '''

    # Ejecutar la consulta
    tables = query_api.query_data_frame(query)
    if tables.empty:
        print("No se encontraron datos de humedad.")
        return

    # Convertir a DataFrame
    df = tables[['_time', '_value']].rename(columns={"_time": "Time", "_value": "Humidity"})
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)

    # Graficar los datos
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Humidity'], marker='o', linestyle='-', color='g')
    plt.title("Humedad del Higrómetro - Últimos 10 minutos")
    plt.xlabel("Tiempo")
    plt.ylabel("Humedad (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_humidity_data()
