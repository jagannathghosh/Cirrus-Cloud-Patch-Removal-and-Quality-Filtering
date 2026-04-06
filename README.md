📂 Data Used
IMERG precipitation data (NetCDF)
Cloud Top Pressure (CTP) and Cloud Top Height (CTH) data
Shapefile for regional masking

⚠️ Data is not included due to large file size

⚙️ Methodology
1. Spatial Masking

A shapefile of the study region was used to create a polygon mask. This mask was applied to gridded satellite data to retain only the region of interest.

2. Cirrus Cloud Patch Removal

I performed an additional quality control step by removing cirrus cloud patches from the dataset. Cirrus clouds are high-altitude clouds that are generally not associated with deep convection and therefore contribute little to no rainfall. Since this study focuses on extreme rainfall events and convective cloud behavior, the inclusion of cirrus clouds would introduce noise and reduce the accuracy of the analysis. Hence, cirrus cloud patches were removed to ensure that only convective cloud regions were retained for further investigation.

Cirrus clouds are typically characterized by low Cloud Top Pressure (CTP) values (generally < 250 hPa). To eliminate these regions, a threshold-based masking approach was applied using a conditional filter:

CTP_filtered = np.where(CTP < 250, NaN, CTP)

This step effectively excluded cirrus cloud patches from the dataset.

3. Consistent Masking for Cloud Height

The same mask derived from filtered CTP was applied to the corresponding Cloud Top Height (CTH) variables to ensure consistency in analysis.

4. Precipitation Aggregation

IMERG precipitation data from multiple time steps (00Z–21Z) were aggregated to compute daily rainfall totals.

5. Time Series Analysis

Daily spatial mean precipitation was calculated and visualized to analyze temporal variability.

6. Monthly Averaging

After preprocessing, monthly area-averaged values were computed for June, July, August, and September (JJAS) over the period 2000–2024.



📦 Requirements

Install dependencies using:

pip install -r requirements.txt

Libraries used:

numpy
matplotlib
netCDF4
scipy
geopandas
shapely
xarray
