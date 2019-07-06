import glob

import pandas as pd


path = r'/Users/neiellcare/Documents/scrapy_projects/cpaaustralia_com' # use your path
all_files = glob.glob(path + "/cpaaustralia-*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

data = pd.concat(li, axis=0, ignore_index=True, sort=True)

data.drop_duplicates(subset="phone", keep='last')
data.to_csv("final_data.csv", index=False, encoding='utf-8')