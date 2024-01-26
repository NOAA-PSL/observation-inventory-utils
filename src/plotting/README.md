Scripts for plotting data contained in either the sqlite or mysql databases.

plot_barcode_family.py and plot_line_family.py are built to use sqlite as the backend. 

Scripts which contain "mysql" in title reference the mysql database.


# Usage

```sh
python3 plot_mysql_dir_sensor_sat.py --sidb ../satinfo 
```

## Flag options 

--sidb provides the location of the satinfo folder for plots which go down to the satellite level to include the black/white list 
if not included, then the plot will be all black and not sure any blue lines 

-o the location where the plot should be saved to.
if not included, it will save to a folder called figures in the location of the script 

-dev this will append a timestamp to the name of the plot to prevent overwriting the same file during development stages 

# Example Outputs

plot_mysql_dir_sensor_sat.py with --sidb provided

![NNJA Directory, Sensor, Satellite](/src/plotting/examples/all_line_observations_inventory_dir_sensor_sat.png "NNJA Directory, Sensor, Satellite")

