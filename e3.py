#!/usr/bin/env python

import pandas as pd

# set up the columns for a year(2004)
header = pd.read_csv("president_general_2004.csv", nrows = 1).dropna(axis = 1)
d = header.iloc[0].to_dict()

df = pd.read_csv("president_general_2004.csv", index_col = 0,
               thousands = ",", skiprows = [1])

df.rename(inplace = True, columns = d) # rename to democrat/republican
df.dropna(inplace = True, axis = 1)    # drop empty columns

df.index = df.index.str.replace("\ \(CD\ .\)","")
df = df.groupby(df.index).sum() # group the data of districts with "CD-"

df["Year"] = 2004

# combine the dataframes of all the elections, using a for loop
for line in open("ELECTION_ID.txt","r"):
    year = line.split()[0]
    if year == "2004": continue # already have a dataframe for 2004 election
    header = pd.read_csv("president_general_"+year+".csv", nrows = 1).dropna(axis = 1)
    d = header.iloc[0].to_dict()
    df2 = pd.read_csv("president_general_"+year+".csv", index_col = 0,
               thousands = ",", skiprows = [1])
    df2.rename(inplace = True, columns = d)
    df2.dropna(inplace = True, axis = 1)
    df2.index = df2.index.str.replace("\ \(CD\ .\)","")
    df2 = df2.groupby(df2.index).sum()
    df2["Year"] = int(year)
    df = pd.concat([df,df2], axis=0 , join='inner')

# creat a new dataframe which shows the trend of Republican Share in each district
df = df.sort_values(by="Year")
del df["All Others"]
df["Republican Share"] = 100 * df["Republican"] / df["Total Votes Cast"]
trend = df.pivot(columns='Year', values='Republican Share')

# plot the data for four counties
graph1 = trend.loc["Accomack County"].plot(title = "Accomack County")
graph1.set_xlabel("Year")
graph1.set_ylabel("Republican Share")
graph1.figure.savefig("accomack_county.pdf")

graph2 = trend.loc["Albemarle County"].plot(fontsize = 8, title = "Albemarle County")
graph2.set_xlabel("Year")
graph2.set_ylabel("Republican Share")
graph2.figure.savefig("albemarle_county.pdf")

graph3 = trend.loc["Alexandria City"].plot(fontsize = 8, title = "Alexandria City")
graph3.set_xlabel("Year")
graph3.set_ylabel("Republican Share")
graph3.figure.savefig("alexandria_city.pdf")

graph4 = trend.loc["Alleghany County"].plot(fontsize = 8, title = "Alleghany County")
graph4.set_xlabel("Year")
graph4.set_ylabel("Republican Share")
graph4.figure.savefig("alleghany_county.pdf")
