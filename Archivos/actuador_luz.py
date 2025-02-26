import time
from influxdb_client import InfluxDBClient
from connection_component import InfluxDBConnection

def control_light():
    """Actúa como una luz que se enciende si la luminosidad es baja."""
    connection = InfluxDBConnection(
        url="http://localhost:8086",
        token="StpdsQrPrK_eRYDVcxNF3gFxSe0pPoKbtLe-qsxfZIl_fW-kxb2dvZT_gIpK-tS_U7hZipu4oNJaPMN7mMDgrw==",
        org="jhs",
        bucket="jhs"
    )

    client = connection.get_client()
    query_api = client.query_api()

    light_status = False  # Estado de la luz (False = apagada, True = encendida)

    try:
        while True:
            query = f'from(bucket: "{connection.bucket}") |> range(start: -1m) |> filter(fn: (r) => r._measurement == "light_sensor") |> filter(fn: (r) => r._field == "lux") |> last()'
            result = query_api.query(org=connection.org, query=query)

            for table in result:
                for record in table.records:
                    luminosity = record.get_value()

                    if luminosity < 300 and not light_status:
                        light_status = True
                        print("💡 Luz ENCENDIDA (Ambiente oscuro)")
                    elif luminosity > 600 and light_status:
                        light_status = False
                        print("🌙 Luz APAGADA (Ambiente iluminado)")

            time.sleep(5)
    except KeyboardInterrupt:
        print("Actuador de luz detenido.")

if __name__ == "__main__":
    control_light()
