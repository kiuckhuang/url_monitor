#!/usr/bin/python3

import requests
import json
import re
import sys, getopt
import os.path
from os import path
import math
from time import sleep
from random import randint
import pandas as pd


# max number of author ids
max_per_request = 100

# set the apiKey here
url_paras = {
    'apiKey': '7f59af901d2d86f78a1fd60c1bf9426a',
    'indexType': 'hIndex',
    'httpAccept': 'application/json',
    'authors': ''
}

# set the request output to json
request_headers = {
    'Accept': 'application/json'
}

# search urls
request_urls = {
    'Academic_Corporate_Collaboration_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=AcademicCorporateCollaboration&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false',
    'Collaboration_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=Collaboration&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false',
    'Citations_Per_Publication_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=CitationsPerPublication&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false',
    'Cited_Publications_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=CitedPublications&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=false',
    'Cited_Publications_all_years':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=CitationCount&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'Field_Weighted_Citation_Impact_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=FieldWeightedCitationImpact&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'HIndex_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=HIndices&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'HIndex_all_years':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=HIndices&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'ScholarlyOutput_2017-2022_by_year':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=ScholarlyOutput&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=true&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'ScholarlyOutput_all_years':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=ScholarlyOutput&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'Pubs_Top_Percentile_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=PublicationsInTopJournalPercentiles&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
    'Outputs_Top_Percentile_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=OutputsInTopCitationPercentiles&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true'
}

# testing for 1 url
#request_urls = {
#    'Pubs_Top_Percentile_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=PublicationsInTopJournalPercentiles&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true',
#    'Outputs_Top_Percentile_2017-2022':'https://api.elsevier.com/analytics/scival/author/metrics?metricTypes=OutputsInTopCitationPercentiles&yearRange=5yrsAndCurrent&includeSelfCitations=true&byYear=false&includedDocs=AllPublicationTypes&journalImpactType=CiteScore&showAsFieldWeighted=true'
#}

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

    json_all = pd.DataFrame()
    for myname, url_prefix in request_urls.items():
        json_metric = pd.DataFrame()
        
        for i in range(0, math.floor( len(lines) / max_per_request) + 1 ):
            index_start = i * max_per_request
            index_end = (i+1) * max_per_request
            if index_end > len(lines):
                index_end = len(lines) 

            #print(str(index_start) + ":" + str(index_end))
            url_paras['authors'] = ','.join(lines[index_start:index_end])
            p = requests.models.PreparedRequest()

            p.prepare_url(url=url_prefix, params=url_paras)
            #print(p.url)
            json_dict = json.loads(requests.get(p.url, headers=request_headers).text)
            json_results = pd.json_normalize(json_dict['results'])
            json_metric = pd.concat([json_metric, json_results], axis=0, ignore_index=True)
            #print(json_metric)
        
        json_metric = json_metric.drop(['author.link.@ref', 'author.link.@href', 'author.link.@type', 'author.uri'], axis=1)
        json_metric.columns = [myname, 'author.id', 'author.name']
        json_metric = json_metric[['author.id', 'author.name', myname]]
        #print(json_metric)
        json_metric.set_index('author.id')
        print(json_all.size)
        if json_all.size == 0:
            json_all = json_metric
        else:
            json_all= json_all.merge(json_metric, how='left', on=['author.id', 'author.name'])
        #print(json_all)
        sleep(randint(100,200)/100)

    #print(json_all)
    with open(outputfile, 'w') as ofile:
        result = json_all.to_json(orient="table", index=False)
        json.dump(json.loads(result), ofile, indent=4)
        print('Saved to:', outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])