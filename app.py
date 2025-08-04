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
    This tool helps you compute the **shortest route** between major KL landmarks using **Dijkstra's Algorithm**.

    ✅ Visualizes the graph of locations and connections  
    ✅ Computes shortest path and total distance  
    ✅ Highlights the path visually for clarity

    Explore how Dijkstra's algorithm works and why it's used in navigation systems worldwide.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif", caption="How Dijkstra works (Wikipedia GIF)")

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
    Dijkstra’s Algorithm is one of the most trusted and widely-used **shortest path algorithms** in the world.  
    It's the engine behind **GPS apps**, **delivery route planners**, and even **network routing protocols**.
    """)

    st.subheader("💡 What Is Dijkstra's Algorithm?")
    st.markdown("""
    It’s a **greedy algorithm** that finds the shortest path between a starting node and all other nodes in a graph — with non-negative edge weights.

    - It explores paths in increasing order of distance.
    - Uses a **priority queue (min-heap)** to always expand the closest node.
    - Guarantees the optimal shortest path in graphs without negative weights.
    """)

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/5/57/Dijkstra_Animation.gif",
        caption="Visualization of Dijkstra's Algorithm (Source: Wikipedia)",
        use_column_width=True
    )

    st.subheader("🎯 Why Dijkstra Is So Popular")
    st.markdown("""
    - ✅ **Fast and efficient**: Especially with a priority queue.
    - ✅ **Widely supported**: Built into libraries like NetworkX.
    - ✅ **Safe and optimal**: Guarantees the best path if no negative weights.
    - ✅ **Versatile**: Can be used for both static and real-time routing.

    **Used by:**
    - 🚗 Google Maps, Waze, Uber
    - 📦 Amazon Logistics
    - 📶 Computer Networks (e.g., OSPF routing protocol)
    """)

    st.subheader("📊 Performance Overview")
    st.markdown("""
    | Feature                      | Dijkstra              |
    |------------------------------|------------------------|
    | Time Complexity              | `O((V + E) log V)`     |
    | Handles Negative Weights     | ❌ No                  |
    | Real-time Routing            | ✅ Yes                 |
    | Memory Usage                 | Moderate               |
    | Best For                     | Sparse graphs, GPS, logistics |
    """)

    st.subheader("🔍 How Dijkstra Compares")
    st.markdown("""
    | Algorithm         | Handles Negative Weights | Time Complexity  | Use Case                       |
    |-------------------|---------------------------|------------------|--------------------------------|
    | **Dijkstra**      | ❌ No                     | O((V + E) log V) | Fast, accurate for real maps  |
    | **Bellman-Ford**  | ✅ Yes                    | O(V × E)         | Works with debt/credit graphs |
    | **Floyd-Warshall**| ✅ Yes                    | O(V³)            | All-pairs path problems        |

    In KL route planning, **Dijkstra is ideal** because:
    - All routes have **positive weights**
    - We only need **source-to-target** computation
    - It’s the **most efficient option**
    """)

    st.success("That's why Dijkstra is our choice for KL Route Optimization! 🧠")

# ---------------------------- COMPARISON TAB ---------------------------- #
with tabs[3]:
    st.header("📊 Algorithm Comparison")
    st.markdown("Here's how Dijkstra compares to Bellman-Ford and Floyd-Warshall:")

    st.table({
        "Algorithm": ["Dijkstra", "Bellman-Ford", "Floyd-Warshall"],
        "Handles Negative Weights": ["❌", "✅", "✅"],
        "Time Complexity": ["O((V + E) log V)", "O(V × E)", "O(V³)"],
        "Best For": ["Sparse graphs, real-time routing", "Graphs with negative weights", "All-pairs shortest paths"]
    })
