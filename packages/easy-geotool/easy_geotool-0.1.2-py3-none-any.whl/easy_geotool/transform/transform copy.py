import geopandas as gpd
import rasterio
from rasterio.features import rasterize, shapes
from rasterio.transform import from_bounds
from pyproj import CRS
from shapely.geometry import Point, shape, MultiLineString, LineString
import numpy as np

def vector_to_raster(vector_path, raster_path, pixel_size=10, mode="constant", fill_value=0, burn_value=1, field_name=None):
    """
    将矢量数据转换为栅格数据，支持地理坐标系的转换，以保证分辨率为米，并根据模式选择栅格值。

    参数：
    - vector_path: 矢量数据文件路径 (.shp)
    - raster_path: 输出栅格文件路径 (.tif)
    - pixel_size: 像素大小（米为单位）
    - mode: 栅格填充值模式 ("constant" 或 "field")
    - fill_value: 栅格中非矢量区域的填充值（常量模式）
    - burn_value: 栅格中矢量区域的填充值（常量模式）
    - field_name: 在 "field" 模式下用于填充栅格的字段名
    """
    # 读取矢量数据
    vector_data = gpd.read_file(vector_path)
    crs = vector_data.crs  # 获取矢量的原始坐标系
    
    # 如果是地理坐标系（例如 WGS84），转换为一个适当的投影坐标系
    if not crs.is_projected:
        projected_crs = CRS.from_epsg(3857)  # 使用 Web Mercator 作为投影示例
        vector_data = vector_data.to_crs(projected_crs)
        print(f"坐标系从地理坐标系 {crs} 转换为投影坐标系 {projected_crs}")
    else:
        projected_crs = crs

    # 获取矢量边界和转换矩阵
    minx, miny, maxx, maxy = vector_data.total_bounds
    width = int((maxx - minx) / pixel_size)
    height = int((maxy - miny) / pixel_size)
    
    # 创建栅格转换矩阵
    transform = from_bounds(minx, miny, maxx, maxy, width, height)

    # 根据模式设置填充值
    if mode == "constant":
        shapes = [(geom, burn_value) for geom in vector_data.geometry]
    elif mode == "field":
        # 检查 field_name 是否有效
        if field_name is not None and field_name in vector_data.columns:
            shapes = [(geom, value) for geom, value in zip(vector_data.geometry, vector_data[field_name])]
        else:
            # 尝试自动选择一个数值列
            numeric_columns = vector_data.select_dtypes(include=[float, int]).columns
            if len(numeric_columns) > 0:
                # 选择第一个找到的数值列
                selected_field = numeric_columns[0]
                shapes = [(geom, value) for geom, value in zip(vector_data.geometry, vector_data[selected_field])]
                print(f"提示：未提供有效的 field_name，已自动选择数值列 '{selected_field}'")
            else:
                # 未找到数值列，抛出错误
                raise ValueError("在 'field' 模式下，必须提供有效的 field_name 参数，或在数据中包含数值列")
    else:
        raise ValueError("无效的 mode 参数")

    # 使用 rasterize 生成栅格
    raster_data = rasterize(
        shapes,
        out_shape=(height, width),
        fill=fill_value,
        transform=transform,
        dtype='float32'
    )

    # 保存栅格文件，使用原始矢量的坐标系
    with rasterio.open(
        raster_path,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=raster_data.dtype,
        crs=crs,  # 保持原始坐标系
        transform=transform
    ) as dst:
        dst.write(raster_data, 1)

    print(f"矢量数据已成功转换为栅格数据并保存到 {raster_path}")

def raster_to_points(raster_path, output_path=None, band=1, value_name="value", output_format="shp"):
    """
    将栅格文件转换为点数据并返回GeoDataFrame，选择性保存为文件。
    
    参数:
    - raster_path: str，栅格文件路径
    - output_path: str，可选，输出文件路径（例如 "output.geojson" 或 "output.shp"）
    - output_format: str，可选，保存格式（默认为 "GeoJSON"；也可选择 "ESRI Shapefile" 等其他格式）

    """
    # 读取栅格数据
    with rasterio.open(raster_path) as src:
        raster_data = src.read(band)  # 读取栅格的指定波段波段
        transform = src.transform  # 获取仿射变换，用于坐标计算
        nodata = src.nodata  # 获取无效数据值（NODATA）

    # 创建空列表存储点和栅格值
    points = []
    values = []

    # 遍历栅格的每个像元
    for row in range(raster_data.shape[0]):
        for col in range(raster_data.shape[1]):
            value = raster_data[row, col]
            
            # 排除无效数据
            if value != nodata:
                # 计算像元的地理坐标
                x, y = rasterio.transform.xy(transform, row, col, offset='center')
                # 创建点几何并存储
                points.append(Point(x, y))
                values.append(value)

    # 创建GeoDataFrame
    gdf = gpd.GeoDataFrame({value_name: values, 'geometry': points}, crs=src.crs)

    # 保存到文件（可选）
    if output_path:
        if output_format == "shp":
            gdf.to_file(output_path, driver="ESRI Shapefile")
        elif output_format == "geojson":
            gdf.to_file(output_path, driver="GeoJSON")
        print(f"点数据已保存到 {output_path}.")


