#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, date
import matplotlib.dates as mdates
import os
import argparse
import obs_inv_utils.inventory_table_factory as itf
import plot_utils as utils

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
parser.add_argument("-qc_only", dest='qc_only', help="Use this flag to only get the qm0thru3 values versus the default of total ", default=False, type=bool)
parser.add_argument("-separate", dest="plot_separate", help="Boolean to say if you want all typs on one plot or on their own individual. Passing in True will plot each one individually", default=False, type=bool)
parser.add_argument("-typ_list", dest="typ_list", help="List of the typs to plot", type=int, nargs='+')
parser.add_argument("-var_list", dest="var_list", help="List of variables to plot", type=str, nargs='+')
args = parser.parse_args()


#define helper functions for plotting

def plot_timeseries_by_typ_and_variable_tot(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Sort the data by obs_day to ensure proper plotting
    df = df.sort_values(by='obs_day')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width

    # Get unique combinations of typ and variable
    unique_combos = df[['typ', 'variable']].drop_duplicates()

    # Plot data for each typ and variable combination
    for _, row in unique_combos.iterrows():
        typ, variable = row['typ'], row['variable']
        
        # Filter the data for the current typ and variable
        combo_df = df[(df['typ'] == typ) & (df['variable'] == variable)]
        
        # Plot the data with a label that includes both typ and variable
        ax.plot(combo_df['obs_day'], combo_df['tot'], marker='o', label=f'Typ {typ} - Variable {variable}')
    
    # Set title and labels
    ax.set_title('Time Series for Typ and Variable Combinations')
    ax.set_xlabel('Observation Day')
    ax.set_ylabel('TOT')

    # Formatting the x-axis for dates (display only the year)
    ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
    ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
    plt.xticks(rotation=45, ha='right')

    # Add grid and legend
    ax.grid(True)
    ax.legend()

    # Create a string that includes all unique typ and variable combinations
    combo_string = "_".join([f"{row['typ']}_{row['variable']}" for _, row in unique_combos.iterrows()])
    
    # Save the plot as an image or show it
    plt.tight_layout()
    plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
    
    #TODO: handle so the file name doesn't get too long
    # Create the output file name based on unique typ and variable combinations
    file_name = f"timeseries_typ_variable_{combo_string}.png"
    if args.dev:
        file_name = f"timeseries_typ_variable_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    
    fnout = os.path.join(args.out_dir, file_name)
    print(f"saving {fnout}")
    plt.savefig(fnout, bbox_inches='tight')

def plot_timeseries_each_typ_variable_tot(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Sort the data by obs_day to ensure proper plotting
    df = df.sort_values(by='obs_day')
    
    # Get unique combinations of typ and variable
    unique_combos = df[['typ', 'variable']].drop_duplicates()

    # Loop through each typ and variable combination
    for _, row in unique_combos.iterrows():
        typ, variable = row['typ'], row['variable']
        
        # Filter the data for the current typ and variable
        combo_df = df[(df['typ'] == typ) & (df['variable'] == variable)]
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width
        ax.plot(combo_df['obs_day'], combo_df['tot'], marker='o', label=f'Typ {typ} - Variable {variable}')
        
        # Set title and labels
        ax.set_title(f'Time Series for Typ {typ} and Variable {variable}')
        ax.set_xlabel('Observation Day')
        ax.set_ylabel('TOT')

        # Formatting the x-axis for dates (display only the year)
        ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
        ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
        plt.xticks(rotation=45, ha='right')

        # Add grid and legend
        ax.grid(True)
        ax.legend()

        # Create the output file name based on the typ and variable combination
        file_name = f"timeseries_typ_{typ}_variable_{variable}.png"
        if args.dev:
            file_name = f"timeseries_typ_{typ}_variable_{variable}" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        
        fnout = os.path.join(args.out_dir, file_name)
        print(f"saving {fnout}")
        
        # Save the plot as an image
        plt.tight_layout()
        plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
        plt.savefig(fnout, bbox_inches='tight')
        plt.close()  # Close the plot to prevent overlap

def plot_timeseries_by_typ_and_variable_qm0thru3(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Sort the data by obs_day to ensure proper plotting
    df = df.sort_values(by='obs_day')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width

    # Get unique combinations of typ and variable
    unique_combos = df[['typ', 'variable']].drop_duplicates()

    # Plot data for each typ and variable combination
    for _, row in unique_combos.iterrows():
        typ, variable = row['typ'], row['variable']
        
        # Filter the data for the current typ and variable
        combo_df = df[(df['typ'] == typ) & (df['variable'] == variable)]
        
        # Plot the data with a label that includes both typ and variable
        ax.plot(combo_df['obs_day'], combo_df['qm0thru3'], marker='o', label=f'Typ {typ} - Variable {variable}')
    
    # Set title and labels
    ax.set_title('Time Series for Typ and Variable Combinations Quality Controlled')
    ax.set_xlabel('Observation Day')
    ax.set_ylabel('qm0thru3')

    # Formatting the x-axis for dates (display only the year)
    ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
    ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
    plt.xticks(rotation=45, ha='right')

    # Add grid and legend
    ax.grid(True)
    ax.legend()

    # Create a string that includes all unique typ and variable combinations
    combo_string = "_".join([f"{row['typ']}_{row['variable']}" for _, row in unique_combos.iterrows()])
    
    # Save the plot as an image or show it
    plt.tight_layout()
    plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
    
    #TODO: handle so the file name doesn't get too long
    # Create the output file name based on unique typ and variable combinations
    file_name = f"timeseries_qm0thru3_typ_variable_{combo_string}.png"
    if args.dev:
        file_name = f"timeseries_qm0thru3_typ_variable_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    
    fnout = os.path.join(args.out_dir, file_name)
    print(f"saving {fnout}")
    plt.savefig(fnout, bbox_inches='tight')

def plot_timeseries_each_typ_variable_qm0thru3(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Sort the data by obs_day to ensure proper plotting
    df = df.sort_values(by='obs_day')
    
    # Get unique combinations of typ and variable
    unique_combos = df[['typ', 'variable']].drop_duplicates()

    # Loop through each typ and variable combination
    for _, row in unique_combos.iterrows():
        typ, variable = row['typ'], row['variable']
        
        # Filter the data for the current typ and variable
        combo_df = df[(df['typ'] == typ) & (df['variable'] == variable)]
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width
        ax.plot(combo_df['obs_day'], combo_df['tot'], marker='o', label=f'Typ {typ} - Variable {variable}')
        
        # Set title and labels
        ax.set_title(f'Time Series for Typ {typ} and Variable {variable} Quality Controlled')
        ax.set_xlabel('Observation Day')
        ax.set_ylabel('qm0thru3')

        # Formatting the x-axis for dates (display only the year)
        ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
        ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
        plt.xticks(rotation=45, ha='right')

        # Add grid and legend
        ax.grid(True)
        ax.legend()

        # Create the output file name based on the typ and variable combination
        file_name = f"timeseries_qm0thru3_typ_{typ}_variable_{variable}.png"
        if args.dev:
            file_name = f"timeseries_qm0thru3_typ_{typ}_variable_{variable}" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        
        fnout = os.path.join(args.out_dir, file_name)
        print(f"saving {fnout}")
        
        # Save the plot as an image
        plt.tight_layout()
        plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
        plt.savefig(fnout, bbox_inches='tight')
        plt.close()  # Close the plot to prevent overlap

def filter_acceptable_variables(user_input_list):
    # Define the set of acceptable values
    acceptable_values = {"PRESSURE", "SPECIFIC HUMIDITY", "TEMPERATURE", "HEIGHT", "WIND COMPONENTS", "PRECIPITABLE H2O"}
    
    # Convert user input to uppercase and filter based on acceptable values
    filtered_list = [item.upper() for item in user_input_list if item.upper() in acceptable_values]
    
    return filtered_list


variables = None
if args.var_list is not None:
    variables = filter_acceptable_variables(args.var_list)

print(f"Args: QC: {args.qc_only} , Plot Separate: {args.plot_separate}")

#df = utils.get_distinct_prepbufr_by_typ_variable(args.typ_list, variables)

if args.qc_only is True: #quality controlled only
    if args.plot_separate is False:
        plot_timeseries_by_typ_and_variable_qm0thru3(df)
    else: 
        plot_timeseries_each_typ_variable_qm0thru3(df)
else: #total 
    if args.plot_separate is False:
        plot_timeseries_by_typ_and_variable_tot(df)
    else: 
        plot_timeseries_each_typ_variable_tot(df)

print(f"plotting for types: ${args.typ_list} and variables: {variables} completed")