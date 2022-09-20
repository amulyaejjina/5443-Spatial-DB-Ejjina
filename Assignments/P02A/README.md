

##  Part 1 of Project2 - Data Setup
### Loading tables with data and creating index on geometry column

#### Used shp2pgsql to create tables with data :

    shp2pgsql -s 4326 -I INPUTSHAPEFILE.shp TABLENAME| psql -d DATABASENAME -U USERNAME

#### For Data files, go to respective links to downaload them -

|   #   | Data | Link |
| :---: | ----------- | ---------------------- |
|    1  |     Airports       |  https://cs.msutexas.edu/~griffin/data/Airport_and_Plane_Data/airports.csv|
|2|  Primary US Roads  |https://www2.census.gov/geo/tiger/TIGER2019/PRIMARYROADS/tl_2019_us_primaryroads.zip|
|3|  US Rail Roads  |http://www2.census.gov/geo/tiger/TIGER2019/RAILS/tl_2019_us_rails.zip|
|4|  States  |https://www2.census.gov/geo/tiger/TIGER2021/STATE/tl_2021_us_state.zip|
|5|  Military Bases  |https://www2.census.gov/geo/tiger/TIGER2021/MIL/tl_2021_us_mil.zip|
|6|  Time Zones  |https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_time_zones.zip|
