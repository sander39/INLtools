"""
This module ... (Enter description)
"""
import numpy
import os
import re
from itertools import islice

#=======================================================================
#make this part its own function

#=======================================================================
def get_input():

# Get the coordinates of the corners of the region of interest
 #north = float(raw_input("Enter the upper latitude for the region of interest: "))
 #south = float(raw_input("Enter the lower latitude for the region of interest: "))
 #east = float(raw_input("Enter the eastern longitude for the region of interest: "))
 #west = float(raw_input("Enter the western longitude for the region of interest: "))

 geo_step = .5  #float(raw_input("Enter the timestep of the GeoClaw simulation: "))
 neutrino_step = 1  #float(raw_input("Enter the timestep of the Neutrino simulation: "))

 geo_start = 0 #float(raw_input("Enter the beginning time of the GeoClaw simulation: "))
 geo_end = 4 #float(raw_input("Enter the ending time of the GeoClaw simulation: "))
#geo start and end in seconds
 #this part not neede.d 
 #path = raw_input("Enter the path to the output directory where you would like to extract the data from (do not include the name of the output file): ")
 north = 0
 south = 0
 east = 0
 west = 0
 return (north, south, east, west, geo_step, neutrino_step, geo_start, geo_end)#path

#end of function

#=========================================================================





#===========================================================================
#determine which grids are good

#===========================================================================
def useful_grids(file_name, north, south, east, west):

#This chunk of code locates the grid headers and saves the line numbers. It needs to be inside of a while loop that will send it through all the fort.q files we want it to go through. 

 #file_name= os.getcwd()+'/'+ 'output_files' + file_name
 fort_file = open(file_name, 'r')
 read_file = fort_file.read()

 grid_headers = []
 num_of_grids = 0
 file_data = read_file.splitlines()

 for i, line in enumerate(read_file.splitlines()):
  if 'grid_number' in line:
   num_of_grids += 1
  #grid_headers.append(num_of_grids)
   grid_headers.append(i)
   grid_headers.append(line)
  elif ('mx' or 'numcols') in line:
   grid_headers.append(line) 
  elif ('my' or 'numrows') in line:
   grid_headers.append(line)
  elif ('xlow' or 'xllcorner') in line:
   grid_headers.append(line)
  elif ('ylow' or yllcorner) in line:
   grid_headers.append(line)
  elif 'dx' in line:
   grid_headers.append(line)
  elif 'dy' in line:
   grid_headers.append(line)

 grid_headers_data = []
 temp = []

#make space 
 grid_headers_data = [[] for l in range(num_of_grids)]

#first, extract numbers from the list grid_headers
 regex = "[-+]?[\d+\.\d+]+(?:E[-+]?\d+)?"
 counter = 0
 for j in range(num_of_grids):
  for k in range(8):
   grid_headers_data[j].extend(re.findall(regex, str(grid_headers[counter])))
   counter += 1

#change grid_headers-data into floats
 for m in range(len(grid_headers_data)):
  for k in range(8):
   grid_headers_data[m][k] = float(grid_headers_data[m][k])

#now go through and decide which grids are relevent
 useful_data = []
 counter1 = 0
 counter2 = 0

 for k in range(num_of_grids):
  grid_line = grid_headers_data[k][0]+9
  mx = grid_headers_data[k][2]
  my = grid_headers_data[k][3]
  xlow = grid_headers_data[k][4]
  ylow = grid_headers_data[k][5]
  dx = grid_headers_data[k][6]
  dy = grid_headers_data[k][7]
  stop = grid_line+mx*my+my

  grid_top = ylow + my*dy
  grid_left = xlow + mx*dx
  print xlow, grid_left, ylow, grid_top
# determine what grids will be useful 
  if xlow <= east <= grid_left and xlow <= west <= grid_left and ylow <= north <= grid_top and ylow <= south <= grid_top:
   useful_data.append(grid_headers_data[k])
   useful_data.append([])
#now attach all the useful data. 
   for line in islice(read_file.splitlines(), grid_line, stop, 1):
    useful_data[2*k+1].append(line)
 #print useful_data
 return useful_data 
 
#============================================================================
#############################################################################
#everything above here working




#============================================================================
#this function goes through and gets only data that is on the boundary of the region of interest. 

#============================================================================
def get_data(useful_data, north, south, east, west):
#Determine how many grids are in useful_data
 num_useful_grids = len(useful_data)
 east_line = []
 west_line = []
 south_line = []
 north_line = []

 for s in range(1,num_useful_grids,2): #go to the correct element in the list
  mx = useful_data[s-1][2]
  my = useful_data[s-1][3]
  xlow = useful_data[s-1][4]
  ylow = useful_data[s-1][5]
  dx = useful_data[s-1][6]
  dy = useful_data[s-1][7]
  top = ylow+my*dy 

  for i,k in enumerate(useful_data[s]):  
   if xlow <= east:
    EL = i 

   if xlow <= west:
    WL = i
   xlow += dx
  east_line.append(EL)
  west_line.append(WL)
 
  for j in range(0,int(my*mx+my),int(my)):
   if top >= north:
    NL = j
   if top >= south:
    SL = j
   top -= dy
  north_line.append(NL)
  south_line.append(SL)

 south_data = []
 north_data = []
 east_data = []
 west_data = []

