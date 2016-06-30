# OpenStreetMap Monitoring Tool for Python

This Tool provides several python scripts that can be used to download data from the OpenStreetMap API and analyse changes over time. The scripts can be used seperately, but there is also a version that combines all of them. In the following you will find some descriptions.

## Set up

Download the python scripts. Download osmosis-latest (http://bretth.dev.openstreetmap.org/osmosis-build/osmosis-latest.zip) unzip and copy to the same folder.

Further requirements: python libraries ogr and urllib2


## Analyse OSM contributions to Tasking Manager project every 15 Minutes

###run.py:
- example run: 'python run.py 1251'

Input:
- HOT Task id (e.g. '1251') Have a look at the Tasking Manager (http://tasks.hotosm.org/) for ongoing projects.

Output:
- OSM data for different timestamps, .osm files --> these files will be stored in a separate folder for each timestamp
- Changes between different timestamps, .osc files --> these files will be stored in the "output" folder
- statistics file with information on deleted, modified and created nodes and ways per time intervall, .txt file --> this file will be stored in the "output" folder
- statistics figures --> not implemented yet

Workflow:

1. First run:
  - download OSM data for timestep 1 --> uses get_tm_osm_data.py
  - merge single files for timestep 1 --> uses merge_osm_data.py
  - wait 15 minutes 

2. Second run and further runs:
  - download OSM data for timestep 2 (3,...) --> uses get_tm_osm_data.py
  - merge single files for timestep 2 (3,...) --> uses merge_osm_data.py
  - compare timestep 1 and timestep 2 (or timestep 2 and timestep 3,...) --> uses compare_osm_data.py
  - calculate statistics and add to statistics file --> uses get_diff_stats.py
  - wait 15 minutes, then start again with 2.1

Issues:
- you may change the waiting time (in seconds) at lines 60 and 106

## Description for individual scripts

### get_tm_osm_data.py:
- example run: python get_tm_osm_data.py 1251 D:/temp/osm_data

Input arguments:
- HOT Task id (e.g. '1251') Have a look at the Tasking Manager (http://tasks.hotosm.org/) for ongoing projects.
- output directory

Output:
- many .osm files within the output directory

Workflow:

1. downloads information about the Tasking Manager project
2. iterates over each tile in the Tasking Manager project
3. downloads all OSM data via the OpenStreetMap API given the bounding box for each tile

Issues:
- download from OpenStreetMap API may fail if the bounding box is too big
- download may take some time depending on the amount of data in OSM
- you can think about use cases where you are only interested in specific objects or object types: the overpass api is better suited for those scenarios

### merge_osm_data.py:
- example run: 'python merge_osm_data.py D:/temp/osm_data merge.osm osm'

Input arguments:
- input directory, e.g. D:/temp/osm_data
- output file name, e.g. merge.osm
- file extension, e.g. .osm for OSM file, .osc for OSM change files

Output
- merged OSM data into one file

Issues:
- uses the osmosis tool --> you need to have this tool in the same directory or point to the correct directory withing the script at lines 45 and 58

### compare_osm_data.py:
- example run: 'python compare_osm_data.py time1.osm time2.osm change.osc'

Input arguments:
- .osm file for first timestamp, e.g. time1.osm
- .osm file for second timestamp, the "new" one, e.g. time2.osm
- output file name with .osc extension --> OSM change files have the extension .osc

Output:
- difference between the two timestamps in .osc format --> this file can be easily visualized using JOSM (https://josm.openstreetmap.de/)
- contains information on created, modified and deleted OSM objects

Issues:
- uses the osmosis tool --> you need to have this tool in the same directory or point to the correct directory withing the script at line 12
- time1.osm and time2.osm should cover the same area, otherwise this analysis is quite meaningless

### get_diff_stats.py:
- example run: 'python get_diff_stats.py diff.osc D:/temp/osm_data'

Input arguments:
- .osc file that contains information on changes between two timestamps
- output directory, e.g. D:/temp/osm_data

Output:
- .txt file with information on number of created, modified and deleted OSM objects
- header: diff_file;nodes_created;nodes_modified;nodes_deleted;ways_created;ways_modified;ways_deleted;buildings_created;buildings_modified;buildings_deleted
- delimiter ';'






