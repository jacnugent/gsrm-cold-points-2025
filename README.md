# gsrm-cold-points-2025
[![DOI](https://zenodo.org/badge/703695983.svg)](https://doi.org/10.5281/zenodo.15048415)

Code used in Nugent et al., revised manuscript under review at _Earth and Space Science_ (original preprint [doi:10.22541/essoar.172405869.95851202/v1](https://doi.org/10.22541/essoar.172405869.95851202/v1), August 2024), on the role of cold point-overshooting convection and lofting of cirrus near the cold point on influencing the height and temperature of the cold point tropopause in global storm-resolving models (GSRMs). 

Please note that relative and absolute file paths within the scripts and Jupyter notebooks listed below, as well as the names of files and directories, may have changed since they were last run. These scripts and notebooks therefore may not run "out of the box."

## Data Processing
(Pre)processing and preliminary analysis needed for the DYAMOND2 output, ERA5 reanalysis, and DARDAR observations. Dates/regions/file paths in the processing scripts below should be changed as needed and script headers should be updated.
### DYAMOND2 ([shell_scripts/dyamond2](shell_scripts/dyamond2/))
DYAMOND2 (winter phase) output can be accessed by contacting ESiWACE; see instructions [here](https://www.esiwace.eu/the-project/past-phases/dyamond-initiative). Full descriptions of the models and their outputs are provided by DKRZ [here](https://easy.gems.dkrz.de/DYAMOND/Winter/index.html). In this study, the existing DYAMOND2 output from DKRZ was subset into 10°x10° and/or 30°S - 10°N regions, then processed further for analysis. See below for details on the scripts that should be run for each step. Note that all of these scripts were written to be submitted as batch jobs and need headers updated before running.
1. Subset 30°S - 10°N region from each model for temperature, height, w, frozen hydrometeors (ice/snow/graupel), humidity, and OLR (2d variable) and concatenate into one file per model & variable.
	* GEOS: geos_qiqg.sh, geos_qv.sh, geos_temp.sh, geos_zg.sh, geos_w.sh, sub_geos2d.sh, cat_geos.sh
	* SCREAM: get_scream_z.sh, scream_q.sh, scream_temp.sh, scream_w.sh, scream_qv.sh, subset_scream.sh, cat_scream.sh
	* ICON: icon_full_w.sh, icon_pres.sh, icon_qiv.sh, icon_temp.sh, icon_w.sh, subset_icon.sh, cat_icon.sh
	* gSAM: sam_full_w.sh, sam_qiv.sh, sam_temp.sh, sub_sam.sh, cat_sam.sh
	* X-SHiELD: subset_shield_3d.sh, subset_shield.sh, cat_shield.sh
2. Optional: run timesel_3d.sh to drop the first 10 days (spinup period) so file sizes are smaller.
3. Convert accumulated OLR to 15 min OLR in gSAM and ICON to match the other models: deltat_sam.sh, deltat_icon.sh
4. Subset global tropics files to the 10°x10° regions:
   	* 10x10_sub_shield.sh (X-SHiELD only)
   	* 10x10_subsets_gsri.sh (GEOS, SCREAM, and ICON)
   	* 10x10_subsets_ns.sh (gSAM only)
5. Remap the native grid temperature files to 0.25° to calculate the cold point: remapcon_geos.sh, remapcon_icon.sh, remapcon_sam.sh, remapcon_scream.sh, remapcon_shield.sh
6. Remap the 0.25° temperature files back to the native grid (so you have the same coarsened temperature value for all native grid points that fall within that 0.25°x0.25° box): remapnn_temp_025.sh. This is used to calculate the background cold point index at each native grid cell.
7. (After running time_avg_cold_point_maps.ipynb, where cold point files are saved):
	* Remap the cold point indices (0.25° resolution) onto the native grid: remapnn_cpT.sh
	* Subset the cold point indices for the 10°x10° regions: 10x10_subset_cp_inds.sh
8. Put the brightness temperature threshold for overshooting convection (i.e., the cold point temperature) onto the native grid: remapnn_tb_thresh_025.nc
### ERA5 ([shell_scripts/](shell_scripts/))
Run get_era5_ml.sh to download the model-level reanalysis data. Then run process_era5_ml_itcz.sh to get the temperature and geopotential height files as netcdfs. 
### DARDAR 
DARDAR data in this study was subset from the larger regions used in Nugent and Bretherton (2023), _GRL_. See the instructions in that repository [here](https://github.com/jacnugent/tropical-conv-os-2023/tree/main?tab=readme-ov-file#dardar). The larger 30°S - 10°N region was downloaded/processed using those same scripts. 
### MERGIR ([shell_scripts/](shell_scripts/))
Follow the "Subset/Get Data" link on the NCEP/CPC GPM_MERGIR page ([doi:10.5067/P4HZB9N27EKU](https://doi.org/10.5067/P4HZB9N27EKU)). Download links lists for each region/year and then run get_mergir.sh to download and concatenate files into one file per region. Then run get_mergir_3h.sh to resample the half hourly files every 3 hours. 

## Analaysis ([notebooks/](notebooks/)) and Figures ([plots/](plots/))
Scripts needed to generate the figures used in the paper. Also includes processing of the QBO/ENSO index data and the IGRA sounding data.
* **Figure 1**: tropics_map_d2.ipynb
* **Figure 2**: 10x10_UTLS_temp_profiles.ipynb
	* IGRA data stored in igra_sounding_data/; originally downloaded from [Wyoming Weather Web](https://weather.uwyo.edu/upperair/sounding.html) (last accessed March 2025) and processed in soundings_cold_points.ipynb.
* **Figure 3**: time_avg_cold_point_maps.ipynb
	* Time averages also calculated in time_avg_cold_point_maps.ipynb.
* **Figures 4-5, S2-S3**: d2_binned_plots_match_obs.ipynb
	* Observations: 
		* Big observation regions binned using analysis from Nugent and Bretherton (2023), *GRL*; see the relevant notebooks from [Figs. 1, 2, S2, and S3 in that repository](https://github.com/jacnugent/tropical-conv-os-2023/tree/main?tab=readme-ov-file#figures-1-2-s2-and-s3)
	* GSRMs:
		* Tb-Tcp differences binned in d2_tb-tcp_hist.ipynb
		* Frozen water binned in shell_scripts/bin_by_diffs_d2.sh
* **Figures 6-7, S4-S5**: d2_joint_Tb-cpT_histograms.ipynb
	* Observation histograms computed in shell_scripts/get_Tb-cpT_hist_d2.sh 
	* GSRM histograms also computed in d2_joint_Tb-cpT_histograms.ipynb
* **Figures 8, 11**: d2_paper_coarsened_heatmaps_os_ci.ipynb
	* Overshooting convection frequencies calculated in d2_calc_os_counts.ipynb
	* Cirrus frequencies and 5x5 cell counts calculated in d2_cirrus_heatmaps.ipynb
* **Figures 9-10**: d2_cirrus_histograms.ipynb
	* Cold point-relative cloud ice also calculated in d2_cirrus_histograms.ipynb.
*  **Figure S1**: d2_enso_qbo_ts.ipynb
	* Data downloaded from NOAA Physical Sciences Laboratory (all links last accessed March 2025): 
		* [Nino 3.4 SST Index from NOAA ERSST V5](https://psl.noaa.gov/data/timeseries/month/DS/Nino34_CPC/)
		* [Quasi-Biennial Oscillation (QBO) 50 mb](https://psl.noaa.gov/data/timeseries/month/DS/QBO50/)
* **Convective and "other stratospheric" cirrus fractions**: Calculated in d2_cirrus_fractions.ipynb.

## Other Files
### Python Scripts ([python_scripts/](python_scripts/))
* **split_soundings.py**: Split up a text file containing data from many soundings into individual files that can be read into python.
* **model_grid.py**: Read in arrays of coordinates of GSRM grids, calculate ICON height, etc.
* **get_d2_data.py**: Read in (already processed/subset) GSRM files for 10x10 regions.
* **biv_hist.py** and **biv_hist_d2.py**: Calculate bivariate histogram of Tb and Tcp for observations or GSRMs, respectively.
* **bin_overshoot.py** and **bin_obs_overshoot.py**: Bin a variable (ice, frozen water, effective radius, etc.) at cold point-relative levels by Tb-Tcp for GSRMs or observations, respectively.
* **bin_d2.py**: Make and save histogram files (for the binned plots) of ice/frozen water binned by Tb-Tcp for the GSRMs. Runs bin_overshoot.py.
* **calc_cold_point....py**: Calculates the number of time steps that each pixel/grid point has an ice mixing ratio above the radiatively-active threshold for a 1 km layer near the cold point. Separate scripts for GSRMs and observations (..._obs...) and for cold point +/- 1000m or cold point only (..._at_cp_only.py)
* **get_era5_climo_ml.py** and **compute_geopotential_on_ml.py**: Helper scripts to download and processes ERA5 reanalysis.
### Helper Jupyter Notebooks ([notebooks/helper/](notebooks/helper))
* **find_coords.ipynb**: Get .csv files of SCREAM coordinates.
* **get_model_vert_inds.ipynb**: Make SCREAM_est_height_12-20km.nc file.
### Pickle Files ([pickle_files/](pickle_files/))
Contains pickle files created, saved, and used in the notebooks and scripts for plotting outlined above as well as the colormap used in Figure 2. 
