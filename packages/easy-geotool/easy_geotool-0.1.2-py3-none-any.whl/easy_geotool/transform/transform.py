import geopandas as gpd
import rasterio
from rasterio.features import rasterize, shapes
from rasterio.transform import from_bounds
from pyproj import CRS
from shapely.geometry import Point, shape, MultiLineString, LineString
import numpy as np

def vector_to_raster(vector_path, output_path=None, pixel_size=10, epsg=3857, mode="constant", fill_value=0, burn_value=1, field_name=None):
    """
    Converts vector data to raster data, supporting coordinate system transformation to ensure meter resolution,
    and sets raster values based on the selected mode.

    Parameters:
    - vector_path: Path to the vector data file (.shp)
    - raster_path: Path to the output raster file (.tif)
    - pixel_size: Pixel size (in meters)
    - mode: Raster fill mode ("constant" or "field")
    - fill_value: Fill value for non-vector areas in the raster (constant mode)
    - burn_value: Fill value for vector areas in the raster (constant mode)
    - field_name: Field name for filling the raster in "field" mode
    """
    # Read vector data
    vector_data = gpd.read_file(vector_path)
    crs = vector_data.crs  # Get the original coordinate system of the vector

    # If it's a geographic coordinate system (e.g., WGS84), convert to a projected coordinate system
    if not crs.is_projected:
        projected_crs = CRS.from_epsg(epsg)  # Use Web Mercator as an example projection
        vector_data = vector_data.to_crs(projected_crs)
        print(f"Coordinate system transformed from geographic {crs} to projected {projected_crs}")
    else:
        projected_crs = crs

    # Get vector bounds and transformation matrix
    minx, miny, maxx, maxy = vector_data.total_bounds
    width = int((maxx - minx) / pixel_size)
    height = int((maxy - miny) / pixel_size)

    # Create raster transformation matrix
    transform = from_bounds(minx, miny, maxx, maxy, width, height)

    # Set fill values based on the mode
    if mode == "constant":
        shapes = [(geom, burn_value) for geom in vector_data.geometry]
    elif mode == "field":
        # Check if field_name is valid
        if field_name is not None and field_name in vector_data.columns:
            shapes = [(geom, value) for geom, value in zip(vector_data.geometry, vector_data[field_name])]
        else:
            # Attempt to auto-select a numeric column
            numeric_columns = vector_data.select_dtypes(include=[float, int]).columns
            if len(numeric_columns) > 0:
                # Select the first numeric column found
                selected_field = numeric_columns[0]
                shapes = [(geom, value) for geom, value in zip(vector_data.geometry, vector_data[selected_field])]
                print(f"Note: No valid field_name provided, auto-selected numeric column '{selected_field}'")
            else:
                # No numeric column found, raise an error
                raise ValueError("In 'field' mode, a valid field_name must be provided, or the data must contain a numeric column")
    else:
        raise ValueError("Invalid mode parameter")

    # Generate raster using rasterize
    raster_data = rasterize(
        shapes,
        out_shape=(height, width),
        fill=fill_value,
        transform=transform,
        dtype='float32'
    )

    # Save the raster file, using the original vector coordinate system
    if output_path:
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,
            dtype=raster_data.dtype,
            crs=crs,  # Retain original coordinate system
            transform=transform
        ) as dst:
            dst.write(raster_data, 1)

        print(f"Vector data successfully converted to raster data and saved to {output_path}")

def raster_to_points(raster_path, output_path=None, band=1, value_name="value", output_format="shp"):
    """
    Converts a raster file to point data and returns a GeoDataFrame, optionally saving as a file.

    Parameters:
    - raster_path: str, Path to the raster file
    - output_path: str, optional, Output file path (e.g., "output.geojson" or "output.shp")
    - output_format: str, optional, Save format (default "GeoJSON"; also "ESRI Shapefile" and others)
    """
    # Read raster data
    with rasterio.open(raster_path) as src:
        raster_data = src.read(band)  # Read specified band of the raster
        transform = src.transform  # Get affine transform for coordinate calculation
        nodata = src.nodata  # Get NODATA value

    # Create empty lists to store points and raster values
    points = []
    values = []

    # Iterate through each cell in the raster
    for row in range(raster_data.shape[0]):
        for col in range(raster_data.shape[1]):
            value = raster_data[row, col]

            # Exclude NODATA values
            if value != nodata:
                # Calculate the geographic coordinates of the cell
                x, y = rasterio.transform.xy(transform, row, col, offset='center')
                # Create point geometry and store
                points.append(Point(x, y))
                values.append(value)

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame({value_name: values, 'geometry': points}, crs=src.crs)

    # Save to file (optional)
    if output_path:
        if output_format == "shp":
            gdf.to_file(output_path, driver="ESRI Shapefile")
        elif output_format == "geojson":
            gdf.to_file(output_path, driver="GeoJSON")
        print(f"Point data saved to {output_path}.")

