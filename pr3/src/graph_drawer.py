import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer:
    def draw(self, resultDf, filename):
        G = nx.Graph()
        for i in range(len(resultDf)):
            for col in range(len(resultDf.columns) - 1):
                G.add_edge(resultDf.iloc[i, col], resultDf.iloc[i, col + 1])

        # Dibujar el grafo
        pos = nx.spring_layout(G)  # Disposición de los nodos
        plt.figure(figsize=(8, 6))

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_size=2000,
            node_color="lightblue",
            font_size=10,
            font_weight="bold",
        )

        plt.savefig(filename, format="PNG")

        # plt.title("Grafo")
        plt.show()
