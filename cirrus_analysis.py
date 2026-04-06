import geopandas as gpd
import numpy as np
from shapely.geometry import Point
shapefile_path = r"D:\MS Thesis\North Coastal\NC_Shape\NC_Orissa.shp"
gdf = gpd.read_file(shapefile_path)
polygon = gdf.union_all()
lon2d, lat2d = np.meshgrid(new_lon, new_lat)
points = [Point(x, y) for x, y in zip(lon2d.ravel(), lat2d.ravel())]
mask = np.array([polygon.contains(pt) for pt in points], dtype=bool)
mask = mask.reshape(lat2d.shape)
print(f"Mask shape: {mask.shape}")
all_vars = list(globals().keys())
for varname in all_vars:
    if varname.endswith("_regrid") or varname.startswith("CTP_"):
        arr = globals()[varname]
        print(f"Processing {varname} with shape {arr.shape}")
        if arr.shape != mask.shape:
            print(f"Shape mismatch for {varname}: {arr.shape} vs mask {mask.shape}")
            continue
        arr_masked = np.where(mask, arr, np.nan)
        newname = varname.replace("CTP_", "NC_CTP_").replace("CTH_", "NC_CTH_")
        globals()[newname] = arr_masked
print("✅ Masking complete. New variables NC_CTP_YYYY_MM and NC_CTH_YYYY_MM created.")


#############################################################
import numpy as np
workspace_vars = list(globals().items())
for var_name, var_data in workspace_vars:
    if var_name.startswith("NC_CTP_") and isinstance(var_data, np.ndarray):
        masked_array = np.where(var_data < 250, np.nan, var_data)       
        new_name = var_name.replace("NC_CTP_", "NC_CTP_") + "_LIM"
        globals()[new_name] = masked_array
        print(f"✅ Threshold applied: {var_name} → {new_name}")
        
################### apply the SAME spatial mask derived from CTP (<250 hPa) to the CTH variables,        
import numpy as np
workspace_vars = dict(globals())
for var_name, var_data in workspace_vars.items():
    if var_name.startswith("NC_CTH_") and isinstance(var_data, np.ndarray):
        ctp_lim_name = var_name.replace("NC_CTH_", "NC_CTP_") + "_LIM"
        if ctp_lim_name in workspace_vars:
            masked_cth = np.where(np.isnan(workspace_vars[ctp_lim_name]), np.nan, var_data)
            globals()[var_name + "_LIM"] = masked_cth
            print(f"✅ CTH masked: {var_name} → {var_name}_LIM")
        else:
            print(f"⚠️ Missing CTP mask for {var_name}")