#Get the rows for north and south
 count = 0
 for s in range(1,num_useful_grids,2):
  mx = useful_data[s-1][2]
  my = useful_data[s-1][3]
  xlow = useful_data[s-1][4]
  ylow = useful_data[s-1][5]
  dx = useful_data[s-1][6]
  dy = useful_data[s-1][7]

  north_data.append(useful_data[s][int(north_line[count]):int(north_line[count]+mx)])
  south_data.append(useful_data[s][int(south_line[count]):int(south_line[count]+mx)])
  east_data.append([])
  west_data.append([])
  for k in range(int(my)):
   east_data[count].append(useful_data[s][int(east_line[count]+k*(my+1))])
   west_data[count].append(useful_data[s][int(west_line[count]+k*(my+1))])
  count += 1

 return (east_data, west_data, north_data, south_data)
#============================================================================





#============================================================================
#extract the data

#============================================================================
def extract_data(east_data, west_data, north_data, south_data):
 regex = "[-+]?[\d+\.\d+]+(?:E[-+]?\d+)?"

 north_data1 = []
 south_data1 = []

 for m in range(len(north_data)):
  north_data1.append([])
  south_data1.append([])
  for a in range(len(north_data[m])):
   north_data1[m].append(re.findall(regex, north_data[m][a])) 
   south_data1[m].append(re.findall(regex, south_data[m][a]))  
 
 for a in range(len(north_data1)):
  north_data1[a] = filter(None, north_data1[a])
  south_data1[a] = filter(None, south_data1[a])

#change to floats
 for a in range(len(north_data1)):
  for b in range(len(north_data1[a])):
   for c in range(4):
    north_data1[a][b][c] = float(north_data1[a][b][c])
    south_data1[a][b][c] = float(south_data1[a][b][c])

#divide the momentums by the height to get velocity
#WARNING: This only works if the heights in the output files are in meters
 for a in range(len(north_data1)):
  for b in range(len(north_data1[a])):
   for c in range(1,3,1):
    if north_data1[a][b][c] <= 0.001: #if water-level is less than 1 mm
     north_data1[a][b][c] = 0
    else:
     north_data1[a][b][c] = north_data1[a][b][c]/north_data1[a][b][0]

    if south_data1[a][b][c] <= 0.001: #if water-level is less than 1 mm
     south_data1[a][b][c] = 0
    else:
     south_data1[a][b][c] = south_data1[a][b][c]/south_data1[a][b][0]

 east_data1 = []
 west_data1 = []

 for m in range(len(east_data)):
  east_data1.append([])
  west_data1.append([])
  for a in range(len(east_data[m])):
   east_data1[m].append(re.findall(regex, east_data[m][a])) 
   west_data1[m].append(re.findall(regex, west_data[m][a]))  
 
 for a in range(len(east_data1)):
  east_data1[a] = filter(None, east_data1[a])
  west_data1[a] = filter(None, west_data1[a])

#change to floats
 for a in range(len(east_data1)):
  for b in range(len(east_data1[a])):
   for c in range(4):
    east_data1[a][b][c] = float(east_data1[a][b][c])
#######################################
 for a in range(len(west_data1)):
  for b in range(len(west_data1[a])):
   for c in range(4):
    west_data1[a][b][c] = float(west_data1[a][b][c])

#divide the momentums by the height to get velocity
#WARNING: This only works if the heights in the output files are in meters
 for a in range(len(east_data1)):
  for b in range(len(east_data1[a])):
   for c in range(1,3,1):
    if east_data1[a][b][c] <= 0.001: #if water-level is less than 1 mm
     east_data1[a][b][c] = 0
    else:
     east_data1[a][b][c] = east_data1[a][b][c]/east_data1[a][b][0]
 for a in range(len(west_data1)):
  for b in range(len(west_data1[a])):
   for c in range(1,3,1):
    if west_data1[a][b][c] <= 0.001: #if water-level is less than 1 mm
     west_data1[a][b][c] = 0
    else: 
     west_data1[a][b][c] = west_data1[a][b][c]/west_data1[a][b][0]

#Delete etah from the list
 for a in range(len(east_data1)):
  for b in range(len(east_data1[a])):
   east_data1[a][b].pop() 
 for a in range(len(west_data1)):
  for b in range(len(west_data1[a])):
   west_data1[a][b].pop() 
 
 for c in range(len(north_data1)):
  for d in range(len(north_data1[c])):
   north_data1[c][d].pop()
   south_data1[c][d].pop()

 return (east_data1, west_data1, north_data1, south_data1)
