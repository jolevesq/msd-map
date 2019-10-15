import datetime

traceFile = None

def create(path):
    """
    Create trace file

    Args:
        path: Path for the map file
    """
    global traceFile
    traceFile = open(path, 'w')
    log('Start Trace: ' + str(datetime.datetime.now()))

def close():
    """
    Close trace file
    """
    global traceFile
    log('End Trace: ' + str(datetime.datetime.now()))
    traceFile.close()

def log(txt):
    """
    Add to trace file

    Args:
        txt: Text to add
    """
    traceFile.write(txt + '\n')

def setSampleUrl(mapFile, layers):
    """
    Add the sample url to use to test the service

    Args:
        mapFile: Map file to use
        layers: Layers to use
    """
    url = """***ReplaceByMapServer***?map=/home/ubuntu/wms/{mapFile}&layers={layers}
&VERSION=1.1.1&FORMAT=application/openlayers&SERVICE=WMS&REQUEST=GetMap&SRS=EPSG%3A3978
&BBOX=-4482582,-1201458,4333351,6429140&WIDTH=1600&HEIGHT=800""".format(mapFile=mapFile, layers=layers)

    log('\nURL: ' + url.replace('\n', '') + '\n')