#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 2021

@author: howardwetsman
Aims: To allow an individual user to compare data on their 23andMe report to the frequency data of
the 1000genomes project.

"""
import pandas as pd


def Get_Header(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        count = 0
        for i in range(len(lines)):
            if '##' in lines[i]:
                count = count+1
    return count


sample = 'genome_Mickey_Mouse_v2_v3_Full.txt'

header = Get_Header(sample)
df = pd.read_csv(sample,header=header,sep='\t')
print(df)

#allow user to pick a gene

#filter df for that gene

#get frequency data for those SNPs

#present comparison to the person











































#
