#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 2021

@author: howardwetsman
Aims: To allow an individual user to compare data on their 23andMe report to the frequency data of
the 1000genomes project.
Contributions and credits:
Ensembl API documentation http://grch37.rest.ensembl.org/documentation/info/symbol_lookup
"""
import pandas as pd
import requests

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

sample = 'genome_Mickey_Mouse_v2_v3_Full.txt'

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
    print(gene_data)


#filter df for that gene

#get frequency data for those SNPs

#present comparison to the person











































#
