#!/usr/bin/env python

import requests

# get the csv files for all the election IDs
for line in open("ELECTION_ID.txt","r"):
    ID = line.split()[1]
    year = line.split()[0]
    resp = requests.get("http://historical.elections.virginia.gov/elections/download/"+ID+"/precincts_include:0/")
    file_name = "president_general_" + year + ".csv"
    with open(file_name, "w") as out: # save the csv files
        out.write(resp.text)
