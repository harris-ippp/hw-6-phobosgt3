#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup as bs

# grab the data from HP
resp = requests.get("http://historical.elections.virginia.gov/elections/search/year_from:1924/year_to:2016/office_id:1/stage:General")
soup = bs(resp.content, "html.parser")

# Election IDs are stored in the table rows whose class is "election_item".
row = soup.find_all("tr", class_="election_item")
ID = [x.get("id").split("-")[2] for x in row]

# The years of elections are stored in the table cells whose class is "year first".
year = [x.find("td",class_="year first").string for x in row]

# save a text file including the data of IDs and years
with open("ELECTION_ID.txt","w") as output:
    for (a,b) in zip(year, ID):
        print(a,b)
        output.write(a+" "+b+"\n")
