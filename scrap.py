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

os.chdir("/home/user")
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
    if "hsa" == line[:3] and len(current["proteins"])!=0:
        # we ended ele chunk append to brit
        brit_dict[node_name] = current
        current = dict(proteins=[])
    if "hsa" == line[:3]:
        node_name = line
    if "up:" in line:
        current["proteins"].append(line.strip())
    print("prog {}".format(i/len(lines_list)))

[name for name in brit_dict if len(brit_dict[name]["proteins"])> 1]

print(brit_dict)
original = brit_dict.copy()
backup = brit_dict.copy()

brit_dict = backup.copy()

for k in brit_dict:
    print(len(brit_dict[k]["proteins"]))

## sanity check that multiple subproteins can actually be found
one_prot = brit_dict[list(brit_dict.keys())[0]]["proteins"]
another_prot = brit_dict[list(brit_dict.keys())[1]]["proteins"]
set(one_prot).intersection(set(another_prot))
another_prot    
set(one_prot).intersection(set(another_prot)) == set(brit_dict[list(brit_dict.keys())[0]]["edges"][list(brit_dict.keys())[1]])

## only export a small part
sub = {}
for k in list(brit_dict.keys())[0]:
    sub[k] = brit_dict[k]

sub[list(brit_dict.keys())[0]] = brit_dict[list(brit_dict.keys())[0]]


with open("./testing/public/subtest.json","w") as phile:
    phile.write(json.dumps(sub))

##set overlap counter
for i,current_node in enumerate(brit_dict):
    current_proteins = brit_dict[current_node]["proteins"]
    edges = {}
    for other_node in brit_dict:
        if other_node == current_node:
            continue
        other_proteins = brit_dict[other_node]["proteins"]
        print(len(current_proteins),len(other_proteins))
        overlap = set(current_proteins).intersection(other_proteins)
        if len(overlap)!= 0:
            edges[other_node] =list(overlap)
    brit_dict[current_node]["edges"] = edges

import pprint
pp = pprint.PrettyPrinter()
pp.pprint(brit_dict)

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

with open("./testing/public/bio.json","w") as phile:
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
        for edge in brit_dict[node]["edges"][other_node]:
            dot.edge(node,other_node,edge,concentrate="true")

## get the graphviz in path

os.environ["PATH"]+=os.pathsep + "/home/user/miniconda3/pkgs/graphviz-2.40.1-h21bd128_2/bin"

dot.render("test.gv",format="svg")

##make a test
brit_dict = dict(cat1 = dict(proteins=[2,5]),cat2 = dict(proteins=[4,2,8,5]),cat3 =dict(proteins=[8,4,1]))
brit_dict_copy = brit_dict.copy()
##set overlap counter
for i,current_node in enumerate(brit_dict_copy):
    current_proteins = brit_dict_copy[current_node]["proteins"]
    edges = {}
    for other_node in brit_dict_copy:
        if other_node == current_node:
            continue
        other_proteins = brit_dict_copy[other_node]["proteins"]
        overlap = set(current_proteins).intersection(other_proteins)
        if len(overlap)!= 0:
            edges[other_node] =list(overlap)
    brit_dict_copy[current_node]["edges"] = edges

brit_dict_copy

import json
with open("./testing/public/test.json","w") as phile:
    phile.write(json.dumps(brit_dict_copy))



 set(["there is a list of words","another"]).intersection(set(["another","there is a list of words"]))