import numpy as np
import pandas as pd

# Load input data from a CSV file (adjust the file path)
input_data_df = pd.read_csv("input_data.csv")

# Extract data from the DataFrame
wind_farm_names = input_data_df["Plant_Name"]
individual_forecasts = input_data_df["Forecast"]
wind_farm_capacities = input_data_df["Capacity"]

# Create a dictionary to store zonal mappings
zone_mapping = {
    'E': 'East',
    'N': 'North',
    'W': 'West',
    'S': 'South'
}

# Create a dictionary to store zonal capacities
zonal_capacities = {
    "East": 2000,
    "North": 2500,
    "West": 1500,
    "South": 4000
}

# State capacity
state_capacity = 12000  # State Capacity

# Normalize the individual forecasts to match the state-level forecast
total_individual_forecast = sum(individual_forecasts)
scale_factor = state_capacity / total_individual_forecast
normalized_individual_forecasts = individual_forecasts * scale_factor

# Create an array to store the initial redistributed output
final_output = normalized_individual_forecasts

# Maximum number of iterations
max_iterations = 100
tolerance = 0.1

for iteration in range(max_iterations):
    total_forecast = np.zeros(len(wind_farm_names))
    total_zonal_forecast = {zone: 0 for zone in zonal_capacities.keys()}

    # Calculate total forecast for each wind farm
    for i, wind_farm_name in enumerate(wind_farm_names):
        zonal_prefix = wind_farm_name[0]
        zone = zone_mapping.get(zonal_prefix, None)

        if zone is not None:
            total_forecast[i] = final_output[i]
            total_zonal_forecast[zone] += final_output[i]
        else:
            print(f"Error: Unrecognized zone for wind farm {wind_farm_name}")

    # Calculate scaling factors to match zonal and state forecasts
    scaling_factors = {}
    for zone, forecast in total_zonal_forecast.items():
        scaling_factors[zone] = zonal_capacities[zone] / forecast

    state_forecast = sum(total_zonal_forecast.values())
    state_scaling_factor = state_capacity / state_forecast

    # Apply scaling factors to the forecasts
    for i in range(len(wind_farm_names)):
        zonal_prefix = wind_farm_names[i][0]
        zone = zone_mapping.get(zonal_prefix, None)

        if zone is not None:
            final_output[i] = total_forecast[i] * scaling_factors[zone] * state_scaling_factor

    # Check for convergence
    if all(abs(final_output - total_forecast) < tolerance):
        print(f"Converged after {iteration + 1} iterations.")
        break

output_data.to_csv("output_data.csv", index=False)
from google.colab import files
files.download('output_data.csv')