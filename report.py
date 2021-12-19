import pandas as pd

df = pd.read_csv('output.csv')
print(df)
# extract non_wild SNPs
non_wild = df[df.genotype != (df.ref + df.ref)]
print(non_wild)
