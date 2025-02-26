import random
import time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from connection_component import InfluxDBConnection

def simulate_temperature_data():
    """Simula el envío de datos de temperatura cada 5 segundos."""
    connection = InfluxDBConnection(
        url="http://localhost:8086",
        token="BEQp0_xkmLW_Bwya6595hQGjHXlqbobHfpBf7myPKugSkOnnMAiRE3W-t3SLMMdLaDYIwmHhuUQeHd1NspXmgQ==",
        org="jhs",
        bucket="jhs"
    )
    
    client = connection.get_client()
    write_api = connection.get_write_api(client)

    try:
        while True:
            # Genera datos de temperatura aleatoria entre 20 y 30 grados.
            temperature = round(random.uniform(20, 30), 2)
            point = Point("thermometer").field("temperature", temperature)
            write_api.write(bucket=connection.bucket, org=connection.org, record=point)
            print(f"Temperatura enviada: {temperature}°C")
            time.sleep(5)  # Simula el envío cada 5 segundos
    except KeyboardInterrupt:
        print("Simulación detenida.")

if __name__ == "__main__":
    simulate_temperature_data()
