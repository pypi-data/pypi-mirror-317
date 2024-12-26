from vgrid.utils import s2, olc, geohash, georef, mgrs, mercantile, maidenhead
from vgrid.utils.gars import garsgrid

import h3

from rhealpixdggs.dggs import RHEALPixDGGS
from rhealpixdggs.utils import my_round
from rhealpixdggs.ellipsoids import WGS84_ELLIPSOID

from vgrid.utils.eaggr.enums.shape_string_format import ShapeStringFormat
from vgrid.utils.eaggr.eaggr import Eaggr
from vgrid.utils.eaggr.shapes.dggs_cell import DggsCell
from vgrid.utils.eaggr.enums.model import Model

from shapely.wkt import loads
from shapely.geometry import shape, Point,Polygon,mapping

import json, re,os,argparse
from vgrid.generator.h3grid import fix_h3_antimeridian_cells
from vgrid.generator.rhealpixgrid import fix_rhealpix_antimeridian_cells
from vgrid.generator.eaggrisea4tgrid import fix_isea4t_antimeridian_cells
from vgrid.generator.eaggrisea4tgrid import fix_isea4t_wkt
from vgrid.utils.antimeridian import fix_polygon

from pyproj import Geod
geod = Geod(ellps="WGS84")
E = WGS84_ELLIPSOID

def h32geojson(h3_code):
    # Get the boundary coordinates of the H3 cell
    cell_boundary = h3.cell_to_boundary(h3_code)    
    if cell_boundary:
        filtered_boundary = fix_h3_antimeridian_cells(cell_boundary)
        # Reverse lat/lon to lon/lat for GeoJSON compatibility
        reversed_boundary = [(lon, lat) for lat, lon in filtered_boundary]
        cell_polygon = Polygon(reversed_boundary)
        
        center_lat, center_lon = h3.cell_to_latlng(h3_code)
        center_lat = round(center_lat,7)
        center_lon = round(center_lon,7)

        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
        cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])  # Perimeter in meters  
        avg_edge_len = round(cell_perimeter/6,2)
        if (h3.is_pentagon(h3_code)):
            avg_edge_len = round(cell_perimeter/5 ,2)   
        resolution = h3.get_resolution(h3_code)        
        
        feature = {
                    "type": "Feature",
                    "geometry": mapping(cell_polygon),
                    "properties": {
                        "h3": h3_code,
                        "center_lat": center_lat,
                        "center_lon": center_lon,
                        "cell_area": cell_area,
                        "avg_edge_len": avg_edge_len,
                        "resolution": resolution
                        }
                    }
        return {
            "type": "FeatureCollection",
            "features": [feature],
        }
    
def h32geojson_cli():
    """
    Command-line interface for h32geojson.
    """
    parser = argparse.ArgumentParser(description="Convert H3 code to GeoJSON")
    parser.add_argument("h3", help="Input H3 code, e.g., h32geojson 8d65b56628e46bf")
    args = parser.parse_args()
    geojson_data = json.dumps(h32geojson(args.h3))
    print(geojson_data)

def s22geojson(cell_id_token):
    # Create an S2 cell from the given cell ID
    cell_id = s2.CellId.from_token(cell_id_token)
    cell = s2.Cell(cell_id)
    if cell:
        # Get the vertices of the cell (4 vertices for a rectangular cell)
        vertices = [cell.get_vertex(i) for i in range(4)]
        # Prepare vertices in (longitude, latitude) format for Shapely
        shapely_vertices = []
        for vertex in vertices:
            lat_lng = s2.LatLng.from_point(vertex)  # Convert Point to LatLng
            longitude = lat_lng.lng().degrees  # Access longitude in degrees
            latitude = lat_lng.lat().degrees   # Access latitude in degrees
            shapely_vertices.append((longitude, latitude))

        # Close the polygon by adding the first vertex again
        shapely_vertices.append(shapely_vertices[0])  # Closing the polygon
        # Create a Shapely Polygon
        cell_polygon = fix_polygon(Polygon(shapely_vertices)) # Fix antimeridian
        lat_lng = cell_id.to_lat_lng()            
        # Extract latitude and longitude in degrees
        center_lat = round(lat_lng.lat().degrees,7)
        center_lon = round(lat_lng.lng().degrees,7)

        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
        cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])  # Perimeter in meters  
        avg_edge_len = round(cell_perimeter/4,2)

        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),
            "properties":{
                "s2_token": cell_id_token,
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area": cell_area,
                "avg_edge_len": avg_edge_len,
                "resolution": cell_id.level()
                }
        }
        
        # Create the FeatureCollection
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }

        # Return the FeatureCollection
    return feature_collection

       
