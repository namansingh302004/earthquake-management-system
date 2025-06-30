import numpy as np
import matplotlib.pyplot as plt
import json
import geojson

def generate_points(center_lat, center_lng, inner_radius, outer_radius, count, interior_ratio=0.3):
    """
    Generate random points both inside and outside the inner radius.
    
    :param center_lat: Latitude of the center point
    :param center_lng: Longitude of the center point
    :param inner_radius: Inner radius (in meters)
    :param outer_radius: Outer radius (in meters)
    :param count: Total number of random points to generate
    :param interior_ratio: Ratio of points inside the inner radius (default 30%)
    :return: Two lists of points (interior and exterior)
    """
    exterior_points = []
    interior_points = []
    
    num_interior = int(count * interior_ratio)
    num_exterior = count - num_interior

    # Generate exterior (donut) points
    for _ in range(num_exterior):
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(inner_radius, outer_radius)
        
        lat_offset = (radius / 111000) * np.cos(angle)
        lng_offset = (radius / (111000 * np.cos(np.radians(center_lat)))) * np.sin(angle)
        
        exterior_points.append((center_lat + lat_offset, center_lng + lng_offset))

    # Generate interior points
    for _ in range(num_interior):
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(0, inner_radius)
        
        lat_offset = (radius / 111000) * np.cos(angle)
        lng_offset = (radius / (111000 * np.cos(np.radians(center_lat)))) * np.sin(angle)
        
        interior_points.append((center_lat + lat_offset, center_lng + lng_offset))
    
    return interior_points, exterior_points

def save_points_to_geojson(interior_points, exterior_points, geojson_filename):
    """
    Save points to a GeoJSON file, marking interior and exterior separately.
    
    :param interior_points: List of points inside the inner radius
    :param exterior_points: List of points in the donut region
    :param geojson_filename: Name of the output GeoJSON file
    """
    features = []
    
    for point in interior_points:
        features.append(geojson.Feature(
            geometry=geojson.Point((point[1], point[0])),
            properties={"region": "interior"}
        ))
    
    for point in exterior_points:
        features.append(geojson.Feature(
            geometry=geojson.Point((point[1], point[0])),
            properties={"region": "exterior"}
        ))
    
    feature_collection = geojson.FeatureCollection(features)
    
    with open(geojson_filename, 'w') as geojson_file:
        geojson.dump(feature_collection, geojson_file, indent=2)
    print(f"Points saved to {geojson_filename}")

def plot_points(interior_points, exterior_points):
    """
    Plot the generated points using Matplotlib.
    """
    int_lats, int_lngs = zip(*interior_points)
    ext_lats, ext_lngs = zip(*exterior_points)

    plt.figure(figsize=(8, 8))
    plt.scatter(ext_lngs, ext_lats, color='red', s=10, label="Exterior (Donut)")
    plt.scatter(int_lngs, int_lats, color='blue', s=10, label="Interior")
    plt.legend()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Interior & Exterior Points in a Donut Shape")
    plt.grid(True)
    plt.show()

# Example usage
center_lat = 12.8406
center_lng = 80.1534
inner_radius = 1750   # meters
outer_radius = 4000  # meters
count = 15000         # total points

interior_points, exterior_points = generate_points(center_lat, center_lng, inner_radius, outer_radius, count)

# Save to GeoJSON
save_points_to_geojson(interior_points, exterior_points, "random_donut_points.geojson")

# Plot
plot_points(interior_points, exterior_points)
