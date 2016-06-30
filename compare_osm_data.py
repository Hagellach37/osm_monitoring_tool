#!/bin/python
# -*- coding: UTF-8 -*-
# Author: B. Herfort, 2016, GIScience Heidelberg
###########################################

import sys
import os

def main(t1_osm,t2_osm,out_file):
	
	cwd = os.getcwd()
	osmosis = cwd + '\\osmosis-latest\\bin\\osmosis.bat'
	print osmosis
	
	cmd = osmosis + ' --read-xml file="'+t1_osm+ '" --sort --read-xml file="'+t2_osm+'" --sort --derive-change --write-xml-change file="'+out_file+'"'
	
	os.system(cmd)


if __name__ == "__main__":

    #
    # example run : $ python compare_osm_data.py time1.osm time2.osm diff_2.osc
    #

    if len( sys.argv ) != 4: 
        print "[ ERROR ] you must supply 3 arguments: time1.osm time2.osm out_file"
        sys.exit( 1 )

    main( sys.argv[1], sys.argv[2], sys.argv[3] )
