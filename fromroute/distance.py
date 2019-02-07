from geopy import Point
import geopy.distance as dis
import pandas as pd

def distanceFromRoute(route,\
                      point,\
                      firstIndex = -1,\
                      lastIndex = -1,\
                      threshold = -1,\
                      latColumn = 'Lat',\
                      lngColumn = 'Lng'\
                     ):
    
    def perpendicularPoint(a, b, c): 

        aby = (dis.distance(a, (b[0], a[1])).km +\
             dis.distance((a[0], b[1]), b).km) / 2.0 

        abx = (dis.distance(a, (a[0], b[1])).km +\
             dis.distance((b[0], a[1]), b).km) / 2.0

        acy = (dis.distance(a, (c[0], a[1])).km +\
              dis.distance((a[0], c[1]), c).km) / 2.0

        acx = (dis.distance(a, (a[0], c[1])).km +\
              dis.distance((c[0], a[1]), c).km) / 2.0     

        s = aby**2 + abx**2

        if s == 0:
            return (True, a)

        t = (acy * aby + acx * abx) / s

        (px, py, pz) = dis.distance(kilometers = t * abx).\
        destination(point = dis.distance(kilometers = t * aby).\
                    destination(point = Point(a[0], a[1]),\
                                bearing = 0 if (b[0] > a[0]) else 180),\
                    bearing = 90 if b[1] > a[1] else 270)  

        D = (px, py)

        minx = min(a[0], b[0])
        maxx = max(a[0], b[0])
        miny = min(a[1], b[1])
        maxy = max(a[1], b[1])

        valid = (minx <= D[0] <= maxx) and (miny <= D[1] <= maxy)

        return (valid, D)
    
    if type(point) is not tuple:
        raise ValueError('Invalid point')

    elif type(route) is pd.core.frame.DataFrame:
        
        cols = list(route.columns.values)
        
        if (latColumn in cols) and (lngColumn in cols):
    
            distance = float('inf')
            startIndex = -1
            endIndex = -1
            closestPoint = (float('inf'), float('inf'))

            first = max(0, firstIndex)

            if lastIndex > 0:
                last = min(lastIndex, len(route) - 1)
            else:
                last = len(route) - 1

            if first >= last:
                raise ValueError('Invalid indeces')

            for i in range(first, last):

                p1 = (route.iloc[i][latColumn], route.iloc[i][lngColumn])
                p2 = (route.iloc[i + 1][latColumn], route.iloc[i + 1][lngColumn])

                (onSegment, p3) = perpendicularPoint(p1, p2, point)

                if onSegment:

                    d3 = dis.distance(p3, point).m

                    if (d3 < distance):
                        distance = d3
                        startIndex = i
                        endIndex = i + 1
                        closestPoint = p3

                else:

                    d1 = dis.distance(p1, point).m
                    d2 = dis.distance(p2, point).m

                    if (d1 < distance):
                        distance = d1
                        startIndex = i
                        endIndex = i
                        closestPoint = p1

                    if (d2 < distance):
                        distance = d2
                        startIndex = i + 1
                        endIndex = i + 1
                        closestPoint = p2

                if threshold > 0:
                    if distance <= threshold:
                        return (distance, closestPoint, startIndex, endIndex)

            return (distance, closestPoint, startIndex, endIndex)
        
        else:
            raise ValueError('Route does not contain ' + latColumn + ' and ' + lngColumn)

    else:
         raise ValueError('Route is not a pandas.core.frame.DataFrame')
         