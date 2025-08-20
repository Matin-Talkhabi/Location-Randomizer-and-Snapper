# Location Randomizer and Snapper

This Python script allows you to generate a random geographical point at a specified distance from a starting location and then snap that point to the nearest road. It supports both decimal and Degrees, Minutes, Seconds (DMS) coordinate formats for input and output.

## Features

- **Flexible Location Input**: Provide starting coordinates in either decimal (latitude, longitude) or DMS format. If no coordinates are provided, the script attempts to use your current IP address for location.
- **DMS <-> Decimal Conversion**: Includes utility functions to convert between DMS and decimal coordinate systems.
- **Random Point Generation**: Calculates a random point at a given distance (in meters) from the starting location.
- **Road Snapping**: Utilizes OSMnx to snap the randomly generated point to the closest road network, providing realistic geographical points.

## Prerequisites

Before running the script, ensure you have Python 3 installed. You will also need the following Python packages:

- `osmnx`
- `geocoder`

You can install them using pip:

```bash
pip install -r requirements.txt
```

## Usage

1.  **Run the script**:
    ```bash
    python main.py
    ```

2.  **Enter Start Coordinates**: The script will prompt you to enter your starting coordinates. You can provide them in two formats:
    -   **Decimal**: `34.0522, -118.2437` (Latitude, Longitude)
    -   **DMS**: `34°38'31.7"N 50°52'46.0"E` (Latitude DMS Longitude DMS)
    
    Alternatively, you can leave the input empty to use your current IP address as the starting location.

3.  **Enter Distance**: After the starting location is determined, you will be asked to enter the desired distance in meters.

4.  **View Results**: The script will then output the calculated random road point in both decimal and DMS formats.

## Example

```
📍 Enter start coordinates (decimal or DMS), or leave empty to use IP location: 34.642139, 50.879444
✅ Start location (Decimal): 34.642139, 50.879444
✅ Start location (DMS): 34°38'31.7"N 50°52'46.0"E
📏 Enter distance in meters: 2000
🎯 Random road point (Decimal): 34.6238126 50.8758402
🎯 Random road point (DMS): 34°37'25.73"N 50°52'33.02"E
``` 