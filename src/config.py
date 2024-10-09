import toml

class Config:
    """
    Clase encargada de trabajar con la confuguración adicional en el archivo config.toml
    """

    def __init__(self):
        self.load()

    def load(self):
        """
        Carga el archivo config.toml
        """

        try:
            with open("config.toml", "r") as f:
                self.config = toml.load(f)
        except Exception:
            self.config = []
            print(
                "Archivo config.toml no se puedo cargar. Usando configuración predeterminada."
            )

    def getConfigOrDefault(self, configPath, default):
        """
        Devuelve la entrada del archivo toml
        - configPath -> lista de keys para acceder al valor
        - default -> valor por defecto (se usa si no se encontró el valor)

        Ej.
        getConfigOrDefault(["settings", "user"], "test")
        
        Accede a self.config["settings"]["user"]
        Devuelve "test" si es vacío
        """
        result = self.config
        for level in configPath:
            if level in result:
                result = result[level]
            else:
                return default
        
        return result