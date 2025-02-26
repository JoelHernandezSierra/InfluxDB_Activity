import random
import time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from connection_component import InfluxDBConnection

def simulate_humidity_data():
    """Simula el envío de datos de humedad cada 5 segundos."""
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
            # Genera datos de humedad aleatoria entre 30% y 70%
            humidity = round(random.uniform(30, 70), 2)
            point = Point("hygrometer").field("humidity", humidity)
            write_api.write(bucket=connection.bucket, org=connection.org, record=point)
            print(f"Humedad enviada: {humidity}%")
            time.sleep(5)  # Simula el envío cada 5 segundos
    except KeyboardInterrupt:
        print("Simulación detenida.")

if __name__ == "__main__":
    simulate_humidity_data()
