# -----------------------------------------------------------
# Copyright (C) 2023 CryoLab CUHK
# -----------------------------------------------------------
import os
import inspect
import sys

# Ensure PROJ database is discoverable for pyproj/rasterio inside QGIS
_env_gdal = os.path.join(sys.prefix, "share", "gdal")
_proj_candidates = [
    os.path.join(sys.prefix, "lib", "python3.9", "site-packages", "rasterio", "proj_data"),
    os.path.join(sys.prefix, "lib", "python3.12", "site-packages", "rasterio", "proj_data"),
    os.path.join(sys.prefix, "share", "proj"),
]
_env_proj = next((p for p in _proj_candidates if os.path.exists(os.path.join(p, "proj.db"))), None)

if _env_proj:
    os.environ.setdefault("PROJ_LIB", _env_proj)
    os.environ.setdefault("PROJ_DATA", _env_proj)
os.environ.setdefault("GDAL_DATA", _env_gdal)

# Harden by explicitly pointing pyproj/rasterio to the data dir if available
try:
    import pyproj
    try:
        from pyproj import datadir as _pyproj_datadir
        if _env_proj:
            _pyproj_datadir.set_data_dir(_env_proj)
    except Exception:
        pass
except Exception:
    pass

try:
    import rasterio
    try:
        from rasterio import env as _rio_env
        if _env_proj:
            _rio_env.set_proj_data_search_path(_env_proj)
    except Exception:
        pass
except Exception:
    pass

from .geo_sam_tool import Geo_SAM

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]


def classFactory(iface):
    return Geo_SAM(iface, cmd_folder)
