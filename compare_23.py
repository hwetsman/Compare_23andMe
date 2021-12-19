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
import urllib.request


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
    r = requests.get(f"{server}{ext}", headers={"Content-Type": "application/json"})
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


def Get_Ref_Alt(snp):
    with open('frequency_table.tsv') as f:
        for i in range(9):
            line = f.readline()
            # print(line)
            if 'Alleles' in line:
                if '/' in line:
                    alleles = line.split('\t')[1].split('/')[0]
                else:
                    alleles = line.split('\t')[1]
                # print(alleles)
                ref, alt = alleles.split('>')
    return ref, alt.strip()


def Get_Freq(snp):
    freq_df = pd.read_csv(destination, sep='\t', header=12)
    global_alt = freq_df.loc[0, 'Alt Allele'].split('=')[1]
    return global_alt


# input sample
sample = 'genome_Mickey_Mouse_v2_v3_Full.txt'

# get 23andme data from sample file
header = Get_Header(sample)
df = pd.read_csv(sample, header=header, sep='\t', dtype={
                 '# rsid': str, 'chromosome': str, 'position': int, 'genotype': str})

# allow user to pick a gene
symbol = 'MTHFR'

# get start and stop for that gene
print(f"Looking for data on {symbol}... ")
gene_data = Get_Gene(symbol)
if gene_data == None:
    print(f"I'm sorry. I can find nothing on {symbol} right now")
else:
    chrom = list(Find_Keys(gene_data, 'seq_region_name'))[0]
    start = list(Find_Keys(gene_data, 'start'))[0]
    end = max(list(Find_Keys(gene_data, 'end')))

# print(chrom,start, end)
print(
    f"The gene you're looking for is on chromosome {chrom} and goes from position {start} to position {end}")

# filter df for that gene and no calls
df = df[(df.chromosome == chrom) & (df.position <= end) & (df.position >= start)]
df = df[df.genotype != '--']
df = df[~df['# rsid'].str.contains('i')]
print(df)

# get frequency data for those SNPs
snps = df['# rsid'].tolist()
df.set_index('# rsid', inplace=True, drop=True)
print(f"There is data on {len(snps)} SNPs in your report from {symbol}.")
print('It takes a few seconds per SNP:')
for snp in snps:
    print('\n', snp)
    url = f"https://www.ncbi.nlm.nih.gov/snp/{snp}/download/frequency"
    destination = "frequency_table.tsv"
    # freq_filename = str(rsid)
    urllib.request.urlretrieve(url, destination)
    try:
        df.loc[snp, 'alt_freq'] = Get_Freq(snp)
        ref, alt = Get_Ref_Alt(snp)
        df.loc[snp, 'ref'] = ref
        df.loc[snp, 'alt'] = alt
    except:
        ref, alt = Get_Ref_Alt(snp)
        df.loc[snp, 'ref'] = ref
        df.loc[snp, 'alt'] = alt


# present comparison to the person
print(df)
df.to_csv('output.csv', index=False)

non_wild = df[df.genotype != (df.ref + df.ref)]


#