def s22geojson_cli():
    """
    Command-line interface for s22geojson.
    """
    parser = argparse.ArgumentParser(description="Convert S2 cell token to GeoJSON")
    parser.add_argument("s2", help="Input S2 cell token, e.g., s22geojson 31752f45cc94")
    args = parser.parse_args()
    geojson_data = json.dumps(s22geojson(args.s2))
    print(geojson_data)


def rhealpix_cell_to_polygon(cell):
    vertices = [tuple(my_round(coord, 14) for coord in vertex) for vertex in cell.vertices(plane=False)]
    if vertices[0] != vertices[-1]:
        vertices.append(vertices[0])
    vertices = fix_rhealpix_antimeridian_cells(vertices)
    return Polygon(vertices)

def rhealpix2geojson(rhealpix_code):
    rhealpix_code = str(rhealpix_code)
    rhealpix_uids = (rhealpix_code[0],) + tuple(map(int, rhealpix_code[1:]))
    rhealpix_dggs = RHEALPixDGGS(ellipsoid=E, north_square=1, south_square=3, N_side=3) 
    rhealpix_cell = rhealpix_dggs.cell(rhealpix_uids)
    
    if rhealpix_cell:
        resolution = rhealpix_cell.resolution        
        cell_polygon = rhealpix_cell_to_polygon(rhealpix_cell)
        
        center_lat = round(cell_polygon.centroid.y,7)
        center_lon = round(cell_polygon.centroid.x,7)

        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters                
        cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])  # Perimeter in meters  
        avg_edge_len = round(cell_perimeter/4,2)
        if rhealpix_cell.ellipsoidal_shape() == 'dart':
            avg_edge_len = round(cell_perimeter/3,2)

        feature =({
                "type": "Feature",
                "geometry": mapping(cell_polygon),
                "properties": {
                        "rhealpix": str(rhealpix_cell),
                        "center_lat": center_lat,
                        "center_lon": center_lon,
                        "cell_area": cell_area,
                        "avg_edge_len": avg_edge_len,
                        "resolution": resolution
                    }
                })
        
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
            
        return feature_collection

def rhealpix2geojson_cli():
    """
    Command-line interface for rhealpix2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert Rhealpix code to GeoJSON")
    parser.add_argument("rhealpix", help="Input Rhealpix code, e.g., rhealpix2geojson R31260335553825")
    args = parser.parse_args()
    geojson_data = json.dumps(rhealpix2geojson(args.rhealpix))
    print(geojson_data)


def eaggrisea4t2geojson(eaggrisea4t):
    eaggr_dggs = Eaggr(Model.ISEA4T)
    cell_to_shape = eaggr_dggs.convert_dggs_cell_outline_to_shape_string(DggsCell(eaggrisea4t),ShapeStringFormat.WKT)
    cell_to_shape_fixed = loads(fix_isea4t_wkt(cell_to_shape))
    if eaggrisea4t.startswith('00') or eaggrisea4t.startswith('09') or eaggrisea4t.startswith('14') or eaggrisea4t.startswith('04') or eaggrisea4t.startswith('19'):
        cell_to_shape_fixed = fix_isea4t_antimeridian_cells(cell_to_shape_fixed)
    
    if cell_to_shape_fixed:
        resolution = len(eaggrisea4t)-2
        # Compute centroid
        cell_centroid = cell_to_shape_fixed.centroid
        center_lat, center_lon = round(cell_centroid.y,7), round(cell_centroid.x,7)
        # Compute area using PyProj Geod
        cell_polygon = Polygon(list(cell_to_shape_fixed.exterior.coords))

        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters
        cell_perimeter = abs(geod.geometry_area_perimeter(cell_polygon)[1])  # Perimeter in meters  
        avg_edge_len = round(cell_perimeter/3,2)  

        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),
            "properties": {
                 "eaggr_isea4t": eaggrisea4t,
                 "center_lat": center_lat,
                 "center_lon": center_lon,
                 "cell_area": cell_area,
                 "avg_edge_len": avg_edge_len,
                 "resolution": resolution,
                    }
        }

        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        return  feature_collection

def eaggrisea4t2geojson_cli():
    """
    Command-line interface for eaggrisea4t2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert EaggrISEA4T code to GeoJSON")
    parser.add_argument("eaggrisea4t", help="Input EaggrISEA4T code, e.g., eaggrisea4t2geojson 131023133313201333311333")
    args = parser.parse_args()
    geojson_data = json.dumps(eaggrisea4t2geojson(args.eaggrisea4t))
    print(geojson_data)


