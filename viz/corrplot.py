import pandas as pd
import numpy as array
import csv
import math
import numpy as np
import string
from biokit.viz import corrplot

df2 = pd.read_csv('../data/BigRedConfessions_output/BigRedConfessions_Emotions_posts.csv')

df = df2
print df

df = df.drop('date', 1)

letters = string.uppercase[0:15]
df = df.corr()
# print df


c = corrplot.Corrplot(df)
c.plot()