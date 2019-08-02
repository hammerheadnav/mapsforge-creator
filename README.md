
# mapsforge-creator

Automatic generation for Mapsforge maps and pois (based on our [guide](https://github.com/mapsforge/mapsforge/blob/master/docs/MapCreation.md)). The scripts download OpenStreetMap data from [Geofabrik](http://download.geofabrik.de/) and land polygons from [OpenStreetMap Data](https://osmdata.openstreetmap.de/).

Requirements are working installations of: 
- [GDAL](http://gdal.org/)
- [Java](https://www.java.com/)
- [Perl](https://www.perl.org/
- [Python 2.x](https://www.python.org/) with GDAL.
- [Osmosis](http://wiki.openstreetmap.org/wiki/Osmosis) installation.
- Download the **map-writer** and **poi-writer** plugins (**jar-with-dependencies**), either their release version from [Maven Central](https://search.maven.org/search?q=g:org.mapsforge) or their snapshot version from [Sonatype OSS Repository Hosting](https://oss.sonatype.org/content/repositories/snapshots/org/mapsforge/). See the Osmosis [documentation]. (http://wiki.openstreetmap.org/wiki/Osmosis/Detailed_Usage#Plugin_Tasks) for how to properly install them.

## Hammerhead Specifics

map-creator (and variants listed below) require a buffer size to be specified for each region. This is a buffer around the boundign box of the region.poly file downloaded from Geofabrik. The buffer size was fixed at 0.1 degrees in the origin map-creator scripts. Now it is a required argument to the perl script that computes the bounding box as well as to map-creator (and variants). This is a workaround to a bug where converting the clipped land polygons from shapefiles to OSM files sometimes removes rectangular (tile boundaries?) regions of the land polygon. Altering the buffer size can allow it to work properly.

**map-creator**: Primary script used to create a Mapsforge map for a single region. Cleans up/removes temporary data.

- Usage: ./map-creator continent/country[/region] buffer_size ram|hd [lang,...]
- Example: ./map-creator europe/germany/berlin 0.1 ram en,de,fr,es

Two addition scripts have been added to more easily create data locally (outside of automated AWS scripts):

**single-map-creator**: This will build a Mapsforge map file for a single Geofabrik region. The primary difference from map-creator is that this script will not delete the temporary data and will check if the OSM regions has been downloaded previously (similar to how map-creator checks for presence of land polygons). This will allow for successive runs without downloading from OSM each time.

- Usage: ./single-map-creator continent/country[/region] buffer_size ram|hd [lang,...]
- Example: ./single-map-creator europe/germany/berlin 0.1 ram en,de,fr,es

**bounded-map-creator**: This script downloads a full region and clips it to a specified bounding box. This is needed for regions that are not separate Geofabrik regions (e.g. Bahamas, Bermuda, Caribbean islands, South pacific Islands).

- Usage: ./bounded-map-creator continent country minlon minlat maxlon maxlat centerlon centerlat ram|hd [lang,...]
- Example: ./bounded-map-creator central-america bahamas -79.0 20.0 -70.0 27.0 -74.5 23.5 ram en,de,fr,es

Each of these scripts has config specifications in `# Configuration` section at the top. Adjust them to your environment: Osmosis home, data path, output paths, variable tag values etc. Or you can set externally the relevant variables.

## Dependencies and Setup

Requires osmosis and GDAL. On Ubuntu the following can be run to set this up:

```bash
apt-get update
apt-get install -y wget git zip software-properties-common default-jdk
add-apt-repository -y ppa:ubuntugis/ppa
apt update
apt install -y gdal-bin python-gdal
```

For osmosis:
```bash
wget https://bretth.dev.openstreetmap.org/osmosis-build/osmosis-latest.tgz
mkdir osmosis
mv osmosis-latest.tgz osmosis
cd osmosis
tar xvfz osmosis-latest.tgz
rm osmosis-latest.tgz
chmod a+x bin/osmosis
```

Within map-creator or variant scripts the OSMOSIS_HOME variable must be hanged to point to the directory where osmosis resides.

The last step in the setup is to add the Mapsforge writers to osmosis:
```bash
cd osmosis/lib/default/
wget https://search.maven.org/remotecontent?filepath=org/mapsforge/mapsforge-poi-writer/0.10.0/mapsforge-poi-writer-0.10.0-jar-with-dependencies.jar
wget https://search.maven.org/remotecontent?filepath=org/mapsforge/mapsforge-map-writer/0.10.0/mapsforge-map-writer-0.10.0-jar-with-dependencies.jar
```

## Notes

**For the old process using planet.osm see [here](https://github.com/mapsforge/mapsforge-mapcreator).**

- You could increase the Java heap space that may be allocated for Osmosis. You can do so by editing the script `$OSMOSIS_HOME/bin/osmosis(.bat)` and insert a line with `JAVACMD_OPTIONS=-Xmx800m`. This sets the maximum available Java heap space to 800MB. Of course you can set this parameter to a value which fits best for your purpose.
