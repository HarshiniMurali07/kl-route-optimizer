import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from dijkstra_module import build_graph, dijkstra_with_priority_queue, build_path

# Page config
st.set_page_config(page_title="KL City Route Optimizer", page_icon="🗺️", layout="wide")

# Custom title layout
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("## 🏙️ KL City Route Optimizer")
    st.caption("🚀 Find the shortest path between landmarks using Dijkstra's Algorithm")

st.markdown("---")

# Load graph
G = build_graph()
nodes = list(G.nodes())

# User input: source and target
col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("📍 Select Starting Point", nodes)
with col2:
    target = st.selectbox("🏁 Select Destination", nodes)

# Button to find path
if st.button("🔍 Compute Shortest Path"):
    if source == target:
        st.warning("Source and destination cannot be the same.")
    else:
        distance, previous = dijkstra_with_priority_queue(G, source)
        path = build_path(previous, target)

        if not path:
            st.error("❌ No path found.")
        else:
            st.success("✅ Shortest path found!")
            st.markdown(f"**Path:** {' → '.join(path)}")
            st.markdown(f"**Total Distance:** `{distance[target]} units`")

            # Visualize the path
            pos = nx.spring_layout(G, seed=42)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]

            plt.figure(figsize=(12, 8))
            nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, edge_color='gray')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3)

            st.pyplot(plt.gcf())
            plt.clf()
