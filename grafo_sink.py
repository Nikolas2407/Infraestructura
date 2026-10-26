import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("Grafo de red y Sink Tree hacia B")

# Red no dirigida: los enlaces funcionan en ambos sentidos.
enlaces = [
    ("H", "D"), ("D", "A"), ("A", "B"),
    ("H", "E"), ("E", "J"), ("J", "C"), ("C", "B"),
    ("H", "O"), ("O", "N"), ("N", "J"),
]

G = nx.Graph()
G.add_edges_from(enlaces)

# Posiciones compartidas para facilitar la comparación.
pos = {
    "B": (2, 4),
    "A": (0, 3),
    "C": (4, 3),
    "D": (0, 2),
    "J": (4, 2),
    "E": (2, 1.5),
    "N": (4, 1),
    "H": (0, 0),
    "O": (4, 0),
}

# BFS parte del destino.
# El padre de cada router será su siguiente salto hacia B.
siguiente_salto = dict(nx.bfs_predecessors(G, source="B"))

T = nx.DiGraph()
T.add_nodes_from(G.nodes)

for router, siguiente in siguiente_salto.items():
    T.add_edge(router, siguiente)

def dibujar(red, titulo, dirigido=False):
    fig, ax = plt.subplots(figsize=(7, 5))

    colores = [
        "#F5B041" if nodo == "B" else "#85C1E9"
        for nodo in red.nodes
    ]

    nx.draw_networkx(
        red,
        pos=pos,
        ax=ax,
        node_color=colores,
        node_size=1100,
        font_size=12,
        font_weight="bold",
        edge_color="#566573",
        arrows=dirigido,
        arrowsize=24,
    )

    ax.set_title(titulo)
    ax.axis("off")
    fig.tight_layout()
    return fig

col1, col2 = st.columns(2)

with col1:
    fig = dibujar(G, "Grafo completo")
    st.pyplot(fig)
    plt.close(fig)

with col2:
    fig = dibujar(T, "Sink Tree hacia B", dirigido=True)
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Tabla de siguientes saltos")

st.dataframe(
    [
        {
            "Router": router,
            "Siguiente salto": siguiente_salto[router],
            "Saltos hasta B": nx.shortest_path_length(
                G, router, "B"
            ),
        }
        for router in sorted(siguiente_salto)
    ],
    hide_index=True,
)

ruta = nx.shortest_path(G, source="H", target="B")
st.write("Ruta óptima desde H:", " → ".join(ruta))