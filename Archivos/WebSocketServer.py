import asyncio
import websockets
import pandas as pd
from connection_component import InfluxDBConnection

async def send_temperature_data(websocket):
    """Envía datos de temperatura en tiempo real a los clientes conectados."""
    connection = InfluxDBConnection(
        url="http://localhost:8086",
        token="BEQp0_xkmLW_Bwya6595hQGjHXlqbobHfpBf7myPKugSkOnnMAiRE3W-t3SLMMdLaDYIwmHhuUQeHd1NspXmgQ==",
        org="jhs",
        bucket="jhs"
    )

    client = connection.get_client()
    query_api = connection.get_query_api(client)

    last_timestamp = None  # Almacena el último timestamp enviado

    try:
        while True:
            # Consulta con pivot() para estructurar los datos correctamente
            query = f'''
            from(bucket: "{connection.bucket}")
                |> range(start: -10s)
                |> filter(fn: (r) => r._measurement == "thermometer")
                |> filter(fn: (r) => r._field == "temperature")
                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
            '''
            tables = query_api.query_data_frame(query)

            # Verificar si hay datos y mostrar columnas disponibles
            if not tables.empty:
                print("Datos recibidos de InfluxDB:\n", tables.head())  # Mostrar primeras filas
                print("Columnas disponibles:", tables.columns)  # Mostrar nombres de columnas

                # Verificar si las columnas existen antes de procesar los datos
                if 'temperature' in tables.columns and '_time' in tables.columns:
                    df = tables[['_time', 'temperature']].rename(columns={"_time": "Time", "temperature": "Temperature"})
                    df['Time'] = pd.to_datetime(df['Time'])
                    new_data = df[df['Time'] > (last_timestamp or df['Time'].min())]

                    if not new_data.empty:
                        last_timestamp = new_data['Time'].max()
                        # Enviar datos nuevos a través del WebSocket
                        for _, row in new_data.iterrows():
                            await websocket.send(f"Tiempo: {row['Time']}, Temperatura: {row['Temperature']}°C")
                else:
                    print("⚠️ No se encontraron las columnas esperadas. Revisa la consulta en InfluxDB.")

            await asyncio.sleep(5)  # Pausa entre consultas
    except websockets.exceptions.ConnectionClosed:
        print("Conexión cerrada con el cliente.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Configurar el servidor WebSocket
async def main():
    server = await websockets.serve(send_temperature_data, "0.0.0.0", 8765)
    print("Servidor WebSocket iniciado en ws://0.0.0.0:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
