#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################


import json
import sys      #Require module sys for reading program options
from osgeo import ogr
import urllib2
import time
import os


def get_tm_project_json(task_id):
	
	#create url from hot tasking manager task_id
	url = 'http://tasks.hotosm.org/project/'+str(task_id)+'/tasks.json'
	referer = 'http://tasks.hotosm.org/project/'+str(task_id)
	x_req = 'XMLHttpRequest\r\n'
	
	#send xmlhttp request
	req = urllib2.Request(url)
	req.add_header('Referer', referer)
	req.add_header('X-Requested-With', x_req)
	resp = urllib2.urlopen(req)
	content = resp.read()
	
	#convert content to json format and count features
	tm_project_json = json.loads(content)
	
	#returns the tm project information in json format
	return tm_project_json
    
	
	
	
def get_tm_info(tm_project_json):
	
	#get feature count
	cnt_features = len(tm_project_json['features'])
	
	#create new geometry collection
	geomcol =  ogr.Geometry(ogr.wkbGeometryCollection)
	subtask_id_list = []

	#iterate over all features
	for z in range(0,cnt_features):
		
		#get subtask_id, type, coordinates from tm_project_json
		subtask_id = str(tm_project_json['features'][z]['id'])
		type = tm_project_json['features'][z]['geometry']['type']
		coordinates = tm_project_json['features'][z]['geometry']['coordinates']
		geojson = '{"type":"'+str(type)+'","coordinates":'+str(coordinates)+'}'
		
		#create polygon and add to geometry collection
		polygon = ogr.CreateGeometryFromJson(geojson)
		geomcol.AddGeometry(polygon)
		subtask_id_list.append(subtask_id)
		
	return (geomcol,subtask_id_list)

		
		
def get_osm_data(min_lon,max_lat,max_lon,min_lat,output_file):
	#get osm data from osm api
	url = 'http://api.openstreetmap.org/api/0.6/map?bbox='+min_lon+','+max_lat+','+max_lon+','+min_lat
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	content = resp.read()
	
	#save osm data
	fileout = file(output_file, "w")
	fileout.write(content)
	fileout.close()
	
	#close connection
	resp.close()
	

def main(task_id, output_directory):
	
	#Take start time
	start_time = time.time()
	
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	
	
	tm_project_json = get_tm_project_json(task_id)

	geomcol = get_tm_info(tm_project_json)[0]
	subtask_id_list = get_tm_info(tm_project_json)[1]
	
	
	for z in range(0,len(subtask_id_list)):
		
		#get bbox
		polygon = geomcol.GetGeometryRef(z)
		min_lon = str(polygon.GetEnvelope()[0])
		max_lat = str(polygon.GetEnvelope()[2])
		max_lon = str(polygon.GetEnvelope()[1])
		min_lat = str(polygon.GetEnvelope()[3])
		
		#get subtask_id
		subtask_id = subtask_id_list[z]
		
		#create output file name
		output_file = output_directory + '/' + str(task_id)+ '_' + str(subtask_id) + '.osm'
		
		# Check if file already exists
		if os.path.exists(output_file):
			continue
			
		else:	
			#get current osm data
			get_osm_data(min_lon,max_lat,max_lon,min_lat,output_file)
		
	#Take end time and calculate program run time
	end_time = time.time()
	run_time = end_time - start_time
	
	print '############ END ######################################'
	print '##'
	print '## input HOT task id: '+task_id
	print '##'
	print '## output directory: '+output_directory
	print '## number of output files: '+str(len(subtask_id_list))
	print '##'
	print '## runtime: '+str(run_time)+' s'
	print '##'
	print '## B. Herfort, GIScience Research Group'
	print '##'
	print '#######################################################'
	
	
if __name__ == "__main__":

    #
    # example run : $ python get_tm_osm_data.py 1088 testdata
    #

    if len( sys.argv ) != 3: 
        print "[ ERROR ] you must supply 2 arguments: HOT_Task_ID output_directory"
        sys.exit( 1 )

    main( sys.argv[1], sys.argv[2] )	
