TDM-Q
=====

General approach
----------------

 * we are mapping on the scale of Sardinia, we internally use
   EPSG:3003 (Monte Mario) as reference system and all geographic
   measures are in meter in that reference system.
 * all objects are timeseries with annotations:
 * a timeseries is a collection of snapshots:
   * each snapshot has a timestamp and a geometrical footprint;
     * the geometrical footprint includes also some sort of error
       characterization (a single positive float (res. in meters), in
       the simplest case)
   * plus annotations and provenance information;
   * a geometrical footprint can go from a point to a volume, a
     special case of a geometrical footprint is a polyline, this will
     be used to describe trajectories (f
 * use timescaledb + postgis to hold ghosts of the datasets;
 * one-shot events are, e.g., a car accidents are considered length 1 timeseries.
 * objects are divided in classes:
   * a class defines a class of sensors
     * superclass/category (e.g., meteo_sensor)
     * geometry type and precision
     * event data structure
 * a specific object is an instance of one of the defined classes,
   * it has a name and an unique id
   * we can query the system to get all the objects contained in a
     given space-temporal box with possible selectors on sensor type
     and, possibly, relevant shortcuts, the system will return a list
     of handlers that point to the specific resources selected.
   

Query interface
---------------



   


Datacube query interface
------------------------

latitude = ( 4.5217, 4.5925)
longitude = (-71.7926, -71.6944)
product_class = "l7"
product_instance = "ledaps_meta_river"
ingestion_timestamp = xxxx

data = dc.load(latitude=latitude, longitude=longitude, product_class=,
               product_instance=,
               measurements = ['red', 'nir', 'pixel_qa'])

this will return a list of xarray(s)

use case sensor trace

dimensions  (latitude: 


with dims
print( gpm_data )

<xarray.Dataset>
Dimensions:               (latitude: 3, longitude: 3, time: 366)
Coordinates:
  * time                  (time) datetime64[ns] 2015-01-01T11:59:59.500000 ...
  * latitude              (latitude) float64 12.95 12.85 12.75
  * longitude             (longitude) float64 14.25 14.35 14.45

Data variables:
    total_precipitation   (time, latitude, longitude) int32 0 0 0 0 0 0 0 0 ...
    liquid_precipitation  (time, latitude, longitude) int32 0 0 0 0 0 0 0 0 ...
    ice_precipitation     (time, latitude, longitude) int32 0 0 0 0 0 0 0 0 ...
    percent_liquid        (time, latitude, longitude) uint8 15 15 15 15 15 ...
Attributes:
    crs:      EPSG:4326


 
