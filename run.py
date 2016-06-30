#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################

import os
import sys
import sched
import time

count = 0
timestamp_list = []
task_id = sys.argv[1]

def do_something_else(sc): 
	print "start next run..."

	#get time
	lt = time.localtime()
	
	timestamp = str(lt[0])+'_'+str(lt[1])+'_'+str(lt[2])+'_'+str(lt[3])+'_'+str(lt[4])
	timestamp_list.append(timestamp)
	print 'timestamp: %s' % timestamp
	
	#create osm data directory
	cwd = os.getcwd()
	osm_data_dir = cwd + '\osm_data'+'_'+timestamp
	
	os.mkdir(osm_data_dir)
	
	#get osm data for tasking manager project
	print 'Download OSM data from OpenStreetMap API. This may take some time...'	
	cmd = 'python get_tm_osm_data.py '+task_id+' '+osm_data_dir
	os.system(cmd)
	
	
	#merge osm data
	print 'Merge .osm files'
	output_file = osm_data_dir + '\merge_'+timestamp+'.osm'
	cmd = 'python merge_osm_data.py ' + osm_data_dir + ' ' + output_file + ' osm'
	os.system(cmd)
	
	
	#compare osm data
	print 'Compare two .osm files and derive change'
	new_osm = cwd + '\osm_data'+'_'+timestamp_list[len(timestamp_list)-1]+'\merge_'+timestamp_list[len(timestamp_list)-1]+'.osm' 
	old_osm = cwd + '\osm_data'+'_'+timestamp_list[len(timestamp_list)-2]+'\merge_'+timestamp_list[len(timestamp_list)-2]+'.osm'
	out_file = cwd + '\output\diff_'+timestamp+'.osc'
	cmd = 'python compare_osm_data.py ' + new_osm + ' ' + old_osm + ' ' + out_file
	os.system(cmd)
	
	
	#calculate diff statictics
	diff_file = out_file
	out_dir = cwd + '\output'
	print diff_file
	cmd = 'python get_diff_stats.py ' + diff_file +' ' + out_dir
	os.system(cmd)

	sc.enter(900, 1, do_something_else, (sc,))
	

def do_something(sc): 
	print "start first run..."
    
	#get time
	lt = time.localtime()
	
	timestamp = str(lt[0])+'_'+str(lt[1])+'_'+str(lt[2])+'_'+str(lt[3])+'_'+str(lt[4])
	timestamp_list.append(timestamp)
	
	print 'timestamp: %s' % timestamp
	
	#timestamp = '2016_6_29_17_4'
	
	#create osm data directory
	cwd = os.getcwd()
	osm_data_dir = cwd + '\osm_data'+'_'+timestamp
	out_dir = cwd + '\output'
	
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	
	#os.mkdir(osm_data_dir)
	#os.mkdir(out_dir)
	
	
	#get osm data for tasking manager project
	print 'Download OSM data from OpenStreetMap API. This may take some minutes...'	
	cmd = 'python get_tm_osm_data.py '+task_id+' '+osm_data_dir
	os.system(cmd)
	
	
	#merge osm data
	print 'Merge .osm files'
	output_file = osm_data_dir + '\merge_'+timestamp+'.osm'
	cmd = 'python merge_osm_data.py ' + osm_data_dir + ' ' + output_file + ' osm'
	os.system(cmd)
	
	outputAsc = out_dir + '\diff_stats.txt'
	fileout = file(outputAsc, "w")
	header = 'diff_file;nodes_created;nodes_modified;nodes_deleted;ways_created;ways_modified;ways_deleted;buildings_created;buildings_modified;buildings_deleted\n'
	fileout.write(header)
	fileout.close()
	
	sc.enter(900, 1, do_something_else, (sc,))	



s = sched.scheduler(time.time, time.sleep)
s.enter(1, 1, do_something, (s,))
s.run()
