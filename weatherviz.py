#================================================
#   WeatherViz - WeatherData visualization app                
#                               
#   Author: Hannu Ranta
#------------------------------------------------

#Library imports
import sys
import xml.etree.ElementTree as xml
from time import gmtime, strftime
from subprocess import *

print("----------------------")
print("WeatherViz")
print("Hannu Ranta")
print("----------------------")

#==================================================
# Read configuration file and XML
#==================================================
config = open('config.ini', 'r').read()
configdata = config.split('\n')

print("Found following configuration data:")
print(configdata)

tree = xml.parse(configdata[0])
doc = tree.getroot()

#==================================================
# Initialize variables
#==================================================

day = []
daytemp = []
nighttemp = []
rain = []

farenheitday = []
farenheitnight = []

fieldnames = ('Day', 'Day Temp (C)', 'Day Temp (F)', 'Night Temp (C)', 'Night Temp (F)', 'Rain (mm)', 'Rain (%)')

avgdayc = 0
avgdayf = 0

avgnightc = 0
avgnightf = 0

idcount = 0

Days = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

#==================================================
# Read data from XML
#==================================================

for weekday in tree.iter(tag='day'):
    day.append(int(weekday.text))

for weekday in tree.iter(tag='daytemp'):
    daytemp.append(float(weekday.text))

for weekday in tree.iter(tag='nighttemp'):
    nighttemp.append(float(weekday.text))

for weekday in tree.iter(tag='rain'):
    rain.append(float(weekday.text))

#==================================================
# Calc average temps, farenheits etc...
#==================================================

for i in daytemp:
    temp = "%.1f" % (float(i) * 1.8 + 32) 
    farenheitday.append(float(temp))

for i in nighttemp:
    temp = "%.1f" % (float(i) * 1.8 + 32) 
    farenheitnight.append(float(temp))

    avgdayc = (sum(daytemp)/len(daytemp))
    avgdayf = (sum(farenheitday)/len(farenheitday))
    avgnightc = (sum(nighttemp)/len(nighttemp))
    avgnightf = (sum(farenheitnight)/len(farenheitnight))

#-------------------------------------------------
# Debug-prints
#-------------------------------------------------
print (day[:])
print ("=======================")
print (daytemp[:])
print (farenheitday[:])
print ("=======================")
print (nighttemp[:])
print (farenheitnight[:])
print ("=======================")
print (rain[:])

#------------------------------------------------------------
# HTML Index page creation
#------------------------------------------------------------

print("Generating index called:")
print(configdata[2])

# HTML headers
index = open(configdata[2], 'w')
index.write('<!DOCTYPE html>')
index.write('<html>')
index.write('<head>')
index.write('<title>WeatherViz index</title>')
index.write('<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">')
index.write('<link href="weatherviz.css" rel="stylesheet" type="text/css" media="screen"/>')
index.write('</head>')
index.write('<body>')

# Main div
index.write('<div id="main-container">')
index.write('<h1>Graphical representation of XML-weatherdata</h1>')
index.write('<h2>Generated:'+strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())+'</h2>')
index.write('<p> Visualization is available in following views: </p>')

# Link list
index.write('<ul>')
index.write('<li><a href = "'+configdata[3]+'">Table view</a></li>')
index.write('<li><a href = "'+configdata[4]+".svg"'">Interactive view(SVG)</a></li>')
index.write('<li><a href = "'+configdata[4]+".png"'">Graphical view(PNG)</a></li>')
index.write('</ul>')

index.write('</br>')
index.write('<ul>')
index.write('<li><a href = "'+configdata[0]+'">Original XML</a></li>')
index.write('</ul>')

# HTML close tags
index.write('</div>')
index.write('</body>')
index.write('</html>')
index.close()

print("Index Generation completed")
print("--------------------------")

#------------------------------------------------------------
# HTML Table creation
#------------------------------------------------------------

print("Generating table called:")
print(configdata[3])

# HTML headers
table = open(configdata[3], 'w')
table.write('<!DOCTYPE html>')
table.write('<html>')
table.write('<head>')
table.write('<title>Weather data table</title>')
table.write('<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">')
table.write('<link href="weatherviz.css" rel="stylesheet" type="text/css" media="screen"/>')
table.write('</head>')
table.write('<body>')

table.write('<table id="table-def">')
table.write('<thead>')
table.write('<tr>')

