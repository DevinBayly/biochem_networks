import os
import json
import requests

## load brittany's data
parenturl = "1KGRMwndK3o5mvGgWrkVjBpp1ng_ZXYCQ"

url = "https://www.googleapis.com/drive/v3/files/?key=AIzaSyC5TwUDONA6mxYRM3JnQLStSb0bnh6rI2o&q='{}'+in+parents&fields=files(*)".format(parenturl)
url
res = requests.get(url)
res.content

content =res.content.decode()
print(content)
content_dict = json.loads(content)
ids = [[f["name"],f["id"]] for f in content_dict["files"]]
ids

## download these files

def dwnld(name,id):
    url = "https://www.googleapis.com/drive/v3/files/{}?key=AIzaSyC5TwUDONA6mxYRM3JnQLStSb0bnh6rI2o&alt=media".format(id)
    res = requests.get(url)
    with open(name,"wb") as phile:
        phile.write(res.content)

for e in ids:
    dwnld(e[0],e[1])

## reading the files from her workflow
import pandas as pd

os.listdir()

df = pd.read_csv("List_of_Proteins_Enriched_Above1.5.csv")
df.columns 

with open("./UniprotID_to_KEGGID_KEGGPathway_above1.5.txt","r") as  phile:
    brit_contents = phile.read()

lines_list = brit_contents.split("\n")

brit_dict = {}
current = dict(proteins=[])
node_name = ""
state = "node"

for i,line in enumerate(lines_list):
    if line == "":
        continue
    if "hsa" in line and len(current["proteins"])!=0:
        # we ended ele chunk append to brit
        brit_dict[node_name] = current
        current = dict(proteins=[])
    if "hsa" == line[:3]:
        node_name = line
    if "up:" in line:
        current["proteins"].append(line.strip())
    print("prog {}".format(i/len(lines_list)))

print(brit_dict)
original = brit_dict.copy()
backup = brit_dict.copy()

brit_dict = backup.copy()


##not great code, exponential timing algorithm, small number of eles though
for i,count_node in enumerate(brit_dict):
    edges = []
    ## iterate over proteins in list
    for protein in brit_dict[count_node]["proteins"]:
        ##iterate over other nodes
        for edge_node in brit_dict:
            if count_node == edge_node:
                continue
            if protein in brit_dict[edge_node]["proteins"]:
                edges.append(edge_node)
    brit_dict[count_node]["edges"] = edges
    print("percent done {}".format(i/len(brit_dict)))

## create totals for elements and edges, this will help with visuals later

original = brit_dict.copy()
brit_dict = original.copy()


for cat in brit_dict:
    brit_dict[cat]["total_proteins"] = len(brit_dict[cat]["proteins"])
    brit_dict[cat]["total_edges"] = len(brit_dict[cat]["edges"])

with open("biochem_network_graph.json","w") as phile:
    phile.write(json.dumps(brit_dict))


## upload the data back to the drive

import json

import os
import graphviz
from graphviz import Graph, Digraph

with open("biochem_network_graph.json","r") as phile:
    brit_dict = json.loads(phile.read())

dot = Graph(comment="Brittany vis")

for node in brit_dict:
    dot.node(node,node)
    for other_node in brit_dict[node]["edges"]:
        dot.edge(node,other_node,constraint="true")

## get the graphviz in path

os.environ["PATH"]+=os.pathsep + "/home/user/miniconda3/pkgs/graphviz-2.40.1-h21bd128_2/bin"

dot.render("test.gv",format="svg")
