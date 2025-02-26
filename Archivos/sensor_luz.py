import random
import time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
from connection_component import InfluxDBConnection

def simulate_light_data():
    """Simula el envío de datos de luminosidad cada 5 segundos."""
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
            # Simula la luz entre 100 y 1000 lux
            light = round(random.uniform(100, 1000), 2)
            point = Point("light_sensor").field("lux", light)
            write_api.write(bucket=connection.bucket, org=connection.org, record=point)
            print(f"Luminosidad enviada: {light} lux")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Simulación detenida.")

if __name__ == "__main__":
    simulate_light_data()
