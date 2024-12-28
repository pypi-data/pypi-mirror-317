#!/usr/bin/env python3

class Edge:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __repr__(self):
        return f"(a = {self.a}, b = {self.b}, c = {self.c})"

    def __str__(self):
        return f"(a = {self.a}, b = {self.b}, c = {self.c})"

    def __eq__(self, o):
        return ((self.a == o.a) and (self.b == o.b))

    def __hash__(self):
        return hash((self.a, self.b))

    def reversed(self):
        return Edge(self.b, self.a, -1)


def handle_edge(edge: Edge, edges: list, in_map: dict) -> None:
    if in_map.__contains__(edge.reversed()):
        inverse_edge_index = in_map[edge.reversed()]
        edges[inverse_edge_index + 1] = edge
    else:
        in_map[edge] = len(edges)
        edges.append(edge)
        edges.append(Edge(-1,-1,-1))  # Dummy edge

"""
Recieve a list of triangles and return a list of internal and external edges
NOTE: The internal edges are repeated
"""
def triangles_to_edges(triangles: list) -> (list, list):
    edges = []
    in_map = {}

    for triangle in triangles:
        # A, B
        edge = Edge(triangle[0], triangle[1], triangle[2])
        handle_edge(edge, edges, in_map)

        # B, C
        edge = Edge(triangle[1], triangle[2], triangle[0])
        handle_edge(edge, edges, in_map)

        # C, A
        edge = Edge(triangle[2], triangle[0], triangle[1])
        handle_edge(edge, edges, in_map)


    internal_edges = []
    external_edges = []
    for i in range(0, len(edges), 2):
        if edges[i+1].a < 0:  # If the second edge is dummy, it is external
            external_edges.append(edges[i])
        else:
            internal_edges.append(edges[i]) # We want both semi-edges
            internal_edges.append(edges[i+1])

    return internal_edges, external_edges


"""
From a triangle mesh, compute the indices for tension and bending springs
"""
def compute_tension_and_bending_spring_indices(triangles: list) -> (list, list):
    internal_edges, external_edges = triangles_to_edges(triangles)
    tension_edges = []
    bending_edges = []

    # All external edges are for tension springs
    for external_edge in external_edges:
        tension_edges.append((external_edge.a, external_edge.b))

    for i in range(0, len(internal_edges), 2):
        eA = internal_edges[i]
        eB = internal_edges[i+1]

        tension_edges.append((eA.a, eA.b))
        bending_edges.append((eA.c, eB.c))

    return tension_edges, bending_edges
