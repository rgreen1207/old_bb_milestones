# from math import atan2, pi

# def bearing(endpoint, startpoint):
#   x1 = endpoint['lat']
#   y1 = endpoint['lng']
#   x2 = startpoint['lat']
#   y2 = startpoint['lng']

# #     print startpoint, endpoint

#   radians = atan2((y1 - y2), (x1 - x2))
#   compassReading = radians * (180 / pi)
#   coordNames = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
#   coordIndex = round(compassReading / 45)

#   if coordIndex < 0: coordIndex = coordIndex + 8

#   return (
#       compassReading, 
#       coordNames[int(coordIndex)]
#   )


# ''' example obj data containing lat and lng points
#   stop location - the radii end point
# '''
# if __name__ == '__main__':
#   endpoint = {
#       'lat' : 44.9631,
#       'lng' : -93.2492
#   }

#   #bus location from the southeast - the circle center
#   startpoint = {
#       'lat' : 44.95517,
#       'lng' : -93.2427
#   }
#   print(bearing(endpoint, startpoint))
#   print(bearing(startpoint, endpoint))
