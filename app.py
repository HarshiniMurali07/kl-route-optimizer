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
    h1, h2, h3 { color: #1a1a1a; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.title("🧭 KL City Shortest Path Visualizer")

# Tabs for multi-section layout
tabs = st.tabs(["🏠 Home", "📍 Route Planner", "🧠 Why Dijkstra?", "📊 Algorithm Comparison"])

# ---------------------------- HOME TAB ---------------------------- #
with tabs[0]:
    st.header("Welcome to the KL City Route Optimizer")
    st.markdown("""
    Plan your journey through Kuala Lumpur's iconic landmarks with smart, efficient routing. 
    This tool helps you identify the shortest path between major city locations using the precision of Dijkstra’s Algorithm.

    Whether you're navigating for tourism, logistics, or learning purposes — see your path come to life in a graph, calculated with speed and accuracy.

    Learn the science behind the scenes and explore how route optimization algorithms like Dijkstra power real-time navigation across the world.
    """)
    st.image("istockphoto-521417678-612x612.jpg", caption="Map of Greater Kuala Lumpur", use_container_width=True)

# ---------------------------- ROUTE PLANNER TAB ---------------------------- #
with tabs[1]:
    G = build_graph()
    nodes = list(G.nodes())

    col1, col2 = st.columns(2)
    with col1:
        source = st.selectbox("📍 Select Starting Point", nodes)
    with col2:
        target = st.selectbox("🏁 Select Destination", nodes)

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
                nx.draw(G, pos, ax=ax, with_labels=False, node_color='black', node_size=1000, edge_color='black', width=2)
                for node, (x, y) in pos.items():
                    ax.text(x, y + 0.2, node, fontsize=10, color='white', ha='center', va='center',
                            bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))
                edge_labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9, ax=ax)
                path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='crimson', width=3, ax=ax)
                ax.set_title("📌 Network Graph of KL Routes", fontsize=13)
                ax.axis('off')
                st.pyplot(fig)
    else:
        st.info("👆 Choose two different points and click the button to begin route planning.")

# ---------------------------- WHY DIJKSTRA TAB ---------------------------- #
with tabs[2]:
    st.header("🧠 Why Dijkstra's Algorithm?")
    st.markdown("""
    Dijkstra’s Algorithm is one of the most widely adopted and trusted techniques for shortest path calculation. It’s the silent brain behind many digital maps, logistics platforms, and real-time navigation tools.
    """)

    st.subheader("💡 What Is Dijkstra's Algorithm?")
    st.markdown("""
    Dijkstra’s algorithm is a greedy method to find the shortest path from a source to all nodes in a graph with non-negative edge weights.

    - It explores nodes in increasing order of distance from the source.
    - It uses a **priority queue** to efficiently select the next closest node.
    - It guarantees an **optimal path** when all weights are positive.
    """)

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif",
        caption="Visualization of Dijkstra's Algorithm",
        use_container_width=True
    )

    st.subheader("🌍 Where It's Used")
    st.markdown("""
    - Google Maps, Waze, Uber for route planning
    - Amazon and logistics routing
    - Network routing protocols (e.g., OSPF)
    """)

    st.subheader("📊 Performance Overview")
    st.markdown("""
    | Metric                 | Value                   |
    |------------------------|--------------------------|
    | Time Complexity        | O((V + E) log V)         |
    | Handles Neg. Weights   | No                      |
    | Ideal For              | Sparse graphs, real-time pathfinding |
    """)

    st.success("Dijkstra is chosen for this project due to its efficiency, reliability, and real-world relevance.")

# ---------------------------- COMPARISON TAB ---------------------------- #
with tabs[3]:
    st.header("📊 Algorithm Comparison")
    st.markdown("Compare popular shortest path algorithms based on performance and suitability.")

    comparison_data = {
        "Algorithm": [
            "Dijkstra",
            "Bellman-Ford",
            "Floyd-Warshall",
            "A* Search",
            "BFS (Unweighted)",
            "DFS (Unweighted)"
        ],
        "Handles Negative Weights": [
            "No",
            "Yes",
            "Yes",
            "No",
            "No",
            "No"
        ],
        "Time Complexity": [
            "O((V + E) log V)",
            "O(V × E)",
            "O(V³)",
            "O((V + E) log V)",
            "O(V + E)",
            "O(V + E)"
        ],
        "Best For": [
            "Sparse graphs, GPS navigation",
            "Graphs with negative weights",
            "All-pairs path finding",
            "Heuristic-based search",
            "Unweighted quick lookup",
            "Exploration without shortest path guarantee"
        ]
    }

    st.dataframe(comparison_data, use_container_width=True)
    st.image("https://miro.medium.com/v2/resize:fit:1400/format:webp/1*jw2nHPGk3nVZTZo2xcpV0g.png", caption="Visual Summary of Algorithm Complexity", use_container_width=True)