def eaggrisea3h2geojson(eaggrisea3h):
    eaggr_dggs = Eaggr(Model.ISEA3H)
    cell_to_shape = eaggr_dggs.convert_dggs_cell_outline_to_shape_string(DggsCell(eaggrisea3h),ShapeStringFormat.WKT)
    
    if cell_to_shape:
        coordinates_part = cell_to_shape.replace("POLYGON ((", "").replace("))", "")
        coordinates = []
        for coord_pair in coordinates_part.split(","):
            lon, lat = map(float, coord_pair.strip().split())
            coordinates.append([lon, lat])

        # Ensure the polygon is closed (first and last point must be the same)
        if coordinates[0] != coordinates[-1]:
            coordinates.append(coordinates[0])

        # Step 3: Construct the GeoJSON feature
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]  # Directly use the coordinates list
            },
            "properties": {
                    }
        }

        # Step 4: Construct the FeatureCollection
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        return  feature_collection


def eaggrisea3h2geojson_cli():
    """
    Command-line interface for eaggriseah32geojson.
    """
    parser = argparse.ArgumentParser(description="Convert EeaggrISEA3H code to GeoJSON")
    parser.add_argument("eaggrisea3h", help="Input EeaggrISEA3H code, e.g., eaggrisea3h2geojson '07024,0'")
    args = parser.parse_args()
    geojson_data = json.dumps(eaggrisea3h2geojson(args.eaggrisea3h))
    print(geojson_data)
    
def olc2geojson(olc_code):
    # Decode the Open Location Code into a CodeArea object
    coord = olc.decode(olc_code)
    
    if coord:
        # Create the bounding box coordinates for the polygon
        min_lat, min_lon = coord.latitudeLo, coord.longitudeLo
        max_lat, max_lon = coord.latitudeHi, coord.longitudeHi

        center_lat = round(coord.latitudeCenter,7)
        center_lon = round(coord.longitudeCenter,7)
        resolution = coord.codeLength 

        # Define the polygon based on the bounding box
        cell_polygon = Polygon([
            [min_lon, min_lat],  # Bottom-left corner
            [max_lon, min_lat],  # Bottom-right corner
            [max_lon, max_lat],  # Top-right corner
            [min_lon, max_lat],  # Top-left corner
            [min_lon, min_lat]   # Closing the polygon (same as the first point)
        ])
        
        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
        # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)

        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),
            "properties": {
                "olc": olc_code,  # Include the OLC as a property
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area": cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution": resolution
            }
        }

        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection

