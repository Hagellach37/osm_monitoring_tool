#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################

import sys
import os
import time

def get_all_files(directory,extension):

	#create list for all selected files
	selected_files = []
	
	#iterate over all items in directory and check file extension
	for item in os.listdir(directory):
		#change directory
		os.chdir(directory)
		#get file extension of current item
		item_ext = item.split(".")[-1]

		#check whether item is a file and has right file extension
		if os.path.isfile(item) and item_ext == extension:
			selected_files.append(item)

	return selected_files


def main(directory,output_file,extension):
	
	#Take start time
	start_time = time.time()
	
	selected_files = get_all_files(directory,extension)
	cmd_middle = ''
	cmd_suffix = ''
	
	for i in range(0,len(selected_files)):
	
		#copy first file
		if i == 0:	
			filename = directory + '\\' + selected_files[i]
			
			cwd = os.getcwd()
			osmosis = os.path.dirname(cwd) + '\\osmosis-latest\\bin\\osmosis.bat'
			cmd_1 = osmosis + ' --read-xml file="'+filename+'" --sort --write-xml file="'+output_file+'"'
			os.system(cmd_1)
			
		else:
			filename = directory + '\\' + selected_files[i]
			cmd_middle = cmd_middle + '--read-xml file="'+filename+'" --sort '
			cmd_suffix = cmd_suffix + '--merge '
			
			if (i%50 == 0 ) or (i == (len(selected_files)-1)):
				print i
				osmosis = os.path.dirname(cwd) + '\\osmosis-latest\\bin\\osmosis.bat'
				cmd_prefix = osmosis +' --read-xml file="'+output_file+'" --sort '
				cmd = cmd_prefix + cmd_middle + cmd_suffix + ' --write-xml file="'+output_file+'" -q'
				os.system(cmd)
				cmd = ''
				cmd_middle = ''
				cmd_suffix = ''
		
	#Take end time and calculate program run time
	end_time = time.time()
	run_time = end_time - start_time
	
	print '############ END ######################################'
	print '##'
	print '## output file: '+output_file
	print '##'
	print '## runtime: '+str(run_time)+' s'
	print '##'
	print '## B. Herfort, GIScience Research Group'
	print '##'
	print '#######################################################'
	
if __name__ == "__main__":

    #
    # example run : $ python merge_osm_data.py D:/temp/osm_data merge.osm osm
    #

    if len( sys.argv ) != 4: 
        print "[ ERROR ] you must supply 3 arguments: osm_data_directory output_file file_extension"
        sys.exit( 1 )

    main( sys.argv[1], sys.argv[2], sys.argv[3])	
