import pandas as pd

df = pd.read_csv('output.csv')
print(df)
non_wild = df[df.genotype != (df.ref + df.ref)]
print(non_wild)
