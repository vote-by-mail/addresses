# addresses
This repo pulls a list of distributed US addresses and bulk geocodes them.

## Churches
[Church Finder](https://www.churchfinder.com/churches) provides a large list of addresses of churches throughout the country

## Nominatim
For goecoding.  We actually build our own nominatim server to handle the bulk geocodes.

1. Download the US file from http://download.geofabrik.de/north-america.html
2. Perform a `docker pull mediagis/nominatim`
3. Follow the instructions here https://hub.docker.com/r/mediagis/nominatim/ to initialize and start the server