# Table header fields
for i in range(len(fieldnames)):
        table.write('<th scope="col">' + fieldnames[i] + '</th>')

table.write('</tr>')
table.write('</thead>')
table.write('<tbody>')

# Data fields
for i in day:
        table.write('<tr>')

        # Print table to HTML file, even rows highlighted
        if i%2 == 0:
            table.write('<td class="even"><b>' + str(Days[i-1]) + '</b></td>')
            table.write('<td class="even">' + "%.1f" % (daytemp[i-1]) + '</td>')
            table.write('<td class="even">' + "%.1f" % (farenheitday[i-1]) + '</td>')
            table.write('<td class="even">' + "%.1f" % (nighttemp[i-1]) + '</td>')
            table.write('<td class="even">' + "%.1f" % (farenheitnight[i-1]) + '</td>')
            table.write('<td class="even">' + "%.1f" % (rain[i-1]) + '</td>')
            table.write('<td class="even">' + "%.1f" % ((rain[i-1]/sum(rain))*100) + '</td>')
        else:
            table.write('<td><b>' + str(Days[i-1]) + '</b></td>')
            table.write('<td>' + "%.1f" % (daytemp[i-1]) + '</td>')
            table.write('<td>' + "%.1f" % (farenheitday[i-1]) + '</td>')
            table.write('<td>' + "%.1f" % (nighttemp[i-1]) + '</td>')
            table.write('<td>' + "%.1f" % (farenheitnight[i-1]) + '</td>')
            table.write('<td>' + "%.1f" % (rain[i-1]) + '</td>')
            table.write('<td>' + "%.1f" % ((rain[i-1]/sum(rain))*100) + '</td>')
        table.write('</tr>')

# HTML close tags
table.write('</tbody>')
table.write('</table>')
table.write('<h2>Generated:'+strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())+'</h2>')
table.write('</body>')
table.write('</html>')
table.close()

print("Table Generation completed")
print("--------------------------")

#==================================================
# SVG generation
#==================================================


from xml.etree import ElementTree as et

# Header
f = open(configdata[4]+".svg", 'w')
f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')

#SVG XML element and base parts
svg = et.Element('svg', width='1200', height='800', version='1.1', xmlns='http://www.w3.org/2000/svg')

et.SubElement(svg, 'rect', id='Elem_'+str(idcount), x='50', y='50', width='1100', height='700',
              style='fill:white;stroke:rgb(204, 204, 255);stroke-width:10')
idcount = idcount + 1

et.SubElement(svg, 'line', id='Elem_'+str(idcount), x1='54', y1='480', x2='1146', y2='480',
                          style='stroke:black;stroke-width:2')
idcount = idcount + 1
 
# Draw circles and correct data to each
for i in day:
    if daytemp[i-1] > 25:

        text = et.Element('text', x=str(i*150), y='180', fill='black',
                          style='font-family:Arial;font-size:20px;text-anchor:middle')
        text.text = "Sunny"
        svg.append(text)

        et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx=str(i*150), cy='150', r='75', fill='rgb(244, 164, 96)',
                      onmouseover="evt.target.setAttribute('opacity', '0.3')",
                      onmouseout="evt.target.setAttribute('opacity','1)');")
        idcount = idcount + 1
        
    elif daytemp[i-1] > 15:
        
        text = et.Element('text', x=str(i*150), y='180', fill='black',
                          style='font-family:Arial;font-size:20px;text-anchor:middle')
        text.text = "Half cloudy"
        svg.append(text)

        et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx=str(i*150), cy='150', r='75', fill='rgb(152, 251, 152)',
                      onmouseover="evt.target.setAttribute('opacity', '0.2')",
                      onmouseout="evt.target.setAttribute('opacity','1)');")
        idcount = idcount + 1
        
    else:
        
        text = et.Element('text', x=str(i*150), y='180', fill='black',
                          style='font-family:Arial;font-size:20px;text-anchor:middle')
        text.text = "Cloudy"
        svg.append(text)
        
        et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx=str(i*150), cy='150', r='75', fill='rgb(193, 205, 193)',
                      onmouseover="evt.target.setAttribute('opacity', '0.3');",
                      onmouseout="evt.target.setAttribute('opacity','1)');")
        idcount = idcount + 1

 