def olc2geojson_cli():
    """
    Command-line interface for olc2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert OLC/ Google Plus Codes to GeoJSON")
    parser.add_argument("olc", help="Input OLC, e.g., olc2geojson 7P28QPG4+4P7")
    args = parser.parse_args()
    geojson_data = json.dumps(olc2geojson(args.olc))
    print(geojson_data)


def geohash2geojson(geohash_code):
    # Decode the Open Location Code into a CodeArea object
    bbox =  geohash.bbox(geohash_code)
    if bbox:
        min_lat, min_lon = bbox['s'], bbox['w']  # Southwest corner
        max_lat, max_lon = bbox['n'], bbox['e']  # Northeast corner
        
        center_lat = round((min_lat + max_lat) / 2,7)
        center_lon = round((min_lon + max_lon) / 2,7)
        
        resolution =  len(geohash_code)

        # Define the polygon based on the bounding box
        cell_polygon = Polygon([
            [min_lon, min_lat],  # Bottom-left corner
            [max_lon, min_lat],  # Bottom-right corner
            [max_lon, max_lat],  # Top-right corner
            [min_lon, max_lat],  # Top-left corner
            [min_lon, min_lat]   # Closing the polygon (same as the first point)
        ])
        
        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     

        # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)

        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),
            "properties": {
                "geohash": geohash_code,  # Include the OLC as a property
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area": cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution": resolution
            }
        }
        
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection
    
def geohash2geojson_cli():
    """
    Command-line interface for geohash2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert Geohash code to GeoJSON")
    parser.add_argument("geohash", help="Input Geohash code, e.g., geohash2geojson w3gvk1td8")
    args = parser.parse_args()
    geojson_data = json.dumps(geohash2geojson(args.geohash))
    print(geojson_data)


def mgrs2geojson(mgrs_code,lat=None,lon=None):
    origin_lat, origin_lon, min_lat, min_lon, max_lat, max_lon,resolution = mgrs.mgrscell(mgrs_code)
    if origin_lat:
        # Define the polygon based on the bounding box
        origin_lat = round(origin_lat,7)
        origin_lon = round(origin_lon,7)
        cell_polygon = Polygon([
            [min_lon, min_lat],  # Bottom-left corner
            [max_lon, min_lat],  # Bottom-right corner
            [max_lon, max_lat],  # Top-right corner
            [min_lon, max_lat],  # Top-left corner
            [min_lon, min_lat]   # Closing the polygon (same as the first point)
        ])

        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
        
        # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)

                      
        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),
            "properties": {
                "mgrs": mgrs_code,
                "origin_lat": round(origin_lat,7),
                "origin_lon": round(origin_lon,7),
                "cell_area": cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution": resolution
                }
            }
        
        if lat is not None and lon is not None:
            # Load the GZD JSON file (treated as GeoJSON format) from the same folder
            gzd_json_path = os.path.join(os.path.dirname(__file__), 'gzd.geojson')
            with open(gzd_json_path) as f:
                gzd_json = json.load(f)

            # Convert GZD GeoJSON features to Shapely polygons
            gzd_polygons = [
                {"geometry": shape(feature["geometry"]), "properties": feature["properties"]}
                for feature in gzd_json["features"]
            ]

            # Perform the intersection with the MGRS polygon
            intersection_features = []
            for gzd_polygon_data in gzd_polygons:
                gzd_polygon = gzd_polygon_data["geometry"]
                if cell_polygon.intersects(gzd_polygon):
                    # Find the intersection polygon
                    intersection_polygon = cell_polygon.intersection(gzd_polygon)
                    intersection_min_lon, intersection_min_lat, intersection_max_lon, intersection_max_lat = intersection_polygon.bounds  # Bounds of the polygon
                    interection_area = round(abs(geod.geometry_area_perimeter(intersection_polygon)[0]),2)  # Area in square meters     
                    intersection_width = round(geod.line_length([intersection_min_lon, intersection_max_lon], [intersection_min_lat, intersection_min_lat]),2)
                    intersection_height = round(geod.line_length([intersection_min_lon, intersection_min_lon], [intersection_min_lat, intersection_max_lat]),2)

                    # Convert lat/lon to a Shapely point
                    point = Point(lon, lat)

                    # Check if the point is inside the intersection polygon
                    if intersection_polygon.contains(point):
                        # Manually construct the intersection as a JSON-like structure
                        intersection_feature = {
                            "type": "Feature",
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [list(intersection_polygon.exterior.coords)]
                            },
                            "properties": {
                                "mgrs": mgrs_code,
                                "origin_lat": origin_lat,
                                "origin_lon": origin_lon,
                                "cell_area": interection_area,
                                "cell_width": intersection_width,
                                "cell_height": intersection_height,
                                "resolution": resolution,
                                # **gzd_polygon_data["properties"],  # Include properties from GZD
                            }
                        }
                        intersection_features.append(intersection_feature)

            # If intersections are found, wrap them in a FeatureCollection
            if intersection_features:
                intersection_feature_collection = {
                    "type": "FeatureCollection",
                    "features": intersection_features
                }
                return intersection_feature_collection


        # If no intersection or point not contained, return the original MGRS GeoJSON
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection
    
