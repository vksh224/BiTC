from Mobile.STB import *
from Static.staticNetwork import *
from embedding import *
from degree import *

#Read GRN
GRN = nx.read_gml('Yeast.gml')
GRN = GRN.reverse()
GRN = nx.convert_node_labels_to_integers(GRN,first_label = 0)

print("Number of nodes in GRN: ", len(GRN))
print("Number of edges in GRN: ", len(GRN.edges()))


#Mobile Network: Generate STB graph
#W = genSTB("Nodes10/Time5/Day1/LINK_EXISTS.pkl")

#Static Network: MetroFi
W = create_static_network("Static/metrofi/aps.txt")
deg(W)

#Calculate rank vectors
r_g = nx.pagerank(GRN)
#print (len(r_g))

r_w = nx.pagerank(W)

#Mapped graph
MW,E,_,_ = embed_map(GRN,W,r_g,r_w,0.9)
#deg(MW)

print ("Mapped DRN ", len(MW),len(E))



