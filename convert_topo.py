"""
This script provides functions for rewriting INL topography files (.obj files obtained through the web terrain mapper) to GeoClaw-recognized topography files.

Note: topotools2.py (topotools.py for Clawpack 4.x) muset be saved in the directory $CLAW/clawpack/geoclaw. This file can be found on the University of Washington's website (http://depts.washington.edu/clawpack/clawpack-4.6.2/python/pyclaw/geotools/topotools.py) or on GitHub (https://github.com/clawpack/clawpack-4.x/blob/7ec0ffccf2b97ddd82b3f8aa8656b760ee32f9ce/python/pyclaw/geotools/topotools.py). Either this file must be saved as topotools2.py or the import module below must be changed. 

 
:Classes:
 - None

:Functions:
 - get_file_name
 - read_file 
 - topo_conversion

:TODO:
 - Simplify code
 - make a loop that asks for name of file over and over until a correct one is entered -- and a valid topotype
 - file so it can handle negative numbers--below sea level. 
 - In this code the units are not converted from meters to feet. Does it even matter? Do we need to do that?

"""   

import os
import copy
import numpy as np
import re
import sys
from clawpack.geoclaw import topotools# do I need this?
from clawpack.geoclaw import topotools2




#==========================================================================

#This function is to get the user input. If user input is invalid, the user
#will be prompted to re-enter the information. 

#==========================================================================

def get_file_name():

 while True:
  try:
   file_name = raw_input("Enter the name of the file that you would like to convert (the file must be in the current directory): ")
   open(file_name, 'r').close()
   break
  except IOError:
   print('%s is not found in the current directory. Please enter a valid filename. '%file_name)
  except:
   print "Unexpected error. Please enter a valid filename. "
 
 while True:
  try:
   topo_type = int(raw_input("Choose the topotpye to convert your file to (enter 1, 2 or 3): "))
   if topo_type > 3:
    raise ValueError("A number larger than 3 was selected.") 
   elif topo_type < 1:
    raise ValueError("A number smaller than 1 was selected.")
   break
  except ValueError:
   print "Please enter 1, 2 or 3. "
 
 n = 0
 while n != 1:
  tf = raw_input("Will you be using more than one topography map in GeoClaw? (enter either \"yes\" or \"no\"): ")
  tf = tf.lower()
  if tf == "yes" or tf == "no":
   n = 1

 if tf == "yes":
  tf = True
 else:
  tf = False

 if tf:
  while True:
   try:
    minelv1 = float(raw_input("Enter the lowest elevation in the largest topography to be used in the simulation: "))
    minelv2 = float(raw_input("Enter the lowest elevation in the current topography file: "))
    break
   except ValueError:
    print "Please enter a number." 
   except:
    print "Unexpected error occured: ", sys.exc_info()[0]
  
  height = minelv2 - minelv1
 else:
  height = 0

 outfile = raw_input("Enter a name for the outfile: ")

 return (file_name,topo_type,outfile,height)
  
#end of get_filename()




#==========================================================================

#Read the topography file and save it as a list.

#==========================================================================

def read_file(file_name):  
 try:
  with open(file_name) as f: #open file
   content = f.readlines() #save contents of the file as "content"
  f.close()
 except IOError as e:
  print "I/O error({0}): {1}".format(e.errno, e.strerror)
 except:
  print "Unexpected error occured while reading file: ", sys.exc_info()[0]
 return content

#end of read_file()




#========================================================================

#delete unneeded lines and numbers, create lists of x, y and z values 

#========================================================================

def topo_conversion(content, topo_type, outfile, height):
 vertices = []
 for i in range(len(content)):
  if content[i][0] == 'v':
   vertices.append(content[i]) #find vertices in file and put in the list "vertices"

 x = []
 y = []
 z1 = []

 for j in range(len(vertices)): #extract numbers and save as lists of x,y and z values
  temp = re.findall("[\.0-9]*[0-9]+", vertices[j]) 
  x.append(temp[0])
  y.append(temp[2]) 
  z1.append(temp[1]) 

#change order of y
 y1 = []
 for k in range(len(x)):
  y1.append(y[len(y)-k-1])  

#change to floats
  
 for k in range(len(x)):
  x[k] = float(x[k])  
  z1[k] = float(z1[k])
  y1[k] = float(y1[k])

#change the order of z1

 xstep = int(x[1] - x[0])
 step1 = (int(max(x))+xstep)/xstep #number of columns
 step2 = int((max(y1)+ xstep)/xstep) #number of rows
 
 z = []
 
 for i in range(step2-1,-1,-1):
  for k in range(i*step1,i*step1+step1,1):
   z.append(z1[k])
#change the depth of the z values
 for i in range(len(z)):
  z[i] = z[i] + height

#save x, y and z to a new list in that order

 new = []
 for k in range(len(x)):
  new.append(x[k])
  new.append(y1[k])
  new.append(z[k])

 new1 = []
 for n in range(0,len(new),3):
  new1.append(new[n:n+3])
 
 newfile = open('temp_topo.txt','w+') 
 newfile.writelines(["%s\n" % " ".join(repr(e) for e in item) for item in new1]) 
 newfile.close()

 topotools2.converttopotype('temp_topo.txt', outfile, topotypein=1, topotypeout=topo_type, nodata_value=4000)
 
 os.remove('temp_topo.txt')
 print "Conversion Completed. The file %s can be found in the current directory." %outfile 

 return

#end of topo_conversion()




#==========================================================================

#pull everything together

#==========================================================================

def convert_topo():

 file_name, topo_type , outfile, height = get_file_name()

 content = read_file(file_name)
 
 topo_conversion(content, topo_type, outfile, height)

#end of convert_topo()




 
#Run the code
convert_topo()
