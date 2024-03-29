Scripts for plotting data contained in either the SQLite or MySQL databases.

`plot_barcode_family.py` and `plot_line_family.py` are built to use SQLite as the backend. 

Scripts which contain "mysql" in title reference the mysql database.


# Usage

Each script is designed to be called independently and produce a single plot. Calls are made to be to python with flags as necessary as defined below.

Example call:
```sh
python3 plot_mysql_dir_sensor_sat.py --sidb ../satinfo 
```

## Flag options 

* --sidb provides the location of the satellite info (satinfo) folder for plots which go down to the satellite level to include the black/white list

     if not included, then the plot will be all black and not show any blue lines 

* -o path to figure output directory 

    if not included, it will save to a folder called figures in the location of the script 

* -dev this will append a timestamp to the name of the plot to prevent overwriting the same file during development stages 

# Example Output Plots

## All Sensor
`plot_mysql_sensor.py` 

![NNJA Sensor](/src/plotting/examples/all_line_observations_inventory_sensor.png "NNJA Sensor Plot")

## All Prepbufr Report Types
`plot_mysql_typ.py`

![NNJA Typ](/src/plotting/examples/all_line_observations_inventory_typ.png "NNJA Typ Plot")

## All Directory, Sensor, Satellite
`plot_mysql_dir_sensor_sat.py` with --sidb provided

![NNJA Directory, Sensor, Satellite](/src/plotting/examples/all_line_observations_inventory_dir_sensor_sat.png "NNJA Directory, Sensor, Satellite Plot")

## Atmospheric Motion Vectors (AMV) sensors by Satellite
`plot_mysql_sensor_sat_amv.py` with --sidb provided 

![NNJA AMV Sat](/src/plotting/examples/amv_line_observations_inventory_sensor_sat.png "NNJA AMV Sat Plot")

## Geosynchronous (GEO) sensors by Satellite 
`plot_mysql_sensor_sat_geo.py` --sidb provided

![NNJA GEO Sat](/src/plotting/examples/geo_line_observations_inventory_sensor_sat.png "NNJA GEO Sat Plot")

## GPS sensors by Satellite 
`plot_mysql_sensor_sat_gps.py` with --sidb provided

![NNJA GPS Sat](/src/plotting/examples/gps_line_observations_inventory_sensor_sat.png "NNJA GPS Sat Plot")