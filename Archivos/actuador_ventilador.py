import time
from influxdb_client import InfluxDBClient
from connection_component import InfluxDBConnection

def control_fan():
    """Actúa como un ventilador que se enciende si la temperatura es alta."""
    connection = InfluxDBConnection(
        url="http://localhost:8086",
        token="BEQp0_xkmLW_Bwya6595hQGjHXlqbobHfpBf7myPKugSkOnnMAiRE3W-t3SLMMdLaDYIwmHhuUQeHd1NspXmgQ==",
        org="jhs",
        bucket="jhs"
    )

    client = connection.get_client()
    query_api = client.query_api()

    fan_status = False  # Estado del ventilador (False = apagado, True = encendido)

    try:
        while True:
            query = f'from(bucket: "{connection.bucket}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "thermometer") |> filter(fn: (r) => r._field == "temperature") |> last()'
            result = query_api.query(org=connection.org, query=query)

            for table in result:
                for record in table.records:
                    temperature = record.get_value()

                    if temperature > 28 and not fan_status:
                        fan_status = True
                        print("🔥 Ventilador ENCENDIDO (Temperatura alta)")
                    elif temperature < 25 and fan_status:
                        fan_status = False
                        print("❄️ Ventilador APAGADO (Temperatura baja)")

            time.sleep(5)
    except KeyboardInterrupt:
        print("Actuador de ventilador detenido.")

if __name__ == "__main__":
    control_fan()
