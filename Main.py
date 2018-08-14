from Mobile.STBnetwork import *
from Static.staticNetwork import *
from embedding import *
from degree import *
from otheralgorithms import *
#from plot_graphs import *


def plot_graph(G, filename, fidelity):
    plt.figure()
    plt.title("Nodes: " + str(len(G.nodes())) + " Edges: " + str(len(G.edges())) + " Fidelity: " + str(fidelity))
    nx.draw(G, with_labels=True)
    # plt.xlabel('Degree')
    # plt.ylabel('Number of nodes')
    plt.draw()
    plt.savefig("Plots/" + filename + "_" + str(fidelity) + ".png")
    plt.close()

fidelity = 0

#Mobile Network: Generate STB graph
#W = genSTB("Nodes10/Time10/Day1/LINK_EXISTS.pkl")
#deg(W)

#Static Network: MetroFi
W = create_static_network("Static/metrofi/aps.txt")

print("OriginalDRN: No. of triangles ", len(nx.triangles(W)))
# W = nx.convert_node_labels_to_integers(W,first_label = 0)
# plot_graph(W, "WSN", fidelity)
#nx.write_gml(W, "Static/metrofi.gml")

#W = nx.erdos_renyi_graph(100, 0.25)
#Run other algorithms
# ULCP_W = ULCP(W, "9")
# GrdLCP(W, "9")
# plot_graph(ULCP_W, "ULCP", 0)


#Our algorithm
#Read GRN
GRN = nx.read_gml('Yeast.gml')
GRN = GRN.reverse()
GRN = nx.convert_node_labels_to_integers(GRN,first_label = 0)

print("\nNumber of nodes in GRN: ", len(GRN))
print("Number of edges in GRN: ", len(GRN.edges()))

#Calculate rank vectors
r_g = nx.pagerank(GRN)
r_w = nx.pagerank(W)

#Mapped graph
MW,E,_,_ = embed_map(GRN,W,r_g,r_w,fidelity)

MW_graph = nx.Graph()
MW_graph.add_nodes_from(MW)
MW_graph.add_edges_from(E)

print ("MappedDRN: Nodes ", len(MW))
print ("MappedDRN: Edges ", len(E))
print("MappedDRN: is connected ", nx.is_connected(MW_graph))
print("MappedDRN: No. of triangles ", len(nx.triangles(MW_graph)))
# plot_graph(MW_graph, "MW", fidelity)








