import streamlit as st
import networkx as nx
import folium
from streamlit_folium import st_folium
from dijkstra_module import build_graph, dijkstra_with_priority_queue, build_path

# Coordinates for each node (KL locations)
COORDINATES = {
    'KLIA': (2.7456, 101.7090),
    'Putrajaya': (2.9264, 101.6964),
    'Merdeka 118': (3.1385, 101.6982),
    'Berjaya Times Square': (3.1420, 101.7104),
    'Bukit Bintang': (3.1466, 101.7072),
    'Exchange 106 @ TRX': (3.1390, 101.7225),
    'Petronas Twin Towers': (3.1579, 101.7123),
    'Merdeka Square': (3.1478, 101.6946),
    'KL Tower': (3.1528, 101.7039),
    'Tabung Haji Tower': (3.1569, 101.7060)
}

# Page configuration
st.set_page_config(page_title="KL City Route Optimizer", page_icon="🗺️", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# App header
st.title("🧭 KL City Route Optimizer")
st.markdown("Find the fastest route across key KL landmarks using Dijkstra's Algorithm. Now with interactive map! 🚗")
st.markdown("---")

# Load graph and nodes
G = build_graph()
nodes = list(G.nodes())

col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("📍 Starting Point", nodes)
with col2:
    target = st.selectbox("🏁 Destination Point", nodes)

# Run algorithm on button click
if st.button("🔍 Compute Route"):
    if source == target:
        st.warning("Source and destination must be different.")
    else:
        distance_map, previous_map = dijkstra_with_priority_queue(G, source)
        path = build_path(previous_map, target)

        if not path:
            st.error("❌ No path found between selected locations.")
        else:
            st.success(f"✅ Path found from **{source}** to **{target}**!")
            st.markdown(f"**🛣️ Route:** {' → '.join(path)}")
            st.info(f"📏 Total Distance: **{distance_map[target]} units**")

            # Map visualization
            midpoint = COORDINATES[path[len(path)//2]]
            route_map = folium.Map(location=midpoint, zoom_start=13)

            # Add markers and lines
            for i, loc in enumerate(path):
                lat, lon = COORDINATES[loc]
                popup = f"{i+1}. {loc}"
                icon_color = 'green' if i == 0 else 'red' if i == len(path)-1 else 'blue'
                folium.Marker(location=(lat, lon), popup=popup, icon=folium.Icon(color=icon_color)).add_to(route_map)

            # Draw path
            route_coords = [COORDINATES[loc] for loc in path]
            folium.PolyLine(locations=route_coords, color='crimson', weight=5).add_to(route_map)

            st_folium(route_map, width=1000, height=550)
else:
    st.info("👆 Select two different points and click 'Compute Route' to begin.")
