# README
### Cultivable Lands(CL) and Permaculture.

This repository contains all the steps to make the analysis of the UN data concerning Lands Distributions, specifically for Cultivables Lands.

The main file is <b>'Abstract.md'</b>, which expose the analysis and the correspondant conclusions, and the links to the source codes related to each figure.

Additionally, there are files with the source code for ordering, cleaning and processing the original data, in order to obtain a proper database to be used for the further analysis.

### Repository Scheme:
* <b>Lands</b>
  - Abstract.md: graphic analysis and conclusions.
  - code_data<br>
    - I_data_process_inspection.ipynb: download, inspect and format the UN data in order to merge it with the geopandas and Cartopy library.<br>
    - II_data_merge_fill.ipynb: inspect, fill and filter the empty records from the dataframe previously obtained.<br>
    - III_data_create_indicators.ipynb: generate the indicators created for this project.<br>
    - additional_data_records: merge the Cartopy library with the Geopandas one, in order to obtain the name of the Geographic Region of each country.<br>
  - code_images (images source code)
    - CL.ipynb
    - country_pie.ipynb
    - desc_table.ipynb
    - ha_ref_w.ipynb
    - hist_dens.ipynb
    - hist_dens_CL.ipynb
    - HpF_bars_w.ipynb
    - org_table.ipynb
    - squari_dist.ipynb
    - world_map_w.ipynb
  - images (.png images used in the Abstract.md, obtained in the last section)
    - c_pie.png
    - CL.png
    - desc_table.png
    - example_fam.png
    - ha_ref_w.png
    - hist_dens.png
    - hist_dens_CL.png
    - HpF_bars_w.png
    - org_table.png
    - PI.png
    - ref_hdens.png
    - squari_dist.png
    - world_map_w.png
  - data
    - Main statictic data from the UN databases. ('https://data.un.org/')
      - SYB62_145_201904_Land.csv
    - DataFrames Generated:
      - countries_ref.csv
      - country_ref.csv
      - l_simple.csv
      - l_simple_mod.csv
      - ldown_c.csv
      - over_landun.csv
      - over_world.csv
      - reg_world.csv
      - rworld_miss.csv
      - rworld_miss_mod.csv
      - w_land.csv
      - wl.csv
      - wlands.csv
   
  - Readme



