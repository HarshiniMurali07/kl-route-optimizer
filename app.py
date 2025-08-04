import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from dijkstra_module import build_graph, dijkstra_with_priority_queue, build_path

# Page config
st.set_page_config(page_title="KL Route Optimizer", page_icon="🗺️", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🧭 KL City Shortest Path Visualizer")
st.markdown("Use Dijkstra's Algorithm to find the optimal route across KL landmarks — now in a stylish layout!")
st.markdown("---")

# Build graph and get node list
G = build_graph()
nodes = list(G.nodes())

# UI Inputs
col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("📍 Select Starting Point", nodes)
with col2:
    target = st.selectbox("🏁 Select Destination", nodes)

# Run Dijkstra on button click
if st.button("🚦 Compute Shortest Path"):
    if source == target:
        st.warning("⚠️ Source and destination cannot be the same.")
    else:
        distance_map, previous_map = dijkstra_with_priority_queue(G, source)
        path = build_path(previous_map, target)

        if not path:
            st.error("❌ No valid path found.")
        else:
            st.success("✅ Route successfully computed!")
            st.markdown(f"**🛣️ Route:** {' → '.join(path)}")
            st.info(f"**📏 Total Distance:** `{distance_map[target]} units`")

            # Custom fixed layout
            pos = {
                "KLIA": (0, 0),
                "Putrajaya": (1.5, 0),
                "Merdeka 118": (2.5, -1),
                "Berjaya Times Square": (2.5, 1),
                "Petronas Twin Towers": (3.5, 2),
                "Bukit Bintang": (3.5, 0.5),
                "Exchange 106 @ TRX": (4.5, -0.5),
                "Merdeka Square": (4.5, 1.5),
                "KL Tower": (5.5, 1.5),
                "Tabung Haji Tower": (5.5, -0.5),
            }

            fig, ax = plt.subplots(figsize=(10, 8))

            # Draw all nodes and edges
            nx.draw(
                G, pos, ax=ax,
                with_labels=False,
                node_color='black',
                node_size=1000,
                edge_color='black',
                width=2
            )

            # Draw white text labels on black nodes
            for node, (x, y) in pos.items():
                ax.text(
                    x, y + 0.2, node,
                    fontsize=10,
                    color='white',
                    ha='center',
                    va='center',
                    bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3')
                )

            # Add all edge labels
            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9, ax=ax)

            # Highlight the shortest path in red
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3, ax=ax)

            # Caption and layout
            ax.set_title(" Custom Layout – Network Graph of KL City Routes", fontsize=13)
            ax.axis('off')
            st.pyplot(fig)
else:
    st.info("👆 Choose two different points and click the button to begin route planning.")