def raster_to_lines(raster_path, output_path=None, band=1, output_format="shp"):
    """
    Converts a raster file to line data and returns a GeoDataFrame, optionally saving as a file.

    Parameters:
    - raster_path: str, Path to the raster file
    - output_path: str, optional, Output file path (e.g., "output.geojson" or "output.shp")
    - output_format: str, optional, Save format (default "geojson"; can also choose "shp" etc.)
    
    Returns:
    - GeoDataFrame with geometry information of raster contours
    """
    # Read raster data
    with rasterio.open(raster_path) as src:
        raster_data = src.read(band).astype("float32")
        transform = src.transform
        nodata = src.nodata

        # Create mask marking valid data
        mask = raster_data != nodata

        # Generate geometry of contours
        contours = shapes(np.pad(mask.astype(np.uint8), pad_width=1, mode='constant'), 
                          transform=transform)

    # Extract contours and convert to LineString
    line_geometries = []
    for geom, value in contours:
        if value == 1:  # Extract only edges of valid areas
            poly = shape(geom)
            if isinstance(poly.boundary, LineString):  # If single LineString
                line_geometries.append(poly.boundary)
            elif isinstance(poly.boundary, MultiLineString):  # If MultiLineString
                line_geometries.extend([line for line in poly.boundary])

    # Merge contours
    multiline = MultiLineString(line_geometries)

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=[multiline], crs=src.crs)

    # Save to file (optional)
    if output_path:
        if output_format.lower() == "shp":
            gdf.to_file(output_path, driver="ESRI Shapefile")
        elif output_format.lower() == "geojson":
            gdf.to_file(output_path, driver="GeoJSON")
        else:
            raise ValueError("Unsupported output format. Please use 'shp' or 'geojson'.")
        print(f"Raster contour line data saved to {output_path}.")

def raster_to_polygons(raster_path, output_path=None, band=1, value_name="value", output_format="shp", single_polygon=False):
    """
    Converts a raster file to polygon data and returns a GeoDataFrame, optionally saving as a file.

    Parameters:
    - raster_path: str, Path to the raster file
    - output_path: str, optional, Output file path (e.g., "output.geojson" or "output.shp")
    - value_name: str, optional, Field name for polygon values (default "value")
    - output_format: str, optional, Save format (default "geojson"; can choose "shp" etc.)
    - single_polygon: bool, optional, If True, convert the entire raster to a single polygon

    Returns:
    - GeoDataFrame with polygon geometries and raster values
    """
    # Read raster data
    with rasterio.open(raster_path) as src:
        raster_data = src.read(band).astype('float32')  # Convert raster data to float32
        transform = src.transform  # Get affine transform
        nodata = src.nodata  # Get NODATA value

        # If single_polygon is True, set all raster values to 1 to generate a single polygon
    if single_polygon:
        raster_data = (raster_data != nodata).astype('int32')  # Set valid data as 1, invalid as 0

    # Use shapes function to convert raster to geometry generator, ignoring NODATA
    shapes_gen = shapes(raster_data, mask=(raster_data != nodata), transform=transform)

    # Extract geometries and attributes
    geometries = []
    values = []
    i = 0

    for geom, value in shapes_gen:
        geometries.append(shape(geom))
        # If single_polygon, all values are set to a unique value, otherwise retain original values
        values.append(i if single_polygon else value)
        i = i + 1

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame({value_name: values, 'geometry': geometries}, crs=src.crs)

    # Save to file (optional)
    if output_path:
        if output_format.lower() == "shp":
            gdf.to_file(output_path, driver="ESRI Shapefile")
        elif output_format.lower() == "geojson":
            gdf.to_file(output_path, driver="GeoJSON")
        else:
            raise ValueError("Unsupported output format. Please use 'shp' or 'geojson'.")
        print(f"Polygon data saved to {output_path}.")
