#!/usr/bin/env python2

import os
import sys
import json

import shapely.geometry as s

if len(sys.argv) != 3:
    print('usage: ' + sys.argv[0] + ' /path/to/config.json /path/to/peers')
    sys.exit(1)

configFile = sys.argv[1]
peersDir = sys.argv[2]

config = json.loads(open(configFile).read())

gpsPoly = config['client']['otherCommunityInfo']['localCommunityPolygon']
poly = s.Polygon(map(lambda point: (point['lng'], point['lat']), gpsPoly))

for filename in os.listdir(peersDir):
    if len(filename) == 0 or filename[0] == '.':
        continue

    absFilename = peersDir + '/' + filename
    if os.path.isfile(absFilename):
        peerFile = open(absFilename, 'r')
        try:
            peerLines = peerFile.readlines()
            peer = {}
            mac  = None
            for line in peerLines:
                parts = line.split()

                if len(parts) > 0:
                    if parts[1] == 'Knotenname:':
                        peer['name'] = parts[2].lower()
                    elif parts[1] == 'Koordinaten:' and len(parts) == 4:
                        peer['gps'] = s.Point((float(parts[3]), float(parts[2])))

            if 'gps' in peer and not peer['gps'].within(poly):
                print peer['name']

        except Exception as e:
            print('Error in %s, ignoring peer: %s' % (absFilename, e));
        finally:
            peerFile.close()

