import json
import geojson
import numpy as np
from scipy.spatial import ConvexHull

def load_geojson(filename):
    """ Load points from a GeoJSON file """
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def extract_points(data, region_type):
    """ Extract points for the given region type ('interior' or 'exterior') """
    return [
        (feature["geometry"]["coordinates"][0], feature["geometry"]["coordinates"][1])  # (lng, lat)
        for feature in data["features"]
        if feature["properties"]["region"] == region_type
    ]

def compute_convex_hull(points):
    """ Compute the convex hull of a set of points """
    if len(points) < 3:
        return None  # Convex hull needs at least 3 points
    
    points_array = np.array(points)
    hull = ConvexHull(points_array)
    hull_points = [points[i] for i in hull.vertices]
    
    return hull_points

def save_hull_to_geojson(hull_points, output_filename, region_type):
    """ Save the convex hull polygon to a GeoJSON file """
    if hull_points is None:
        print(f"Skipping {region_type} hull: Not enough points.")
        return
    
    hull_points.append(hull_points[0])  # Close the polygon
    
    feature = geojson.Feature(
        geometry=geojson.Polygon([hull_points]),
        properties={"region": region_type}
    )
    
    feature_collection = geojson.FeatureCollection([feature])
    
    with open(output_filename, 'w') as file:
        geojson.dump(feature_collection, file, indent=2)
    
    print(f"Saved {region_type} convex hull to {output_filename}")

# Load original points
geojson_data = load_geojson("random_donut_points.geojson")

# Compute convex hulls
interior_points = extract_points(geojson_data, "interior")
exterior_points = extract_points(geojson_data, "exterior")

interior_hull = compute_convex_hull(interior_points)
exterior_hull = compute_convex_hull(exterior_points)

# Save convex hulls
save_hull_to_geojson(interior_hull, "interior_hull.geojson", "interior")
save_hull_to_geojson(exterior_hull, "exterior_hull.geojson", "exterior")
