import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd
from shapely import geometry
import mercantile
from tqdm import tqdm
import os
import tempfile
import argparse


def process_tiles(input_shp, minx, miny, maxx, maxy, output_file):
    if input_shp:
        bbox = gpd.read_file(input_shp)
        coords = bbox.iloc[0]['geometry'].exterior.coords.xy
        points_list = list(zip(coords[0], coords[1]))
        aoi = Polygon(points_list)
    else:
        aoi = Polygon([(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)])

    minx, miny, maxx, maxy = aoi.bounds

    quad_keys = set()
    for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
        quad_keys.add(mercantile.quadkey(tile))
    quad_keys = list(quad_keys)
    print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")

    df = pd.read_csv(
        "https://minedbuildings.z5.web.core.windows.net/global-buildings/dataset-links.csv", dtype=str
    )

    idx = 0
    combined_gdf = gpd.GeoDataFrame()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_fns = []
        for quad_key in tqdm(quad_keys):
            rows = df[df["QuadKey"] == quad_key]
            if rows.shape[0] == 1:
                url = rows.iloc[0]["Url"]

                df2 = pd.read_json(url, lines=True)
                df2["geometry"] = df2["geometry"].apply(geometry.shape)

                gdf = gpd.GeoDataFrame(df2, crs=4326)
                fn = os.path.join(tmpdir, f"{quad_key}.geojson")
                tmp_fns.append(fn)
                if not os.path.exists(fn):
                    gdf.to_file(fn, driver="GeoJSON")
            elif rows.shape[0] > 1:
                raise ValueError(
                    f"Multiple rows found for QuadKey: {quad_key}")
            else:
                print(f"QuadKey not found in dataset: {quad_key}")

        for fn in tmp_fns:
            gdf = gpd.read_file(fn)
            gdf = gdf[gdf.geometry.within(aoi)]
            gdf['id'] = range(idx, idx + len(gdf))
            idx += len(gdf)
            combined_gdf = pd.concat([combined_gdf, gdf], ignore_index=True)

    combined_gdf.to_file(output_file)


def main():

    parser = argparse.ArgumentParser(
        description="Download and process building footprints from tile data.")
    parser.add_argument("--input_shp", type=str,
                        help="Path to input shapefile for AOI (optional if bounding box is provided)", default=None)
    parser.add_argument(
        "--minx", type=float, help="Minimum X coordinate of bounding box", default=None)
    parser.add_argument(
        "--miny", type=float, help="Minimum Y coordinate of bounding box", default=None)
    parser.add_argument(
        "--maxx", type=float, help="Maximum X coordinate of bounding box", default=None)
    parser.add_argument(
        "--maxy", type=float, help="Maximum Y coordinate of bounding box", default=None)
    parser.add_argument("--output", type=str, required=True,
                        help="Output file path for the resulting shapefile")

    args = parser.parse_args()

    if not args.input_shp and (args.minx is None or args.miny is None or args.maxx is None or args.maxy is None):
        parser.error(
            "Either --input_shp or all bounding box arguments (--minx, --miny, --maxx, --maxy) must be provided.")

    process_tiles(args.input_shp, args.minx, args.miny,
                  args.maxx, args.maxy, args.output)
    return None


if __name__ == "__main__":
    main()
