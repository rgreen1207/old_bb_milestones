# import math


# class GeomEnum:

#   def __init__(self, data):
#       self.data = data or {}

#   '''
#   expects an array -> returns an int
#   '''
#   def compact(self, values):
#       return sum(map(int, values))

#   '''
#   expects an int -> returns {k,v}
#   '''
#   def expand(self, value):
#       ret = {}
#       if value:
#           keys = sorted(map(int, list(self.data.keys())))
#           for k in keys:
#               if math.floor(value %2) == 1:
#                   key = str(k)
#                   ret[key] = self.data[key]

#               value /= 2

#       return ret


# if __name__ == '__main__':
#   g = GeomEnum({
#       "1" : "contacted",
#       "2" : "cancelled",
#       "4" : "purchased",
#       "8" : "redeemed",
#       "16" : "refunded"
#   })
    
#   print(g.compact([1,2,8]))
#   print(g.expand(3))