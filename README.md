# gsrm-cold-points-2025
Code used in Nugent et al., revised manuscript under review at _Earth and Space Science_ (original preprint [doi:10.22541/essoar.172405869.95851202/v1](https://doi.org/10.22541/essoar.172405869.95851202/v1), August 2024), on the role of cold point-overshooting convection and lofting of cirrus near the cold point on influencing the height and temperature of the cold point tropopause in global storm-resolving models (GSRMs). 

Please note that relative and absolute file paths within the scripts and Jupyter notebooks listed below may have changed since they were last run. 

## Data Processing
(Pre)processing and preliminary analysis needed for the DYAMOND2 output, ERA5 reanalysis, and DARDAR observations.
### DYAMOND2
* ...
### ERA5
* ...
### DARDAR
* ...

## Helper Scripts
* (get d2)
* (split_soundings)

## Figures
# TODO: change so it points to notebook for plotting (not the figure) and only include data processing notes (no "plotted in")
# --> ALSO change figure names to "Fig1_xxx", etc.
Scripts needed to generate the figures used in the paper. Also includes processing of the QBO/ENSO index data and the IGRA sounding data.
* **Figure 1**: tropics_map_with_soundings_with_labels.png
	* Plotted in tropics_map_d2.ipynb
* **Figure 2**: EIGSSS_UTLS_temp_profiles_all_regions.png
	* IGRA data stored in igra_sounding_data/
		* Originally downloaded from [Wyoming Weather Web](https://weather.uwyo.edu/upperair/sounding.html) (last accessed March 2025)
		* Processed in soundings_cold_points.ipynb
	* Plotted in 10x10_UTLS_temp_profiles.ipynb
* **Figure 3**: ErIcGeSaScSh_time_avg_cold_point_height_ITCZ.png and ErIcGeSaScSh_time_avg_cold_point_temp_ITCZ.png
	* Time averages calculated & plotted in time_avg_cold_point_maps.ipynb
* **Figures 4-5, S2-S3**: ObShGeSc_qtot_bin_freq_binned_by_Tb-Tcp_SPC.png, ObShGeSc_qtot_conv_bin_freq_binned_by_Tb-Tcp_SPC_obs_instr_25e-4.png, ObShGeSc_qtot_bin_freq_binned_by_Tb-Tcp_AMZ.png, ObShGeSc_qtot_conv_bin_freq_binned_by_Tb-Tcp_AMZ_obs_instr_25e-4.png
	* Observations: 
		* Big observation regions binned using analysis from Nugent and Bretherton (2023), *GRL*; see the relevant notebooks from [Figs. 1, 2, S2, and S3 in that repository](https://github.com/jacnugent/tropical-conv-os-2023/tree/main?tab=readme-ov-file#figures-1-2-s2-and-s3)
	* GSRMs:
		* Tb-Tcp differences binned in d2_tb-tcp_hist.ipynb
		* Frozen water binned in binned_by_diffs_d2.sh
	* Plotted in d2_binned_plots_match_obs.ipynb
* **Figures 6-7, S4-S5**: OIGSSS_joint_hist_SCA.png, OIGSSS_joint_hist_TIM.png, OIGSSS_joint_hist_AMZ.png, OIGSSS_joint_hist_SPC.png
	* Observation histograms computed in get_Tb-cpT_hist_d2.sh 
	* GSRM histograms computed and ALL plotted in d2_joint_Tb-cpT_histograms.ipynb
* **Figure 8**: OIGSSS_paper_FREQ_with_cbar_os_heatmaps_coarse_single_col.png
	* Overshooting convection frequencies calculated in d2_calc_os_counts.ipynb
	* Plotted in d2_paper_coarsened_heatmaps_os_ci.ipynb
* **Figures 9-10**: OIGSSS_cold_point_cirrus_hists_with_fractions_AMZ.png and OIGSSS_cold_point_cirrus_hists_with_fractions_SPC.png
	* Cold point-relative cloud ice calculated & histograms plotted in d2_cirrus_histograms.ipynb
* **Figure 11**: OIGSSS_paper_FREQ_with_cbar_ci_heatmaps_coarse_single_col.png
	* Cirrus frequencies and 5x5 cell counts calculated in d2_cirrus_heatmaps.ipynb
	* Plotted in d2_paper_coarsened_heatmaps_os_ci.ipynb
*  **Figure S1**: QBO_ENSO_indices_ts.png
	* Data downloaded from NOAA Physical Sciences Laboratory (all links last accessed March 2025): 
		* [Nino 3.4 SST Index from NOAA ERSST V5](https://psl.noaa.gov/data/timeseries/month/DS/Nino34_CPC/)
		* [Quasi-Biennial Oscillation (QBO) 50 mb](https://psl.noaa.gov/data/timeseries/month/DS/QBO50/)
	* Plotted in d2_enso_qbo_ts.ipynb 
