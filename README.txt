WeatherViz
---------------------------------------------------------

XML Weather data visualization program

Hannu Ranta

Requirements
---------------------------------------------------------

Python 3.2

Java

Web browser with SVG-support (PNG-fallback mode for older browsers)

Usage
---------------------------------------------------------

Files names to read and write are defined in config.ini file.
First line tells the name of XML-input file. Sample files can
be found from repository. Second line is the language option 
(not implemented yet). Last lines defines the names of output 
files. 

All generated pages use same css-stylesheet. 
If you want to customize the look, modify stylesheet.

Other Info
---------------------------------------------------------

Program uses Java-based library called batik to convert generated 
SVG-images to PNG. This is done because older browsers can't open SVG-files.

Batik is part of Apache project

Website: http://xmlgraphics.apache.org/batik/index.html

License: http://xmlgraphics.apache.org/batik/license.html
