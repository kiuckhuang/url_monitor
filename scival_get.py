#!/usr/bin/python3

import requests
import json
import re
import sys, getopt
import os.path
from os import path
import math

max_per_request = 100

def main(argv):
    inputfile = ''
    outputfile = ''
    syntax_msg = 'python ' + os.path.basename(__file__) + ' -i <inputfile> -o <outputfile>'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(syntax_msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(syntax_msg)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Input file is:', inputfile)
    print('Output file is:', outputfile)

    if(not path.exists(inputfile)):
        print(syntax_msg)
        sys.exit()

    lines = []
    with open(inputfile) as f:
        lines = f.read().splitlines()

    for i in range(0, math.floor( len(lines) / max_per_request) + 1 ):
        index_start = i * max_per_request
        index_end = (i+1) * max_per_request
        if index_end > len(lines):
           index_end = len(lines) 
        print(str(index_start) + ":" + str(index_end))
        print(lines[index_start:index_end])
    #url_source = 'https://services.nvd.nist.gov/rest/json/cves/2.0'
    #cves = json.loads(requests.get(url_source).text)
    #print(cves["resultsPerPage"], cves['timestamp']);



if __name__ == "__main__":
   main(sys.argv[1:])