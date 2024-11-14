import matplotlib.pyplot as plt
import networkx as nx


class GraphDrawer:
    def draw(self, resultDf, filename):
        """
        Dibuja el grafo del dataframe y guarda la imagen
        """
        if resultDf is None or resultDf.empty:
            raise Exception("[ERROR]: No hay datos para dibujar el grafo")
        if len(filename) < 4 or filename[-4:] != ".png":
            raise Exception("[ERROR]: El archivo debe tener extension PNG")

        G = nx.Graph()
        nRows, nCols = resultDf.shape
        if nCols == 1:
            # no hay aristas, solo nodos
            G.add_nodes_from(resultDf.iloc[:, 0])
        else:
            for i in range(nRows):
                for col in range(nCols - 1):
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
