#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 2021

@author: howardwetsman
Aims: To allow an individual user to compare data on their 23andMe report to the frequency data of
the 1000genomes project.
Contributions and credits:
Ensembl API documentation http://grch37.rest.ensembl.org/documentation/info/symbol_lookup
Chris Vaccaro for findkeys https://github.com/ChrisVaccaro
"""
import pandas as pd
import requests
import json

def Get_Header(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        count = 0
        for i in range(len(lines)):
            if '##' in lines[i]:
                count = count+1
    return count

def Get_Gene(symbol):
    """
    derived from code at the Ensembl API documentation website
    http://grch37.rest.ensembl.org/documentation/info/symbol_lookup
    """
    server = "http://grch37.rest.ensembl.org"
    ext = f"/lookup/symbol/homo_sapiens/{symbol}?expand=1"
    r = requests.get(f"{server}{ext}", headers={"Content-Type" : "application/json"})
    if not r.ok:
      return None
    decoded = r.json()
    return decoded


def Find_Keys(node, kv):
    """
    derived from original code by Chris Vaccaro
    """
    if isinstance(node, list):
        for i in node:
            for x in Find_Keys(i, kv):
                yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in Find_Keys(j, kv):
                yield x


#input sample
sample = 'genome_Mickey_Mouse_v2_v3_Full.txt'

# get 23andme data from sample file
header = Get_Header(sample)
df = pd.read_csv(sample,header=header,sep='\t')
print(df)

#allow user to pick a gene
symbol = 'MTHFR'

# get start and stop for that gene


gene_data = Get_Gene(symbol)
if gene_data == None:
    print(f"I'm sorry. I can find nothing on {symbol} right now")
else:
    chrom = list(Find_Keys(gene_data,'seq_region_name'))[0]
    start = list(Find_Keys(gene_data,'start'))[0]
    end = max(list(Find_Keys(gene_data,'end')))
    print(chrom,start,end)

# print(chrom,start, end)

#filter df for that gene

#get frequency data for those SNPs

#present comparison to the person











































#
