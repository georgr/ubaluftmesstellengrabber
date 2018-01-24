# -*- coding: utf-8 -*-
import requests
import json
import io

station_ids = set()

geojson = {'type': 'FeatureCollection', 'features': []}

res = requests.get('http://luft.umweltbundesamt.at/pub/map_chart/index.pl?runmode=values_json').json()
for station in res['stations']:
    if station['MetaInfo']['Owner'].startswith('Amt der Nieder'):
        id = station['stationid']
        name = station['MetaInfo']['Name']
        owner =  station['MetaInfo']['Owner']
        location = station['MetaInfo']['Location']
        x = float(station['gml$Point']['gml$coord']['X'])
        y = float(station['gml$Point']['gml$coord']['Y'])
        z = float(station['gml$Point']['gml$coord']['Z'])

        #filter duplicates
        if id not in station_ids:
            feature = {'type': 'Feature',
                       'properties': {'id':id,
                                      'name':name,
                                      'owner':owner,
                                      'location':location},
                       'geometry': {'type': 'Point',
                                    'coordinates': [x,y]}}
            geojson['features'].append(feature)
            station_ids.add(id)

with io.open('luftmesstellen_noe.geojson', 'w', encoding='utf8') as f:
    f.write(unicode(json.dumps(geojson, ensure_ascii=False)))

