import heapq
import networkx as nx

def build_graph():
    G = nx.DiGraph()
    edges = [
        ('KLIA', 'Putrajaya', 30),
        ('Putrajaya', 'Berjaya Times Square', 30),
        ('Putrajaya', 'Merdeka 118', 15),
        ('Merdeka 118', 'Berjaya Times Square', 10),
        ('Merdeka 118', 'Exchange 106 @ TRX', 8),
        ('Berjaya Times Square', 'Petronas Twin Towers', 20),
        ('Petronas Twin Towers', 'Merdeka Square', 20),
        ('Merdeka Square', 'KL Tower', 15),
        ('Berjaya Times Square', 'Bukit Bintang', 10),
        ('Bukit Bintang', 'Exchange 106 @ TRX', 5),
        ('Bukit Bintang', 'Merdeka Square', 3),
        ('Exchange 106 @ TRX', 'Tabung Haji Tower', 20),
        ('KL Tower', 'Tabung Haji Tower', 30)
    ]
    G.add_weighted_edges_from(edges)
    return G

def dijkstra_with_priority_queue(G, source):
    distance = {node: float('inf') for node in G.nodes}
    previous = {node: None for node in G.nodes}
    distance[source] = 0
    queue = [(0, source)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        for neighbor in G.neighbors(current_node):
            weight = G[current_node][neighbor]['weight']
            alt = distance[current_node] + weight
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                previous[neighbor] = current_node
                heapq.heappush(queue, (alt, neighbor))
    return distance, previous

def build_path(previous, target):
    path = []
    while target is not None:
        path.insert(0, target)
        target = previous[target]
    return path