def mgrs2geojson_cli():
    """
    Command-line interface for mgrs2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert MGRS code to GeoJSON")
    parser.add_argument("mgrs", help="Input MGRS code, e.g., mgrs2geojson 34TGK56063228")
    args = parser.parse_args()
    geojson_data = json.dumps(mgrs2geojson(args.mgrs))
    print(geojson_data)


def georef2geojson(georef_code):
    center_lat, center_lon, min_lat, min_lon, max_lat, max_lon,resolution = georef.georefcell(georef_code)
    if center_lat:
        center_lat = round(center_lat,7)
        center_lon = round(center_lon,7)

        cell_polygon = Polygon([
            [min_lon, min_lat],  # Bottom-left corner
            [max_lon, min_lat],  # Bottom-right corner
            [max_lon, max_lat],  # Top-right corner
            [min_lon, max_lat],  # Top-left corner
            [min_lon, min_lat]   # Closing the polygon (same as the first point)
        ])
        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
          # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)

        feature = {
            "type": "Feature",            
            "geometry": mapping(cell_polygon),          
            "properties": {
                "georef": georef_code,
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area" : cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution": resolution
                }
            }
        
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection

def georef2geojson_cli():
    """
    Command-line interface for georef2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert GEOREF code to GeoJSON")
    parser.add_argument("georef", help="Input GEOREF code, e.g., georef2geojson VGBL42404651")
    args = parser.parse_args()
    geojson_data = json.dumps(georef2geojson(args.georef))
    print(geojson_data)


def tilecode2geojson(tilecode):
    """
    Converts a tilecode (e.g., 'z8x11y14') to a GeoJSON Feature with a Polygon geometry
    representing the tile's bounds and includes the original tilecode as a property.

    Args:
        tilecode (str): The tile code in the format 'zXxYyZ'.

    Returns:
        dict: A GeoJSON Feature with a Polygon geometry and tilecode as a property.
    """
    # Extract z, x, y from the tilecode using regex
    match = re.match(r'z(\d+)x(\d+)y(\d+)', tilecode)
    if not match:
        raise ValueError("Invalid tilecode format. Expected format: 'zXxYyZ'")

    # Convert matched groups to integers
    z = int(match.group(1))
    x = int(match.group(2))
    y = int(match.group(3))

    # Get the bounds of the tile in (west, south, east, north)
    bounds = mercantile.bounds(x, y, z)    

    if bounds:
        # Create the bounding box coordinates for the polygon
        min_lat, min_lon = bounds.south, bounds.west
        max_lat, max_lon = bounds.north, bounds.east

        # tile = mercantile.Tile(x, y, z)
        # quadkey = mercantile.quadkey(tile)

        center_lat = round((min_lat + max_lat) / 2,2)
        center_lon = round((min_lon + max_lon) / 2,2)
        
        cell_polygon = Polygon([
            [min_lon, min_lat],  # Bottom-left corner
            [max_lon, min_lat],  # Bottom-right corner
            [max_lon, max_lat],  # Top-right corner
            [min_lon, max_lat],  # Top-left corner
            [min_lon, min_lat]   # Closing the polygon (same as the first point)
        ])
        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
          # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)

        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),          
            "properties": {
                "tilecode": tilecode,  # Include the OLC as a property
                # "quadkey": quadkey,
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area": cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution": z  # Using the code length as precision
            }
        }

        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection

