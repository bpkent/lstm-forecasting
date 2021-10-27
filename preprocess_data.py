"""
Purple Air data for six sensors around Texas, in Fall 2021.

The data was downloaded manually from the following links:

- https://www.purpleair.com/sensorlist?key=1U1W11IBB9534IR2&show=98485
- https://www.purpleair.com/sensorlist?key=IW8XRZTM8EIX1MQU&show=92075
- https://www.purpleair.com/sensorlist?key=RPELHZ3E1V9Q0LOV&show=99593
- https://www.purpleair.com/sensorlist?key=D0SDNRW5UCRYI3DD&show=28851
- https://www.purpleair.com/sensorlist?key=CZPJJFPVJMOXZ1UZ&show=2837
- https://www.purpleair.com/sensorlist?key=QU9289C2XOCUL41V&show=65197

Enter the start date (September 1, 2021) and end date (October 21, 2021) manually and
click the button that says "Download Primary (A)".
"""

from pathlib import Path
import pandas as pd

data_folder = Path("purple_air_pm25")
metric = "PM2.5_ATM_ug/m3"

df = pd.DataFrame()
coordinates = []

for f in data_folder.iterdir():
    file_name = f.stem
    sensor_name = file_name[: file_name.find("(outside)") - 1]

    ix_coords_start = file_name.find(") (") + 3
    ix_coords_stop = file_name.find(") Primary")
    latitude, longitude = file_name[ix_coords_start:ix_coords_stop].split()
    coordinates.append((sensor_name, latitude, longitude))

    df_temp = pd.read_csv(f, parse_dates=["created_at"])
    print(f"Sensor: {sensor_name}\t Num rows: {len(df_temp)}")

    df_temp.set_index("created_at", inplace=True)
    df_temp.sort_index(inplace=True)
    df_temp = df_temp.resample("2T").mean().interpolate()
    df[sensor_name] = df_temp[metric]

df.rename(
    columns={
        "Zilker #1": "Austin",
        "Sage Park - Midland, TX": "Midland",
        "Mt. Zion and Sudith": "Midlothian",
        "AMIS Visitor Center": "Del Rio",
        "McAllenNE24": "McAllen",
        "Royal Oaks Houston Tx - Outside": "Houston",
    },
    inplace=True,
)

df.to_csv("processed_pm25.csv", index=True)

coordinates = pd.DataFrame.from_records(
    coordinates, columns=["sensor", "latitude", "longitude"]
)
coordinates.to_csv("sensor_coordinates.csv", index=False)
