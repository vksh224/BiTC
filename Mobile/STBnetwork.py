import pickle
import math
import networkx as nx
import numpy as np
import random
from Mobile.constants import *

def genSTB(fname):
    #Link exist list of format [i, j, s, te, ts]
    P = np.array(pickle.load(open(fname, "rb")))

    #print(P[0])
    #Dimension of P
    S = P.shape
    print ('Dimension of P: ',S)

    #Include temporal links
    includeT = True

    #Initialize flattened
    G = nx.Graph()

    #Add nodes to G. Each node label <nid - time - interface>
    for u in range(S[0]):
        for t in range(S[3]):
            for i in range(S[2]):
                G.add_node(str(u) + '-' + str(t) + '-' + str(i))

    #List of indices such that links exist
    L = np.argwhere(P == 1)

    print(L[0])

    #Construct graph G. The edge weight is the interface.
    for l in L:

        # if l[3] > 4:
        #     continue

        #Include or ignore temporal links
        # if l[0] == l[1] and includeT:
        #     continue

        '''
        for i in range(l[3] + 1,l[4] + 1):
            u = str(l[0]) + '-' + str(l[3]) + '-' + str(l[2])
            v = str(l[1]) + '-' + str(i) + '-' + str(l[2])

            G.add_edge(u,v)
        '''

        u = str(l[0]) + '-' + str(l[3]) + '-' + str(l[2])
        v = str(l[1]) + '-' + str(l[4]) + '-' + str(l[2])

        G.add_edge(u, v)
        if u == v:
            G[u][v]['weight'] = 1
        else:
            G[u][v]['weight'] = M[0]/minBW[l[2]]

    #Add additional spectral edges

    for u in G.nodes():
        for v in G.nodes():
            for s in range(S[2]):
                u_name = str(u).split("-")
                v_name = str(v).split("-")

                #time is same and band is different
                if u_name[0] == v_name[0] == u_name[1] == v_name[1] and u_name[2] != v_name[2]:
                    G.add_edge(u, v)
                    G[u][v]['weight'] = 0

    print ("Number of nodes in STB: ",len(G))
    print ("Number of edges in STB: ",len(G.edges()))
    print("Density of G: ", (2 * len(G.edges())) / (len(G) * (len(G) - 1)))
    print("Link prob at each layer: ", len(G.edges())/(len(G.nodes()) * S[0]))
    print("isConnected", nx.is_connected(G), "\n")
    return G