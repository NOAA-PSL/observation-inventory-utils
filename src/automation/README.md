Automation tools for running observation inventory utils. Runs as a separate script from the main source code accessing the main code via CLI calls. 

## Code Setup 

The main script for running the inventory is auto_inventory.py. All the other files support running the inventory. 

atm_dicts.py contains the definition of each atmospheric variable necessary to complete an inventory as well as the dictionary group collecting them all together (i.e. atm_infos)


## Example Usage 

```sh
$ python3 auto_inventory.py 
```
- this will run the base version of all atmopshere variables as 18 separate jobs for the full time period

```sh
$ python3 auto_inventory.py -ago 3 -n_jobs 25
```
- this will run the inventory for the atmosphere variables for the past 3 days as 25 separate jobs 

```sh
python3 auto_inventory.py -end 20231231T180000Z -ago 31 
```
- this will run the inventory for 31 days ending on December 31, 2023 18Z (i.e. the month of December 2023)


Future versions will have additional supported inputs for the '-cat' flag but currently all atmosphere variables will be run each time. 
