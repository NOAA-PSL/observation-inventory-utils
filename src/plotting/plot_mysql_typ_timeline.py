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
parser.add_argument("--list", dest="typ_list", help="List of the typs to plot", type=int, nargs='+')
parser.add_argument("-plot_together", dest="plot_together", help="Boolean to say if you want all typs on one plot or on their own individual. True [default] produces one plot, False produces individuals", default=True, type=bool)
args = parser.parse_args()

#define helper functions for plotting

#one plot with all typs layered
def plot_timeseries_all_typ_tot(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Sort the data by obs_day to ensure proper plotting
    df = df.sort_values(by='obs_day')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width

    # Plot data for each typ
    unique_typs = df['typ'].unique()
    for typ in unique_typs:
        typ_df = df[df['typ'] == typ]
        ax.plot(typ_df['obs_day'], typ_df['tot'], marker='o', label=f'Typ {typ}')
    
    # Set title and labels
    ax.set_title('Time Series for All Type Values')
    ax.set_xlabel('Observation Day')
    ax.set_ylabel('TOT')

    # Formatting the x-axis for dates
    ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
    ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
    plt.xticks(rotation=45, ha='right')

    # Add grid and legend
    ax.grid(True)
    ax.legend()

    typ_string = "_".join(map(str, unique_typs))
    # Save the plot as an image or show it
    plt.tight_layout()
    plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
    file_name = f"timeseries_types_{typ_string}.png"
    if args.dev:
        file_name = f"timeseries_types_{typ_string}" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    fnout=os.path.join(args.out_dir,file_name)
    print(f"saving {fnout}")
    plt.savefig(fnout, bbox_inches='tight')

#single plot for each typ
def plot_timeseries_by_typ_tot(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Create a new figure and axis object for each typ
    unique_typs = df['typ'].unique()
    
    for typ in unique_typs:
        # Filter data for the current typ
        typ_df = df[df['typ'] == typ]
        
        # Sort the data by obs_day to ensure proper plotting
        typ_df = typ_df.sort_values(by='obs_day')
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width
        ax.plot(typ_df['obs_day'], typ_df['tot'], marker='o', label=f'Typ {typ}')
        
        # Set title and labels
        ax.set_title(f'Time Series for Typ {typ}')
        ax.set_xlabel('Observation Day')
        ax.set_ylabel('TOT')
        
        # Formatting the x-axis for dates
        ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
        ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
        plt.xticks(rotation=45, ha='right')

        # Add grid and legend
        ax.grid(True)
        ax.legend()

        # Save the plot as an image or show it
        plt.tight_layout()
        plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
        file_name = f"timeseries_type_{typ}.png"
        if args.dev:
            file_name = f"timeseries_type_{typ}" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        fnout=os.path.join(args.out_dir,file_name)
        print(f"saving {fnout}")
        plt.savefig(fnout, bbox_inches='tight')

        # Optionally, clear the figure after each iteration
        plt.clf()

#one plot with all typs layered
def plot_timeseries_all_typ_qm0thru3(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Sort the data by obs_day to ensure proper plotting
    df = df.sort_values(by='obs_day')
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width

    # Plot data for each typ
    unique_typs = df['typ'].unique()
    for typ in unique_typs:
        typ_df = df[df['typ'] == typ]
        ax.plot(typ_df['obs_day'], typ_df['qm0thru3'], marker='o', label=f'Typ {typ}')
    
    # Set title and labels
    ax.set_title('Time Series for All Type Values Quality Controlled')
    ax.set_xlabel('Observation Day')
    ax.set_ylabel('qm0thru3')

    # Formatting the x-axis for dates
    ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
    ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
    plt.xticks(rotation=45, ha='right')

    # Add grid and legend
    ax.grid(True)
    ax.legend()

    typ_string = "_".join(map(str, unique_typs))
    # Save the plot as an image or show it
    plt.tight_layout()
    plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
    file_name = f"timeseries_types_qm0thru3_{typ_string}.png"
    if args.dev:
        file_name = f"timeseries_types_qm0thru3_{typ_string}" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    fnout=os.path.join(args.out_dir,file_name)
    print(f"saving {fnout}")
    plt.savefig(fnout, bbox_inches='tight')

#single plot for each typ
def plot_timeseries_by_typ_qm0thru3(df):
    # Convert obs_day to datetime if it is not already in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['obs_day']):
        df['obs_day'] = pd.to_datetime(df['obs_day'])
    
    # Create a new figure and axis object for each typ
    unique_typs = df['typ'].unique()
    
    for typ in unique_typs:
        # Filter data for the current typ
        typ_df = df[df['typ'] == typ]
        
        # Sort the data by obs_day to ensure proper plotting
        typ_df = typ_df.sort_values(by='obs_day')
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(14, 6))  # Increase figure width
        ax.plot(typ_df['obs_day'], typ_df['qm0thru3'], marker='o', label=f'Typ {typ}')
        
        # Set title and labels
        ax.set_title(f'Time Series for Typ {typ} Quality Controlled')
        ax.set_xlabel('Observation Day')
        ax.set_ylabel('qm0thru3')
        
        # Formatting the x-axis for dates
        ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
        ax.xaxis.set_minor_locator(mdates.MonthLocator())  # Minor ticks every month
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format major ticks as years
        plt.xticks(rotation=45, ha='right')

        # Add grid and legend
        ax.grid(True)
        ax.legend()

        # Save the plot as an image or show it
        plt.tight_layout()
        plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
        file_name = f"timeseries_type_qm0thru3_{typ}.png"
        if args.dev:
            file_name = f"timeseries_type_qm0thru3_{typ}" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
        fnout=os.path.join(args.out_dir,file_name)
        print(f"saving {fnout}")
        plt.savefig(fnout, bbox_inches='tight')

        # Optionally, clear the figure after each iteration
        plt.clf()

df = utils.get_distinct_prepbufr_by_typ(args.typ_list)

if args.qc_only: #quality controlled only
    if args.plot_together:
        plot_timeseries_all_typ_qm0thru3(df)
    else: 
        plot_timeseries_by_typ_qm0thru3(df)
else: #total 
    if args.plot_together:
        plot_timeseries_all_typ_tot(df)
    else: 
        plot_timeseries_by_typ_tot(df)

print(f"plotting for ${args.typ_list} completed")