def raster_to_lines(raster_path, output_path=None, band=1, output_format="shp"):
    """
    将栅格文件转换为转折线数据并返回GeoDataFrame，选择性保存为文件。
    
    参数:
    - raster_path: str，栅格文件路径
    - output_path: str，可选，输出文件路径（例如 "output.geojson" 或 "output.shp"）
    - output_format: str，可选，保存格式（默认为 "geojson"；可选 "shp" 等格式）
    
    返回:
    - GeoDataFrame 包含栅格转折线的几何信息
    """
    # 读取栅格数据
    with rasterio.open(raster_path) as src:
        raster_data = src.read(band).astype("float32")
        transform = src.transform
        nodata = src.nodata
        
        # 创建掩膜，标记有效数据
        mask = raster_data != nodata

        # 生成转折线的几何形状
        contours = shapes(np.pad(mask.astype(np.uint8), pad_width=1, mode='constant'), 
                          transform=transform)

    # 提取转折线，并转为 LineString
    line_geometries = []
    for geom, value in contours:
        if value == 1:  # 只提取有效区域的边缘
            poly = shape(geom)
            if isinstance(poly.boundary, LineString):  # 如果是单一的 LineString
                line_geometries.append(poly.boundary)
            elif isinstance(poly.boundary, MultiLineString):  # 如果是 MultiLineString
                line_geometries.extend([line for line in poly.boundary])

    # 合并转折线
    multiline = MultiLineString(line_geometries)

    # 创建GeoDataFrame
    gdf = gpd.GeoDataFrame(geometry=[multiline], crs=src.crs)

    # 保存到文件（可选）
    if output_path:
        if output_format.lower() == "shp":
            gdf.to_file(output_path, driver="ESRI Shapefile")
        elif output_format.lower() == "geojson":
            gdf.to_file(output_path, driver="GeoJSON")
        else:
            raise ValueError("不支持的输出格式。请使用 'shp' 或 'geojson'。")
        print(f"栅格转折线数据已保存到 {output_path}.")

def raster_to_polygons(raster_path, output_path=None, band=1, value_name="value", output_format="shp", single_polygon=False):
    """
    将栅格文件转换为面数据并返回GeoDataFrame，选择性保存为文件。
    
    参数:
    - raster_path: str，栅格文件路径
    - output_path: str，可选，输出文件路径（例如 "output.geojson" 或 "output.shp"）
    - value_name: str，可选，面数据的值字段名称（默认为 "value"）
    - output_format: str，可选，保存格式（默认为 "geojson"；可选 "shp" 等格式）
    - single_polygon: bool，可选，如果为 True，则将整个栅格转换为一个单一的面
    
    返回:
    - GeoDataFrame 包含面形几何和栅格值
    """
    # 读取栅格数据
    with rasterio.open(raster_path) as src:
        raster_data = src.read(band).astype('float32')  # 将栅格数据转换为float32类型
        transform = src.transform  # 获取仿射变换
        nodata = src.nodata  # 获取无效数据值（NODATA）

        # 如果 single_polygon 为 True，将所有栅格值设为 1，生成一个单一面
        if single_polygon:
            raster_data = (raster_data != nodata).astype('int32')  # 将有效数据设为 1，无效数据保持为 0


        # 使用 shapes 函数将栅格转换为几何形状生成器，忽略无效数据
        shapes_gen = shapes(raster_data, mask=(raster_data != nodata), transform=transform)

    # 提取几何形状和属性
    geometries = []
    values = []
    i = 0

    for geom, value in shapes_gen:
        geometries.append(shape(geom))
        # 如果 single_polygon 为 True，所有值设为 unique_value，否则保持原值
        values.append(i if single_polygon else value)
        i = i + 1

    # 创建GeoDataFrame
    gdf = gpd.GeoDataFrame({value_name: values, 'geometry': geometries}, crs=src.crs)

    # 保存到文件（可选）
    if output_path:
        if output_format.lower() == "shp":
            gdf.to_file(output_path, driver="ESRI Shapefile")
        elif output_format.lower() == "geojson":
            gdf.to_file(output_path, driver="GeoJSON")
        else:
            raise ValueError("不支持的输出格式。请使用 'shp' 或 'geojson'。")
        print(f"面数据已保存到 {output_path}.")
