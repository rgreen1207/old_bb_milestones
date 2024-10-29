# _scriptname = 'Blueboard.Utilities.Struct'

# #
# #  Blueboard.Utilities.Struct.py
# #
# #  Created by Jason Wiener on 9/4/08.
# #  Refactored by Jason Wiener on 9/16/08.
# #  Copyright (c) 2008 JasonWiener. All rights reserved.
# #  Copyright (c) 2020 HyperdriveMe, Inc. All rights reserved.
# #

# from .struct import pack, unpack
# from types import IntType, LongType

# # https://docs.python.org/2.7/library/struct.html

# #decode unsigned int32
# def deStructInt(data):
#   try:
#       return int(unpack('>I', data)[0])

#   except Exception as inst:
#       print(_scriptname+'.deStructInt.ERROR:', data, inst)


# #encode unsigned int32
# def structInt(data):
#   try:
#       if type(data) is not IntType:
#           data = int(data)
            
#       return pack('>I', data)

#   except Exception as inst:
#       print(_scriptname+'.structInt.ERROR:', data, inst)


# #decode unsigned long
# def deStructLong(data):
#   try:
#       return int(unpack('>Q', data)[0])

#   except Exception as inst:
#       print(_scriptname+'.deStructLong.ERROR:', data, inst)


# #encode unsigned long
# def structLong(data):
#   try:
#       if type(data) is not LongType:
#           data = int(data)
            
#       return pack('>Q', data)

#   except Exception as inst:
#       print(_scriptname+'.structLong.ERROR:', data, inst)


# def deStructBool(data):
#   try:
#       return int(unpack('?', data)[0])

#   except Exception as inst:
#       print(_scriptname+'.deStructBool.ERROR:', data, inst)


# def structBool(data):
#   try:
#       if type(data) is not IntType:
#           data = int(data)
            
#       return pack('?', data)

#   except Exception as inst:
#       print(_scriptname+'.structBool.ERROR:', data, inst)
