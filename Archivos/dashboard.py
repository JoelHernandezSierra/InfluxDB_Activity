import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from connection_component import InfluxDBConnection

def fetch_data(measurement, field):
    """Consulta los datos de un sensor en InfluxDB."""
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
        |> filter(fn: (r) => r._measurement == "{measurement}" and r._field == "{field}")
        |> yield(name: "sensor_data")
    '''

    tables = query_api.query_data_frame(query)
    if tables.empty:
        return None

    df = tables[['_time', '_value']].rename(columns={"_time": "Time", "_value": field.capitalize()})
    df['Time'] = pd.to_datetime(df['Time'])
    df.set_index('Time', inplace=True)
    return df

def check_alerts(temp, light, humidity):
    """Muestra alertas si los valores están fuera de los límites normales."""
    alerts = []
    if temp is not None:
        if temp > 35:
            alerts.append("⚠️ ALARMA: Temperatura crítica (>35°C)")
        elif temp > 30:
            alerts.append("⚠️ Advertencia: Temperatura alta (>30°C)")
    
    if light is not None:
        if light > 900:
            alerts.append("⚠️ ALARMA: Luminosidad crítica (>900 lux)")
        elif light > 800:
            alerts.append("⚠️ Advertencia: Luminosidad alta (>800 lux)")
    
    if humidity is not None:
        if humidity < 30 or humidity > 70:
            alerts.append("⚠️ ALARMA: Humedad crítica (<30% o >70%)")
        elif humidity < 40 or humidity > 60:
            alerts.append("⚠️ Advertencia: Humedad fuera de rango (40%-60%)")
    
    alert_text.set("\n".join(alerts))

def update_graphs():
    """Actualiza los gráficos con nuevos datos."""
    ax_temp.clear()
    ax_light.clear()
    ax_humidity.clear()

    temp_data = fetch_data("thermometer", "temperature")
    light_data = fetch_data("light_sensor", "lux")
    humidity_data = fetch_data("hygrometer", "humidity")

    temp_value = temp_data['Temperature'].iloc[-1] if temp_data is not None else None
    light_value = light_data['Lux'].iloc[-1] if light_data is not None else None
    humidity_value = humidity_data['Humidity'].iloc[-1] if humidity_data is not None else None

    check_alerts(temp_value, light_value, humidity_value)

    if temp_data is not None:
        ax_temp.plot(temp_data.index, temp_data['Temperature'], marker='o', linestyle='-', color='r')
        ax_temp.set_title("Temperatura")
        ax_temp.set_ylabel("°C")
        ax_temp.grid(True)
    
    if light_data is not None:
        ax_light.plot(light_data.index, light_data['Lux'], marker='o', linestyle='-', color='y')
        ax_light.set_title("Luminosidad")
        ax_light.set_ylabel("Lux")
        ax_light.grid(True)
    
    if humidity_data is not None:
        ax_humidity.plot(humidity_data.index, humidity_data['Humidity'], marker='o', linestyle='-', color='b')
        ax_humidity.set_title("Humedad")
        ax_humidity.set_ylabel("%")
        ax_humidity.grid(True)
    
    canvas.draw()
    root.after(5000, update_graphs)  # Actualiza cada 5 segundos

# Configurar la interfaz gráfica
root = tk.Tk()
root.title("Dashboard de Sensores")
root.geometry("900x700")

fig, (ax_temp, ax_light, ax_humidity) = plt.subplots(3, 1, figsize=(8, 8))
fig.tight_layout()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

alert_text = tk.StringVar()
alert_label = tk.Label(root, textvariable=alert_text, font=("Arial", 12), fg="red")
alert_label.pack()

update_graphs()
root.mainloop()
