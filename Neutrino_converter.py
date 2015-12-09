#fix time steps
#allow for several gauges

import numpy
import os
import re


def func():
 file_name = 'fort.gauge'
 while True:
  try:
   num_gauges = int(raw_input("Enter the number of gauges: "))
   if num_gauges < 1:
    raise ValueError("A number less than 1 was selected.") 
   break
  except ValueError:
   print "Please enter a valid number."
 gauge_file = open(file_name, 'r')
 read_file = gauge_file.read()
 counter = 0
 regex = "[-+]?[\d+\.\d+]+(?:E[-+]?\d+)?"
 
 gauge_data = []
 for i, line in enumerate(read_file.splitlines()):
  gauge_data.append(line)
 gauge_data1 = []

 for j in range(len(gauge_data)):
  gauge_data1.append(re.findall(regex, str(gauge_data[j])))
 
 for k in range(len(gauge_data)):
  for l in range(7):
   gauge_data1[k][l] = float(gauge_data1[k][l])
  if gauge_data1[k][4] <= 1:
   gauge_data1[k][4] = 0.0
  else:
   gauge_data1[k][4] = gauge_data1[k][4]/gauge_data1[k][3]
  if gauge_data1[k][5] <= 1:
   gauge_data1[k][5] = 0.0
  else:
   gauge_dat1[k][5]  = gauge_dat1[k][5]/gauge_dat1[k][3] 
 
  del gauge_data1[k][1]
 
 newfile = open('Neutrino_data', 'w+')
 
 #numpy.savetxt(newfile,gauge_data1,fmt='%10.5f',delimiter=' ',newline='\n',header=" Gauge no.    Time      Height   x-velocity  y-velocity   eta  \n", footer ="\n", comments = ' ') 


 for m in range(len(gauge_data1)):
  for n in range(5):
   newfile.write(str(gauge_data1[m][n])+', ')
  newfile.write(str('\n'))
 newfile.close

#Run the code
func()
