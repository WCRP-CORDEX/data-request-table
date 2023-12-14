# CORDEX-CMIP6 data request

This repository contains a CORDEX-CMIP6 data request table that is used to create [CORDEX-CMIP6 cmor tables](https://github.com/WCRP-CORDEX/cordex-cmip6-cmor-tables).

## Introduction [^1]

[^1]: from https://docs.google.com/document/d/1qX6tF26jPY1IYRVZQ00FLSU7AY4hZJoC.

The CORDEX-CMIP6 Data Request (DR) is a simplified analog of the CMIP6 Data Request for global models and defines all the quantities from CMIP6-driven CORDEX simulations that should be archived. The CORDEX-CMIP6 DR includes a number of Variable Lists (VLs) specifying output from different components (e.g. Atmosphere, Ocean, Aerosol, Land, Sea Ice, Rivers, etc.) of Regional Climate Models (RCMs). This document provides details on i) how to select output variables and their output intervals from the CORDEX-CMIP6 Variable Lists and ii) how to archive a number of specific variables.

* Currently, only the CORDEX-CMIP6 Atmosphere VL is included and VLs for other RCM components will be added when available.
* The CORDEX-CMIP6 VLs provide information about what variables are to be archived, their output frequency, temporal aggregation, units, standard and long names. Detailed metadata for each variable (variable attributes in netcdf files) will be provided in so called Climate Model Output Rewriter (CMOR) tables when available. The format of the CORDEX-CMIP6 CMOR tables is supposed to be the same as for the [CMIP6 CMOR tables](https://github.com/PCMDI/cmip6-cmor-tables).
* If you find any errors or typos in the CORDEX-CMIP6 Atmosphere VL, please report them to datasupport@cordex.org.

### Atmosphere Variable List
#### CORE, Tier1 and Tier 2 Variables

The CORDEX-CMIP6 Atmosphere VL includes three classes of data, namely: CORE (mandatory), Tier 1 (strongly recommended) and Tier 2 (optional). The CORE set contains the 15 most popular variables and the two most common static fields (orography and land area fraction). The selection of these 15 variables is based on statistics of data downloads from the Earth System Grid Federation (ESGF) and the needs of impacts, adaptation and vulnerability (VIA) studies. CORE is considered the minimum dataset to be provided by all CORDEX modeling groups running simulations for any of the 14 continental-scale CORDEX domains. The Tier 1 set includes common variables that are strongly recommended to provide. However, the selection of a subset of the Tier 1 variables is also possible and it is up to the regional CORDEX communities to decide on what Tier 1 variables they need for a specific CORDEX domain. Variables that can be calculated by different methods and are not consistent across RCMs or requested for one of the 14 CORDEX domains are included in the Tier 2 set. Similar to Tier 1 it is up to the regional CORDEX communities to decide what Tier 2 variables should be archived for a specific CORDEX domain.

#### Subdaily output
There is a growing demand for high-frequency subdaily RCM output, especially for impact applications, and moving to higher output frequency is a common tendency in the climate modeling community. All variables in CORE and a number of variables in Tier 1 and Tier 2 should be archived at 1-hr frequency. It is clear that archiving hourly RCM output requires a lot of disk space and there are reasonable concerns that it can be difficult for some RCM groups with limited capacities. Considering these concerns and also keeping wide involvement of individual RCM groups in CORDEX-CMIP6, subdaily output for CORE, Tier 1 and Tier 2 (both 6- and 1-hr) is not defined as mandatory. Any RCM group can provide only daily and monthly means, even for the CORE variables, if they are unable to provide hourly data.

#### Pressure levels
Requesting only three pressure levels (850, 500 and 200hPa) in CORDEX-CMIP5 has seriously limited analysis and usability of the CORDEX-CMIP5-driven simulations. The number of pressure levels is extended in CORDEX-CMIP6 and Tier 1 includes 10 pressure levels that are recommended to be provided (1000, 925, 850, 700, 600, 500, 400, 300, 250, 200hPa). A number of additional pressure levels that are either requested by one of the 14 CORDEX domains or are levels above 200hPa are included in Tier 2.
Default subdaily output frequency for pressure levels is 6 hourly and there are a number of requests to provide higher-frequency subdaily output (3- or even 1-hr) for a subset of the pressure levels defined in Tier 1 for specific studies and applications.
It is recommended that 6-hr pressure levels be provided as a minimum. If 3- or 1-hr output on pressure levels is needed, these frequencies can be provided as additional datasets with the standard 6-hr output. Such an approach leads to some duplication of output to be archived but keeps a consistent 6-hr output for all RCM groups. It is strongly recommended to coordinate the higher-frequency output on pressure levels within the CORDEX domains (i.e. what pressure levels and how many RCM groups are able to provide them).

#### Height levels
A number of new variables at different heights are defined in CORDEX-CMIP6. They include zonal and meridional winds at 50, 100, 150, 200, 250 and 300 m (for wind energy applications) and temperature and specific humidity at 50 m (for urban modeling applications, Tier 1). The selection of heights for wind energy applications may depend on a specific CORDEX domain and the 3 most commonly recommended heights (50, 100 and 150 m) are included in Tier 1. 200, 250 and 300 m that potentially can be used for high altitude systems are defined in Tier 2. It is up to the regional CORDEX communities to define what heights they need after consultations with impact modeling communities in their regions.

#### Zonal and meridional winds
Zonal and meridional winds have to be provided as real north- and eastward winds if a RCM uses coordinate system/projection that does not coincide with real north- and eastward directions (e.g. the rotated pole, Lambert Conformal, etc.).

#### Maximum/minimum values and averaging
Maximum/minimum values (tasmax, tasmin, sfcWindmax and wsgsmax) are defined as the maximum/minimum from all integrated time steps per day. Daily Maximum Hourly Precipitation Rate (prhmax) is defined as the maximum of the precipitation rate averaged over the whole hour. Daily output is an average of subdaily output with exception of maximum/minimum variables (tasmax, tasmin, sfcWindmax, prhmax and wsgsmax) and accumulated sunshine duration (sund). Monthly output for all variables is an average of daily values.
