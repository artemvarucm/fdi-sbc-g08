import matplotlib.pyplot as plt
import networkx as nx
from excepciones import invalidFileExtensionException, noDataException

class GraphDrawer:
    """
    Clase encargada de pintar los grafos
    """

    def draw(self, resultDf, filename):
        """
        Dibuja el grafo del dataframe @resultDf (resultado de una consulta) y guarda la imagen en @filename

        Genera un nodo, si no existe para cada columna de cada fila y
        une con aristas los nodos de las columnas de una fila
        """
        if resultDf is None or resultDf.empty:
            raise noDataException("[ERROR]: No hay datos para dibujar el grafo")
        if len(filename) < 4 or filename[-4:] != ".png":
            raise invalidFileExtensionException("[ERROR]: El archivo debe tener extension PNG")

        G = nx.Graph()
        nRows, nCols = resultDf.shape
        if nCols == 1:
            # si hay una columna, no hay aristas, solo nodos
            G.add_nodes_from(resultDf.iloc[:, 0])
        else:
            for i in range(nRows):
                # unimos todas las columnas con aristas
                for col1 in range(nCols):
                    for col2 in range(nCols):
                        if col1 != col2:
                            # no añadimos autoflechas
                            G.add_edge(resultDf.iloc[i, col1], resultDf.iloc[i, col2])

        pos = nx.spring_layout(G)
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
        plt.show()
