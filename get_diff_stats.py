#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################

import sys
import os

class nodes:
    def __init__(self, x=0, y=0, z=0):
        self.created = x
        self.modified = y
        self.deleted = z
		
class ways:
    def __init__(self, x=0, y=0, z=0):
        self.created = x
        self.modified = y
        self.deleted = z
		
class buildings:
    def __init__(self, x=0, y=0, z=0):
        self.created = x
        self.modified = y
        self.deleted = z



def main(diff_file, out_dir):
	

	Nodes = nodes()
	Ways = ways()
	Buildings = buildings()
	
	#read osm diff data
	filein = file(diff_file, "r")
	
	lines = filein.readlines()

	for i in range(0,len(lines)):
		#find all new nodes and ways
		if lines[i].startswith('  <create>'):
			for j in range(0,len(lines)-i):
				if lines[i+j].startswith('  </create>'):
					break
				if lines[i+j].startswith('    <node'):
					Nodes.created = Nodes.created + 1
				if lines[i+j].startswith('    <way'):
					Ways.created = Ways.created + 1
					for k in range(0,len(lines)-i-j):
						if lines[i+j+k].startswith('    </way>'):
							break
						if lines[i+j+k].startswith('      <tag k="building"'):
							Buildings.created = Buildings.created + 1
						

		#find all modified nodes and ways
		if lines[i].startswith('  <modify>'):
			for j in range(0,len(lines)-i):
				if lines[i+j].startswith('  </modify>'):
					break
				if lines[i+j].startswith('    <node'):
					Nodes.modified = Nodes.modified + 1
				if lines[i+j].startswith('    <way'):
					Ways.modified = Ways.modified + 1
					for k in range(0,len(lines)-i-j):
						if lines[i+j+k].startswith('    </way>'):
							break
						if lines[i+j+k].startswith('      <tag k="building"'):
							Buildings.modified = Buildings.modified + 1
							
		#find all deleted nodes and ways
		if lines[i].startswith('  <delete>'):
			for j in range(0,len(lines)-i):
				if lines[i+j].startswith('  </delete>'):
					break
				if lines[i+j].startswith('    <node'):
					Nodes.deleted = Nodes.deleted + 1
				if lines[i+j].startswith('    <way'):
					Ways.deleted = Ways.deleted + 1
					for k in range(0,len(lines)-i-j):
						if lines[i+j+k].startswith('    </way>'):
							break
						if lines[i+j+k].startswith('      <tag k="building"'):
							Buildings.deleted = Buildings.deleted + 1
	
	#write to ouput file
	outputAsc = out_dir + '\diff_stats.txt'
	fileout = file(outputAsc, "a")
	line = diff_file+';'+str(Nodes.created)+';'+str(Nodes.modified)+';'+str(Nodes.deleted)+';'+str(Ways.created)+';'+str(Ways.modified)+';'+str(Ways.deleted)+';'+str(Buildings.created)+';'+str(Buildings.modified)+';'+str(Buildings.deleted)+'\n'
	fileout.write(line)
	fileout.close()
	
	print '############ END ######################################'
	print '##'
	print '## input diff file: '+diff_file
	print '##'
	print '## created nodes: '+str(Nodes.created)
	print '## created ways: '+str(Ways.created)
	print '## created buildings: '+str(Buildings.created)
	print '##'
	print '## modified nodes: '+str(Nodes.modified)
	print '## modified ways: '+str(Ways.modified)
	print '## modified buildings: '+str(Buildings.modified)
	print '##'
	print '## deleted nodes: '+str(Nodes.deleted)
	print '## deleted ways: '+str(Ways.deleted)
	print '## deleted buildings: '+str(Buildings.deleted)
	print '##'
	print '##'
	print '## B. Herfort, GIScience Research Group'
	print '##'
	print '#######################################################'




if __name__ == "__main__":

    #
    # example run : $ python merge_osm_data.py diff.osc
    #

    if len( sys.argv ) != 3: 
        print "[ ERROR ] you must supply 2 arguments: diff.osc out_dir"
        sys.exit( 1 )

    main( sys.argv[1], sys.argv[2] )	
	
