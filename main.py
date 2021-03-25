
import json
from py2neo import Graph
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "1234"))
null =None
with open('./codebeautify.json', encoding='utf-8') as f:

	# print(f)
	json_data = json.load(f)
f.close()



def addNode(data):
	query = "create(n"

	#labels
	labels = data["Label"]
	if type(labels) == list:
		for label in labels:
		    query += ":"+label

	#properties
	properties = list(data["Property"].keys())
	values = data["Property"]
	if(len(properties)>0):
		query += ":Property{" + properties[0] + ':"' + values[properties[0]] + '"'
	for key in range(1, len(properties)):
		query += ", " + properties[key] + ':"' + (values[properties[key]]) + '"'

	#other properties
	# for key in data:
	#   if(key!="Label" and key!="Property" and key!="Kind"):
	#     query += ", " + key + ':"' + data[key] + '"'

	query += "})"

	# if(len(query)>0):
	# print(query)
	graph.run(query)

def addRelation(data):
	query = "MATCH (node1:"+data["FromLabel"]+"),(node2:"+data["ToLabel"]+") CREATE (node1)-[relation"
	midQuery = " "
	endQuery = "]->(node2) RETURN relation"
	#labels
	labels = data["Label"]
	if type(labels) == list:
		for label in labels:
		    midQuery += ":"+label

	#properties
	properties = list(data["Property"].keys())
	values = data["Property"]
	if(len(properties)>0):
		midQuery += ":"+str(data.get('Type')) +"{" + properties[0] + ':"' + values[properties[0]] + '"'
	for key in range(1, len(properties)):
		midQuery += ", " + properties[key] + ':"' + (values[properties[key]]) + '"'

	#other properties
	# for key in data:
	#   if(key!="Label" and key!="Property" and key!="Kind"):
	#     midQuery += ", " + key + ':"' + data[key] + '"'

	midQuery += "}"
	query += midQuery+endQuery
	# print(query)
	graph.run(query)

for data in json_data:
	if data["Kind"]=="node":
		addNode(data)
	if data["Kind"]=="relationship":
		addRelation(data)
		
# MATCH (<node1-label-name>:<node1-name>),(<node2-label-name>:<node2-name>)
# CREATE  
# 	(<node1-label-name>)-[<relationship-label-name>:<relationship-name>
# 	{<define-properties-list>}]->(<node2-label-name>)
# RETURN <relationship-label-name>

