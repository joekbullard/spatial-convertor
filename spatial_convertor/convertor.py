import fiona


def convertor(input: str, output: str, driver: str) -> fiona.Collection:
    """Converts a vector file from one format to another.

    Args:
        input (str): The path to the input vector file.
        output (str): The path to the output vector file.
        driver (str): The driver name for the output file format.
            Supported drivers: 'ESRI Shapefile', 'GeoJSON', 'GPKG', 'CSV', etc.

    Raises:
        OSError: If there is an error opening or writing the files.
        fiona.errors.DriverError: If the specified driver is not supported.

    Example:
        convertor('/path/to/input.shp', '/path/to/output.gpkg', 'GPKG')

    Note:
        This function uses the Fiona library for reading and writing vector files.
        Make sure to have Fiona installed in your Python environment.

    """
    with fiona.open(input) as src:
        output_schema = src.schema

        with fiona.open(
            output,
            mode="w",
            layer=output,
            crs=src.crs,
            driver=driver,
            schema=output_schema,
        ) as dst:
            for feat in src:
                dst.write(feat)

            return dst
