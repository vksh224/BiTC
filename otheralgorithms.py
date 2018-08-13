import networkx as nx

def get_certain_nodes(V, t):
    chosen_nodes = []
    for v in V:
        v_name = str(v).split("-")
        #print(v_name[1])
        if v_name[1] == t:
            chosen_nodes.append(v)

    return chosen_nodes

#Union of Least Cost Path (ULCP) Algorithm
def ULCP(G, t):
    # Initialize graph
    H = nx.Graph()
    H.add_nodes_from(G)

    V = G.nodes()

    layer_start_nodes = get_certain_nodes(V, "0")
    #print(layer_start_nodes, len(layer_start_nodes))

    layer_end_nodes = get_certain_nodes(V, t)
    #print(layer_end_nodes, len(layer_end_nodes))


    for i in layer_start_nodes:
        for j in layer_end_nodes:
            if nx.has_path(G, i, j):
                path = nx.dijkstra_path(G, i, j)
                edges_in_path = zip(path[0:], path[1:])
                for (u, v) in edges_in_path:
                    #print(u, v, end = " ")
                    if H.has_edge(u, v) == False and G.has_edge(u, v):
                        H.add_edge(u, v)
            #print("\n")

    print("ULCP: Nodes ", len(H))
    print("ULCP: Eges", len(H.edges()))
    print("ULCP: E(H)/E(G)", len(H.edges()) / len(G.edges()))
    print("ULCP: isConnected", nx.is_connected(H), "\n")

    return H

#Greedy Algorithm based on Least Cost Path
def GrdLCP(G, t):
    # Initialize graph
    H = nx.Graph()
    H.add_nodes_from(G)

    V = G.nodes()
    #allPaths = all_shortest_paths(G, V)
    layer_start_nodes = get_certain_nodes(V, "0")
    print(layer_start_nodes, len(layer_start_nodes))

    layer_end_nodes = get_certain_nodes(V, t)
    print(layer_end_nodes, len(layer_end_nodes))

    for i in layer_start_nodes:
        for j in layer_end_nodes:
            #print("Path", path)
            if nx.has_path(G, i, j):
                path = nx.dijkstra_path(G, i, j)
                edges_in_path = zip(path[0:], path[1:])
                for (u, v) in edges_in_path:
                    H.add_edge(u, v)
                    G[u][v]["weight"] = 0

    print("GrdLCP: Nodes ", len(H))
    print("GrdLCP: Eges", len(H.edges()))
    print("GrdLCP: E(H)/E(G)", len(H.edges())/len(G.edges()))
    print("GrdLCP: isConnected", nx.is_connected(H))

    return H

