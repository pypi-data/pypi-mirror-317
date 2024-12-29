import geopandas as gpd
import os

# read vector
def read_vector(file_path, format="shp"):
    if format == "shp":
        gdf = gpd.read_file(file_path)
    elif format == "geojson":
        gdf = gpd.read_file(file_path, driver="GeoJSON")
    elif format == "KML":
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        raise ValueError(f"format value {format} error!")
    
    return gdf

# write vector
def write_vector(file_path, gdf, format="shp"):
    def change_extension(file_path, new_extension):
        base = os.path.splitext(file_path)[0]
        new_file_path = f"{base}.{new_extension.lstrip('.')}"
        return new_file_path

    file_path_new = change_extension(file_path, format)

    if format == "shp":
        gdf.to_file(file_path_new )
    elif format == "geojson":
        gdf.to_file(file_path_new , driver="GeoJSON")
    else:
        raise ValueError(f"format value {format} error!")
    