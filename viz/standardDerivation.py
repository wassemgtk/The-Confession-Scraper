import pandas as pd
import numpy as array
import csv
import math
import numpy as np

df = pd.read_csv('../data/test.csv')
# print df
print 'huhu'
old_date = '  '
list_of_dates = []
for date in df.date:
  if date != old_date:
    values = df.loc[df['date'] == date, 'value']
    list_of_dates.append(values) 
  old_date = date

count_of_dates = len(list_of_dates)

list_of_all_date_sums = []
for datum in list_of_dates:
  sums_of_date = math.fsum(datum)
  list_of_all_date_sums.append(sums_of_date)

average_of_dates = (math.fsum(list_of_all_date_sums)) / count_of_dates

squared_differences_of_sums = []
for sum_date in list_of_all_date_sums:
  print sum_date
  print average_of_dates
  squared_difference = math.exp(sum_date - average_of_dates)
  squared_differences_of_sums.append(squared_difference)


varianz = (math.fsum(squared_differences_of_sums)) / count_of_dates
print varianz

erste_standardAbweichung = math.sqrt(varianz)
print erste_standardAbweichung
