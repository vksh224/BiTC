from computeHarvesine import *
import networkx as nx

def create_static_network(filename):
    wifi_range = 1000

    with open(filename) as f:
        apslocations = f.readlines()

    #Initialize graph
    G = nx.Graph()

    # add nodes
    for ap in apslocations:
        mac_id = ap.split()
        G.add_node(mac_id[0])

    #add edges
    for ap1 in apslocations:
        ap1_arr = ap1.split()
        u = ap1_arr[0]
        lat1 = ap1_arr[1]
        lon1 = ap1_arr[2]

        for ap2 in apslocations:
            ap2_arr = ap2.split()
            v = ap2_arr[0]
            lat2 = ap2_arr[1]
            lon2 = ap2_arr[2]

            dist = funHaversine(float(lon1), float(lat1), float(lon2), float(lat2))

            if dist <= wifi_range:
                G.add_edge(u, v)

    print ("Number of nodes in G: ",len(G))
    print ("Number of edges in G: ",len(G.edges()))
    print ("Density of G: ",(2 * len(G.edges()))/(len(G) * (len(G) - 1)))

