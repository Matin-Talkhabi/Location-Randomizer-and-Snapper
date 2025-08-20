import math
import random
import osmnx as ox
import geocoder
import re

# --- DMS <-> Decimal ---
def dms_to_decimal(dms_str):
    regex = r"(\d+)°(\d+)'([\d.]+)\"?([NSEW])"
    match = re.match(regex, dms_str.strip())
    if not match:
        raise ValueError(f"Invalid DMS format: {dms_str}")
    deg, minute, sec, direction = match.groups()
    deg, minute, sec = int(deg), int(minute), float(sec)

    decimal = deg + minute/60 + sec/3600
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def decimal_to_dms(lat, lon):
    def convert(value, positive, negative):
        direction = positive if value >= 0 else negative
        value = abs(value)
        deg = int(value)
        minute = int((value - deg) * 60)
        sec = (value - deg - minute/60) * 3600
        return f"{deg}°{minute}'{sec:.2f}\"{direction}"

    lat_dms = convert(lat, 'N', 'S')
    lon_dms = convert(lon, 'E', 'W')
    return lat_dms, lon_dms

def parse_location_input(user_input):
    try:
        if "," in user_input and "°" not in user_input:  # Decimal format
            lat, lon = map(float, user_input.split(","))
            return lat, lon
        if "°" in user_input:  # DMS format
            parts = user_input.split()
            if len(parts) != 2:
                raise ValueError("Must provide both latitude and longitude!")
            lat = dms_to_decimal(parts[0])
            lon = dms_to_decimal(parts[1])
            return lat, lon
        raise ValueError("Unknown coordinate format!")
    except Exception as e:
        print("❌ Error parsing coordinates:", e)
        exit(1)

# --- Get starting location ---
def get_start_location():
    user_input = input("📍 Enter start coordinates (decimal or DMS), or leave empty to use IP location: ").strip()
    if user_input:
        return parse_location_input(user_input)
    else:
        g = geocoder.ip("me")
        if g.ok:
            return g.latlng[0], g.latlng[1]
        else:
            print("❌ Could not get location from GPS/IP!")
            exit(1)

# --- Generate random point at given distance ---
def random_point(lat, lon, distance_m):
    distance_km = distance_m / 1000.0
    R = 6371.0
    bearing = random.uniform(0, 2 * math.pi)

    lat1 = math.radians(lat)
    lon1 = math.radians(lon)

    lat2 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance_km / R) * math.cos(lat1),
                             math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2))

    return math.degrees(lat2), math.degrees(lon2)

# --- Snap to nearest road ---
def snap_to_road(lat, lon):
    G = ox.graph_from_point((lat, lon), dist=1000, network_type="walk")  
    node, dist = ox.distance.nearest_nodes(G, lon, lat, return_dist=True)
    return (G.nodes[node]['y'], G.nodes[node]['x'])

# --- Main ---
if __name__ == "__main__":
    start_lat, start_lon = get_start_location()
    print("✅ Start location (Decimal):", start_lat, start_lon)
    print("✅ Start location (DMS):", *decimal_to_dms(start_lat, start_lon))

    distance = float(input("📏 Enter distance in meters: "))

    rand_lat, rand_lon = random_point(start_lat, start_lon, distance)
    road_lat, road_lon = snap_to_road(rand_lat, rand_lon)

    road_lat_dms, road_lon_dms = decimal_to_dms(road_lat, road_lon)

    print("🎯 Random road point (Decimal):", road_lat, road_lon)
    print("🎯 Random road point (DMS):", road_lat_dms, road_lon_dms)