# Draw texts
for i in day:

    #Draw temp info 
    text = et.Element('text', x=str(i*150), y='250', fill='black',
                      style='font-family:Sans;font-size:20px;text-anchor:middle')
    text.text = Days[i-1]
    svg.append(text)

    text = et.Element('text', x=str(i*150), y='110', fill='black',
                      style='font-family:Sans;font-size:15px;text-anchor:middle')
    text.text = "D: %.1f C / %.1f F" % (daytemp[i-1], farenheitday[i-1])
    svg.append(text)

    text = et.Element('text', x=str(i*150), y='130', fill='black',
                      style='font-family:Sans;font-size:15px;text-anchor:middle')
    text.text = "N: %.1f C / %.1f F" % (nighttemp[i-1], farenheitnight[i-1])
    svg.append(text)

    text = et.Element('text', x=str(i*150), y='150', fill='black',
                      style='font-family:Sans;font-size:15px;text-anchor:middle')

    #Draw amount of rain and rain diagram
    if sum(rain) > 0:
        text.text = "%.1f mm / %.1f %%" % (rain[i-1], ((rain[i-1]/sum(rain))*100))

        if i <= len(day):
            et.SubElement(svg, 'line', id='Elem_'+str(idcount), x1=str(i*150), y1='630', x2=str(i*150), y2=str(630-(rain[i-1]*5)),
                          style='stroke:rgb(204, 204, 255);stroke-width:50')
            idcount = idcount + 1
    else:
        text.text = "%.1f mm / - %%" % (rain[i-1])

    #Draw temp diagram
    et.SubElement(svg, 'line', id='Elem_'+str(idcount), x1=str((i*150)-7.5), y1='480', x2=str((i*150)-7.5), y2=str(480-(nighttemp[i-1]*5)),
                          style='stroke:rgb(51,153,204);stroke-width:15')
    idcount = idcount + 1

    et.SubElement(svg, 'line', id='Elem_'+str(idcount), x1=str((i*150)+7.5), y1='480', x2=str((i*150)+7.5), y2=str(480-(daytemp[i-1]*5)),
                          style='stroke:rgb(255,102,51);stroke-width:15')
    idcount = idcount + 1
        
    svg.append(text)

et.SubElement(svg, 'rect', id='Elem_'+str(idcount), x='50', y='630', width='1100', height='5',
              style='fill:white;stroke:rgb(204, 204, 255);stroke-width:5')
idcount = idcount + 1

text = et.Element('text', x='60', y='670', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Average day temp: %.1f C and %.1f F" % (avgdayc, avgdayf)
svg.append(text)

text = et.Element('text', x='60', y='700', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Average night temp: %.1f C and %.1f F" % (avgnightc, avgnightf)
svg.append(text)

text = et.Element('text', x='60', y='730', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Total rain: %.1f mm" % (sum(rain))
svg.append(text)

# Draw explanation marks

et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx='500', cy='660', r='10', fill='rgb(244, 164, 96)')
idcount = idcount + 1

text = et.Element('text', x='530', y='665', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Sunny"
svg.append(text)

et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx='500', cy='690', r='10', fill='rgb(152, 251, 152)')
idcount = idcount + 1

text = et.Element('text', x='530', y='695', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Half cloudy"
svg.append(text)

et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx='500', cy='720', r='10', fill='rgb(193, 205, 193)')
idcount = idcount + 1

text = et.Element('text', x='530', y='725', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Cloudy"
svg.append(text)

et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx='800', cy='720', r='10', fill='rgb(204, 204, 255)')
idcount = idcount + 1

text = et.Element('text', x='830', y='725', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Rain diagram"
svg.append(text)

et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx='800', cy='690', r='10', fill='rgb(255,102,51)')
idcount = idcount + 1

text = et.Element('text', x='830', y='695', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Day temperature diagram"
svg.append(text)

et.SubElement(svg, 'circle', id='Elem_'+str(idcount), cx='800', cy='660', r='10', fill='rgb(51,153,204)')
idcount = idcount + 1

text = et.Element('text', x='830', y='665', fill='black',
                  style='font-family:Sans;font-size:20px;text-anchor:start')
text.text = "Night temperature diagram"
svg.append(text)

f.write((et.tostring(svg)).decode())
f.close()

print ("Generation finished!")
print ("====================")

#------------------------------------------------------------
# PNG transformation
#------------------------------------------------------------
print("Starting external transformation program...")
Popen("cmd /k java -Xms256m -Xmx512m -jar batik/batik-rasterizer.jar *.svg")
print("Started")

print("##########################")
print("DONE")
print("##########################")



