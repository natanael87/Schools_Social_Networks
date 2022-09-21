00282 def watts_strogatz_graph(n, k, p, seed=None):
00283     """
00284     Return a Watts-Strogatz small world graph.
00285 
00286     First create a ring over n nodes.  Then each node in the ring is
00287     connected with its k nearest neighbors (k-1 neighbors if k is odd).  
00288     Then shortcuts are created by rewiring existing edges as follows: 
00289     for each edge u-v in the underlying "n-ring with k nearest neighbors" 
00290     with probability p replace u-v with a new edge u-w with 
00291     randomly-chosen existing node w. In contrast with
00292     newman_watts_strogatz_graph(), the random rewiring does not
00293     increase the number of edges.
00294     
00295 
00296     :Parameters:
00297       - `n`: the number of nodes
00298       - `k`: each node is connected to k neighbors in the ring topology
00299       - `p`: the probability of rewiring an edge
00300       - `seed`: seed for random number generator (default=None)
00301       
00302     """
00303     if seed is not None:
00304         random.seed(seed)
00305     G=empty_graph(n)
00306     G.name="watts_strogatz_graph(%s,%s,%s)"%(n,k,p)
00307     nlist = G.nodes()
00308     fromv = nlist
00309     # connect the k/2 neighbors
00310     for n in range(1, k/2+1):
00311         tov = fromv[n:] + fromv[0:n] # the first n are now last
00312         for i in range(len(fromv)):
00313             G.add_edge(fromv[i], tov[i])
00314     # for each edge u-v, with probability p, randomly replace with
00315     # edge u-w
00316     e = G.edges()
00317     for (u, v) in e:
00318         if random.random() < p:
00319             newv = random.choice(nlist)
00320             # avoid self-loops and reject if edge u-newv exists
00321             # is that the correct WS model?
00322             while newv == u or G.has_edge(u, newv): 
00323                 newv = random.choice(nlist)
00324             G.delete_edge(u,v)  # conserve number of edges 
00325             G.add_edge(u,newv)
00326     return G     
