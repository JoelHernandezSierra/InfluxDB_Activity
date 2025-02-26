from influxdb_client.rest import ApiException
from connection_component import InfluxDBConnection

def read_last_temperature():
    """Lee el último valor de temperatura desde InfluxDB."""
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
        |> filter(fn: (r) => r._measurement == "thermometer" and r._field == "temperature")
        |> last()
    '''

    try:
        tables = query_api.query(query)
        for table in tables:
            for record in table.records:
                print(f"Última temperatura registrada: {record.get_value()}°C")
    except ApiException as e:
        print(f"Error al consultar InfluxDB: {e}")

if __name__ == "__main__":
    read_last_temperature()
