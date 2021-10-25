
from pathlib import Path
import pandas as pd

data_folder = Path("purple_air_pm25")
metric = "PM2.5_ATM_ug/m3"

df = pd.DataFrame()
coordinates = []

for f in data_folder.iterdir():
    file_name = f.stem
    sensor_name = file_name[:file_name.find("(outside)") - 1]
    
    ix_coords_start = file_name.find(") (") + 3
    ix_coords_stop = file_name.find(") Primary")
    latitude, longitude = file_name[ix_coords_start:ix_coords_stop].split()
    coordinates.append((sensor_name, latitude, longitude))

    df_temp = pd.read_csv(f, parse_dates=["created_at"])
    print(f"Sensor: {sensor_name}\t Num rows: {len(df_temp)}")

    df_temp.set_index("created_at", inplace=True)
    df_temp = df_temp.resample('2T').mean().interpolate()
    df[sensor_name] = df_temp[metric]

df.to_csv("processed_pm25.csv", index=True)

coordinates = pd.DataFrame.from_records(
    coordinates, columns=["sensor", "latitude", "longitude"]
)
coordinates.to_csv("sensor_coordinates.csv", index=False)