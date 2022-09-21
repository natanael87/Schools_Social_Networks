# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 17:55:16 2014

@author: elias
"""
import networkx as nx
import igraph as ig
import numpy as np
import random
import matplotlib.pyplot as plt
import math as ma

def short_cuts(g, p, k):
    enlaces=g.get_edgelist()
    nodos=np.arange(g.vcount())
    for i in range(len(enlaces)):
        if random.random()<p[k]:
            u=random.choice(nodos)
            v=random.choice(nodos)
            while u==v or g.are_connected(u,v):
                v=random.choice(nodos)
            g.add_edges((u,v))
            g.delete_edges(g.get_eid(*enlaces[i]))