def tilecode2geojson_cli():
    """
    Command-line interface for tilecode2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert Tilecode to GeoJSON")
    parser.add_argument("tilecode", help="Input Tilecode, e.g. z0x0y0")
    args = parser.parse_args()

    # Generate the GeoJSON feature
    geojson_data = json.dumps(tilecode2geojson(args.tilecode))
    print(geojson_data)


def maidenhead2geojson(maidenhead_code):
    # Decode the Open Location Code into a CodeArea object
    center_lat, center_lon, min_lat, min_lon, max_lat, max_lon, _ = maidenhead.maidenGrid(maidenhead_code)
    if center_lat:
        center_lat = round(center_lat,7)
        center_lon  = round(center_lon,7)
        resolution = int(len(maidenhead_code)/2)
    
        # Define the polygon based on the bounding box
        cell_polygon = Polygon([
            [min_lon, min_lat],  # Bottom-left corner
            [max_lon, min_lat],  # Bottom-right corner
            [max_lon, max_lat],  # Top-right corner
            [min_lon, max_lat],  # Top-left corner
            [min_lon, min_lat]   # Closing the polygon (same as the first point)
        ])
        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
          # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)

        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),       
            "properties": {
                "maidenhead": maidenhead_code,  # Include the OLC as a property
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area": cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution": resolution
            }
        }

        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection

def maidenhead2geojson_cli():
    """
    Command-line interface for maidenhead2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert Maidenhead code to GeoJSON")
    parser.add_argument("maidenhead", help="Input Maidenhead code, e.g., maidenhead2geojson OK30is46")
    args = parser.parse_args()
    geojson_data = json.dumps(maidenhead2geojson(args.maidenhead))
    print(geojson_data)

# SOS: Convert gars_code object to str first
def gars2geojson(gars_code):
    gars_grid = garsgrid.GARSGrid(gars_code)
    wkt_polygon = gars_grid.polygon
    if wkt_polygon:
        # # Create the bounding box coordinates for the polygon
        x, y = wkt_polygon.exterior.xy
        resolution_minute = gars_grid.resolution
        
        min_lon = min(x)
        max_lon = max(x)
        min_lat = min(y)
        max_lat = max(y)

        # Calculate center latitude and longitude
        center_lon = round((min_lon + max_lon) / 2,7)
        center_lat = round((min_lat + max_lat) / 2, 7)

        cell_polygon = Polygon(list(wkt_polygon.exterior.coords))
        cell_area = round(abs(geod.geometry_area_perimeter(cell_polygon)[0]),2)  # Area in square meters     
          # Calculate width (longitude difference at a constant latitude)
        cell_width = round(geod.line_length([min_lon, max_lon], [min_lat, min_lat]),2)
        # Calculate height (latitude difference at a constant longitude)
        cell_height = round(geod.line_length([min_lon, min_lon], [min_lat, max_lat]),2)
        
        feature = {
            "type": "Feature",
            "geometry": mapping(cell_polygon),       
            "properties": {
                "gars": gars_code,
                "center_lat": center_lat,
                "center_lon": center_lon,
                "cell_area": cell_area,
                "cell_width": cell_width,
                "cell_height": cell_height,
                "resolution_minute": resolution_minute
                }
            }
        
        feature_collection = {
            "type": "FeatureCollection",
            "features": [feature]
        }
        
        return feature_collection

def gars2geojson_cli():
    """
    Command-line interface for gars2geojson.
    """
    parser = argparse.ArgumentParser(description="Convert GARS code to GeoJSON")
    parser.add_argument("gars", help="Input GARS code, e.g., gars2geojson 574JK1918")
    args = parser.parse_args()
    geojson_data = json.dumps(gars2geojson(args.gars))
    print(geojson_data)