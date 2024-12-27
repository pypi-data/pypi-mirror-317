import numpy as np
import rasterio
import rasterio.features
from itertools import repeat
import logging
import shapely.geometry
from multiprocessing import Pool
import geopandas as gpd  # Replacing fiona with geopandas

log = logging.getLogger(__name__)
SUPPRESS_ERRORS = True


class UnableToExtractStats(Exception):
    """
    Custom exception raised when statistics extraction fails due to geometry or data issues.
    """

    pass


class RasterStatsExtractor:
    """
    A class for extracting raster statistics based on geometries. It supports single and multiprocessing workflows
    for reading raster files, masking data based on geometries, and computing statistics.
    """

    def __init__(self, suppress_errors=True):
        """
        Initialize the extractor with an option to suppress errors.

        :param suppress_errors: Boolean flag to suppress errors and log warnings instead.
        """
        self.suppress_errors = suppress_errors

    ###########################
    # Array Operations        #
    ###########################
    def arr_stats(
        self, arr, weights=None, output=("min", "max", "sum", "mean", "count")
    ):
        """
        Calculate statistics on a numpy array, optionally applying weights.

        :param arr: NumPy array (masked array supported) on which to calculate statistics.
        :param weights: Optional NumPy array of weights to apply during calculations.
        :param output: Tuple or list of statistics to calculate (e.g., 'min', 'max', 'mean', etc.).
        :return: Dictionary containing the calculated statistics.
        """
        _output = output if isinstance(output, (list, tuple)) else output.split()
        _known_outputs = (
            "min",
            "max",
            "sum",
            "mean",
            "std",
            "median",
            "count",
            "weight_sum",
        )
        if not any(elem in _output for elem in _known_outputs):
            raise ValueError(
                f"Invalid output requested. Allowed outputs are: {_known_outputs}"
            )
        out_vals = dict()
        _arr = np.ma.array(arr)

        arr_compressed = (
            _arr.compressed()
            if any(k in _output for k in ("std", "min", "max", "sum", "median"))
            else None
        )
        if "mean" in _output:
            out_vals["mean"] = (
                np.ma.average(_arr, weights=weights)
                if weights is not None
                else np.ma.mean(_arr)
            )
        if "std" in _output and arr_compressed.size > 1:
            weights_compressed = (
                np.ma.array(weights, mask=_arr.mask).compressed()
                if weights is not None
                else None
            )
            if weights is not None and np.sum(weights_compressed) > 0:
                out_vals["std"] = np.sqrt(
                    np.cov(arr_compressed, aweights=weights_compressed, ddof=0)
                )
            else:
                out_vals["std"] = np.sqrt(np.cov(arr_compressed, ddof=0))
        if "min" in _output:
            out_vals["min"] = arr_compressed.min()
        if "max" in _output:
            out_vals["max"] = arr_compressed.max()
        if "sum" in _output:
            out_vals["sum"] = arr_compressed.sum()
        if "median" in _output:
            out_vals["median"] = np.ma.median(arr_compressed)
        if "count" in _output:
            out_vals["count"] = int((~_arr.mask).sum())
        if "weight_sum" in _output and weights is not None:
            out_vals["weight_sum"] = (
                np.ma.array(weights, mask=_arr.mask).compressed().sum()
            )

        return {k: v.item() for k, v in out_vals.items()}

    def arr_classes_count(self, arr, cls_def, weights=None, border_include="min"):
        """
        Count pixel values in an array that fall within specified value ranges (classes).

        :param arr: Input NumPy array (masked array supported).
        :param cls_def: List of dictionaries defining class ranges with 'min' and 'max' keys.
        :param weights: Optional weights to apply to each pixel value.
        :param border_include: How to include range boundaries ('min', 'max', 'both', or None).
        :return: List of class definitions expanded with pixel counts.
        """
        _weights = weights if weights is not None else 1
        cls_out = []
        for cls in cls_def:
            if border_include == "min":
                cls["val_count"] = np.sum(
                    np.logical_and(arr >= cls["min"], arr < cls["max"]) * _weights
                )
            elif border_include == "max":
                cls["val_count"] = np.sum(
                    np.logical_and(arr > cls["min"], arr <= cls["max"]) * _weights
                )
            elif border_include == "both":
                cls["val_count"] = np.sum(
                    np.logical_and(arr >= cls["min"], arr <= cls["max"]) * _weights
                )
            else:
                cls["val_count"] = np.sum(
                    np.logical_and(arr > cls["min"], arr < cls["max"]) * _weights
                )
            cls_out.append(cls)
        return cls_out

    ###########################
    # Raster Operations       #
    ###########################
    def read_masked(self, ds, mask, indexes=None, window=None, use_pixels="CENTER"):
        """
        Read raster data as a masked NumPy array based on an input geometry mask.

        :param ds: Path to raster file or an opened rasterio dataset.
        :param mask: Geometry used for masking (GeoJSON-like or Shapely geometry).
        :param indexes: Specific band(s) to read from the raster.
        :param window: Optional raster window to read a subset of data.
        :param use_pixels: Defines which pixels to include when masking ('CENTER', 'ALL', 'CONTAINED').
        :return: NumPy masked array with the data read from the raster.
        """
        dataset = ds if isinstance(ds, rasterio.DatasetReader) else rasterio.open(ds)
        mask_all_touched = use_pixels.upper() != "CENTER"
        _window = window or rasterio.features.geometry_window(dataset, shapes=[mask])
        source = dataset.read(indexes, window=_window)

        if 0 in source.shape:
            return source

        out_shape = source.shape[-2:]
        out_transform = dataset.window_transform(_window)
        input_geom_mask = rasterio.features.geometry_mask(
            [mask],
            transform=out_transform,
            invert=False,
            out_shape=out_shape,
            all_touched=mask_all_touched,
        )
        return np.ma.array(source, mask=input_geom_mask)

    def get_common_bounds_and_shape(self, geom, ds_list):
        """
        Compute common raster bounds and shape for multiple raster datasets.

        :param geom: Input geometry (GeoJSON-like or Shapely geometry).
        :param ds_list: List of raster file paths or opened raster datasets.
        :return: Tuple containing unified bounds and shape (rows, columns).
        """
        max_res_ds = min_res_bounds = None
        for ds in ds_list:
            dataset = (
                ds if isinstance(ds, rasterio.DatasetReader) else rasterio.open(ds)
            )
            ds_window = rasterio.features.geometry_window(dataset, shapes=[geom])
            if not max_res_ds or rasterio.windows.shape(
                ds_window
            ) > rasterio.windows.shape(ds_window):
                max_res_ds = dataset
                min_res_bounds = dataset.window_bounds(ds_window)
        out_bounds = max_res_ds.window_bounds(rasterio.windows.Window(*min_res_bounds))
        return out_bounds, rasterio.windows.shape(rasterio.windows.Window(*out_bounds))

    ###########################
    # Main Functionality      #
    ###########################
    def geom_extract(
        self,
        geometry,
        indicator,
        stats_out=("mean", "std", "min", "max", "sum", "counts"),
        afi=None,
        classification=None,
    ):
        """
        Extract raster statistics for a given geometry.

        :param geometry: Input geometry (GeoJSON-like or Shapely geometry).
        :param indicator: Path to raster file or opened raster dataset.
        :param stats_out: List of statistics to compute (e.g., 'mean', 'max', etc.).
        :param afi: Optional path to a weight raster.
        :param classification: Optional class definitions for class-based counts.
        :return: Dictionary with extracted statistics and class-based counts.
        """
        output = {}
        indicator_ds = (
            indicator
            if isinstance(indicator, rasterio.DatasetReader)
            else rasterio.open(indicator)
        )
        rasters_list = [indicator_ds] + ([rasterio.open(afi)] if afi else [])

        try:
            read_bounds, read_shape = self.get_common_bounds_and_shape(
                geometry, rasters_list
            )
        except Exception as e:
            if self.suppress_errors:
                log.warning("Skipping extraction! Geometry has no intersection.")
                return
            raise UnableToExtractStats(str(e))

        indicator_arr = self.read_masked(
            indicator_ds,
            mask=geometry,
            window=indicator_ds.window(*read_bounds),
            use_pixels="CENTER",
        )
        if np.all(indicator_arr.mask):
            if self.suppress_errors:
                log.warning(
                    f"Skipping extraction! No pixels caught by geometry: {geometry}"
                )
                return
            raise UnableToExtractStats(f"No pixels caught by geometry: {geometry}")

        if any(k in stats_out for k in ("min", "max", "mean", "sum", "std")):
            output["stats"] = self.arr_stats(indicator_arr)
        if classification:
            cls_res = self.arr_classes_count(indicator_arr, classification["borders"])
            output["classification"] = {"values": [cls["val_count"] for cls in cls_res]}
        return output

    ###########################
    # Multiprocessing Utility #
    ###########################
    def process_shapefile(
        self,
        shapefile_path,
        raster_file,
        stats_out=("mean", "min", "max", "sum"),
        afi=None,
        classification=None,
        num_workers=4,
    ):
        """
        Process a shapefile with multiple geometries and extract raster statistics in parallel.

        :param shapefile_path: Path to the input shapefile.
        :param raster_file: Path to the raster file.
        :param stats_out: List of statistics to compute.
        :param afi: Optional path to a weight raster.
        :param classification: Optional class definitions for class-based counts.
        :param num_workers: Number of worker processes for parallel execution.
        :return: List of results for each geometry.
        """
        results = []
        try:
            gdf = gpd.read_file(shapefile_path)
            if gdf.empty:
                raise ValueError("Shapefile contains no geometries.")
            geometries = [
                (geom.__geo_interface__, raster_file, stats_out, afi, classification)
                for geom in gdf.geometry
            ]

            if num_workers == 1:
                results = [self.geom_extract_parallel(*geom) for geom in geometries]
            else:
                with Pool(num_workers) as pool:
                    results = pool.starmap(self.geom_extract_parallel, geometries)
        except FileNotFoundError:
            log.error(f"Shapefile not found: {shapefile_path}")
            raise
        except ValueError as e:
            log.error(f"Error processing shapefile: {e}")
            raise
        return results

    def geom_extract_parallel(
        self, geometry, raster_file, stats_out, afi, classification
    ):
        """
        Wrapper for geom_extract to be used with multiprocessing.

        :param geometry: Input geometry.
        :param raster_file: Path to the raster file.
        :param stats_out: Statistics to compute.
        :param afi: Optional weight raster.
        :param classification: Optional class-based counts.
        :return: Extracted statistics or None if extraction fails.
        """
        try:
            return self.geom_extract(
                geometry, raster_file, stats_out, afi, classification
            )
        except UnableToExtractStats as e:
            log.warning(f"Extraction failed: {e}")
            return None