#===========================================================================





#============================================================================
#Write the output file

#============================================================================
def write_file(file_counter, geo_time, file_num, east_data1, west_data1, north_data1, south_data1, my_bool):

 egrid = 1
 wgrid = 1
 ngrid = 1
 sgrid = 1
#Create a folder to put the files in 
 #folder_name = raw_input("Enter the name of the directory where you'd like your files to be written")
 #newpath = r'%s'%folder_name
 #if not o.s.path.exists(newpath):
  #os. makedirs(newpath)

 #if file_counter == 0:
  #mode = 'w+'
 #else:
  #mode = 'a'

#%s'%file_num
 newfile = open('Neutrino_data%s'%file_num, 'w+')
 newfile.writelines("Data for perimeters at time %s \n" % geo_time)
#write east_data1 to newfile
 for d in range(len(east_data1)): 
  numpy.savetxt(newfile, east_data1[d], fmt = '%10.5f',delimiter = ' ', newline = '\n',header = ' \n'+"Eastern data, grid %s\n" % egrid +'\n'+"Height      x-velocity  y-velocity           \n", footer ="\n", comments = ' ') 
  egrid += 1
#write west_data1 to newfile
 for d in range(len(west_data1)): 
  numpy.savetxt(newfile, west_data1[d], fmt = '%10.5f',delimiter = ' ', newline = '\n',header = ' \n'+"Western data, grid %s\n" % wgrid +'\n'+"Height      x-velocity  y-velocity           \n", footer ="\n", comments = ' ') 
  wgrid += 1
#write north_data to newfile
 for d in range(len(north_data1)): 
   numpy.savetxt(newfile, north_data1[d], fmt = '%10.5f',delimiter = ' ', newline = '\n',header = ' \n'+"Northern data, grid %s\n" % ngrid +'\n'+"Height      x-velocity  y-velocity           \n", footer ="\n", comments = ' ') 
   ngrid += 1
#write south_data to newfile
#write east_data1 to newfile
 for d in range(len(south_data1)): 
  numpy.savetxt(newfile, south_data1[d], fmt = '%10.5f',delimiter = ' ', newline = '\n',header = ' \n'+"Southern data, grid %s\n" % egrid +'\n'+"Height      x-velocity  y-velocity           \n", footer ="\n", comments = ' ')  
  egrid += 1
 if my_bool:
  newfile.close()

#============================================================================
"""
# for a in range(len(east_data1)):
  for b in range(len(east_data1[a])):
   for c in range(4):
    east_data1[a][b][c] = str(east_data1[a][b][c])
    west_data1[a][b][c] = str(west_data1[a][b][c])
 for a in range(len(north_data1)):
  for b in range(len(north_data1[a])):
   for c in range(4):
    north_data1[a][b][c] = str(north_data1[a][b][c])
    south_data1[a][b][c] = str(south_data1[a][b][c])
"""
 




#=============================================================================
#This function loops through the desired fort.q files in the desired directory

#=============================================================================
def loop(geo_step = .3333333333, neutrino_step = .3333333333, geo_start = 0, geo_end = 8):
#Have user input data
 north, south, east, west, geo_step, neutrino_step, geo_start, geo_end = get_input() #, path
 east = 20000
 west = 18520 
 north =43.91638
 south = 43.91366

 geo_time = 0
 my_bool = False
 file_step  = int(neutrino_step / geo_step)
 file_counter = 0
 num_files = int((geo_end-geo_start) / geo_step)
 
 for f in range(0, num_files+1, file_step): 
  if neutrino_step < geo_step:
   print "You have more Neutrino timesteps than you have GeoClaw timesteps. Please decrease your number of Neutrino timesteps (increase their size)." 
  else: 
   if f == num_files:
    my_bool = True
   file_num = '%s' %f
   while len(file_num) <= 3:
    file_num = '0'+file_num
   file_name = 'fort.q%s' %file_num
   #file_name = path+'/'+file_name
   
 useful_data = useful_grids(file_name, north, south, east, west)
 east_data, west_data, north_data, south_data = get_data(useful_data, north, south, east, west)
 east_data1, west_data1, north_data1, south_data1 = extract_data(east_data, west_data, north_data, south_data)
 write_file(file_counter, geo_time, file_num, east_data1, west_data1, north_data1, south_data1, my_bool)
 geo_time += geo_step
 file_counter +=1


#=============================================================================


loop()

#newfile.writelines(["%s\n" % " ".join(repr(e) for e in item) for item in west_data1])
#["%s\n" % " ".join(repr(e) for e in item) for item in west_data1]) 
 #newfile.close()
















































