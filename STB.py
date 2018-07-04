import pickle
import networkx as nx
import numpy as np

def genSTB(fname):
    #Link exist list of format [i, j, s, te, ts]
    P = np.array(pickle.load(open(fname, "rb")))

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

            if t > 4:
                continue

            for i in range(S[2]):
                G.add_node(str(u) + '-' + str(t) + '-' + str(i))

    #List of indices such that links exist
    L = np.argwhere(P == 1)

    #Construct graph G. The edge weight is the interface.
    for l in L:

        if l[3] > 4:
            continue


        #Include or ignore temporal links
        if l[0] == l[1] and not includeT:
            continue

        '''
        for i in range(l[3] + 1,l[4] + 1):
            u = str(l[0]) + '-' + str(l[3]) + '-' + str(l[2])
            v = str(l[1]) + '-' + str(i) + '-' + str(l[2])

            G.add_edge(u,v)
        '''

        u = str(l[0]) + '-' + str(l[3]) + '-' + str(l[2])
        v = str(l[1]) + '-' + str(l[4]) + '-' + str(l[2])

        G.add_edge(u, v)

    print ("Number of nodes in STB: ",len(G))
    print ("Number of edges in STB: ",len(G.edges()))

    return G