import networkx as nx

from STB import *
from embedding import *
from degree import *

#Read GRN
GRN = nx.read_gml('Yeast.gml')
GRN = GRN.reverse()
GRN = nx.convert_node_labels_to_integers(GRN,first_label = 0)

print("Number of nodes in GRN: ", len(GRN))
print("Number of edges in GRN: ", len(GRN.edges()))

#Generate STB graph
W = genSTB("Nodes10/Time2/Day1/LINK_EXISTS.pkl")
# deg(W)


#Calculate rank vectors
r_g = nx.pagerank(GRN)
#print (len(r_g))

r_w = nx.pagerank(W)
#print (len(r_w))

#Mapped graph
MW,E,_,_ = embed_map(GRN,W,r_g,r_w,0.4)
#deg(MW)

print ("Mapped DRN ", len(MW),len(E))



