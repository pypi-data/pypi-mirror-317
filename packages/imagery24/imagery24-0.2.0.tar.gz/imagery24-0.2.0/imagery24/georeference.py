from io import BytesIO
from pathlib import Path

import rasterio
from rasterio.control import GroundControlPoint
from rasterio.crs import CRS


def georeference_image(
    input_tiff: Path,
    corner_coords: list[tuple[float, float]],
) -> BytesIO:
    # Open the input TIFF file
    with rasterio.open(input_tiff) as src:
        # Get width and height of the image
        width = src.width
        height = src.height

        # Define image coordinates for the corners (row, col) starting from top-left
        image_coords = [
            (0, 0),  # Upper-left (UL)
            (0, width - 1),  # Upper-right (UR)
            (height - 1, width - 1),  # Lower-right (LR)
            (height - 1, 0),  # Lower-left (LL)
        ]

        # Create GCPs (Ground Control Points) mapping image corners to geographic coordinates
        gcps = [
            GroundControlPoint(
                row=image_coords[i][0],
                col=image_coords[i][1],
                x=corner_coords[i][0],  # Longitude
                y=corner_coords[i][1],  # Latitude
                z=0,  # Elevation (optional, usually 0 for 2D)
            )
            for i in range(4)
        ]

        # Update metadata with CRS (coordinate reference system)
        metadata = src.meta.copy()
        metadata.update(
            {
                "driver": "GTiff",
                "crs": CRS.from_epsg(4326),  # Set CRS to WGS84
                "height": src.height,
                "width": src.width,
            }
        )

        # Write new GeoTIFF to a BytesIO object
        buffer = BytesIO()
        with rasterio.open(buffer, "w", **metadata) as dst:
            dst.write(src.read())  # Write image data
            dst.gcps = (gcps, CRS.from_epsg(4326))  # Add GCPs and CRS

        buffer.seek(0)  # Reset buffer pointer for reading

    return buffer
