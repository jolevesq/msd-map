def getEPSGFromWKID(wkid):
    # list of EPSG code https://epsg.io/3978
    # list os spatial references https://spatialreference.org/ref
    # list of ESRI spatial references https://developers.arcgis.com/rest/services-reference/projected-coordinate-systems.htm
    epsgDict = {
        '102002': '3978',
        '102100': '3857',
        '4326': '4326',
        '3978': '3978'
    }

    return epsgDict[wkid]

def getFontfromESRI(name):
    fontDict = {
        'ESRI Geometric Symbols': 'esri_geom',
        'ESRI Default Marker': 'esri_11',
        'ESRI IGL Font21': 'esri_221',
        'ESRI Enviro Hazard Sites': 'esri_802',
        'ESRI Business': 'esri_34'
    }

    return fontDict[name]