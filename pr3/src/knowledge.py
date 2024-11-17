from utils import readFile
import re


class Knowledge:
    """
    Clase encargada de almacenar y gestionar
    la base de conocimiento y las equivalencias
    La estructura es asi: {<relacion> : { <sujeto> : set(<objeto>) }}
    """

    def __init__(self):
        self.base = dict()
        self.equivalencias = dict()

    def findBy(self, subj, pred, obj):
        """
        Devuelve una lista de parejas [subj, obj] dada una de las clausulas del where (Si es None, se trata de un alias)
        """
        if pred not in self.base and pred not in self.equivalencias:
            raise KeyError(
                f"[WARNING]: El predicado {pred} no existe en la base de conocimiento. Se omite"
            )

        if pred in self.equivalencias:
            # escogemos predicados que tienen alguna afirmacion
            pred = [p for p in self.equivalencias[pred] if p in self.base]
        else:
            pred = [pred]
        result = []
        if subj is None and obj is None:
            # subj y obj son aliases
            for p in pred:
                result.extend([[s, o] for s in self.base[p] for o in self.base[p][s]])
        elif subj is None:
            # subj es alias
            for p in pred:
                result.extend(
                    [[s, o] for s in self.base[p] for o in self.base[p][s] if o in obj]
                )
        elif obj is None:
            # obj es alias
            for p in pred:
                result.extend([[s, o] for s in subj for o in self.base[p][s]])
        else:
            # filtramos filas
            for p in pred:
                result.extend(
                    [[s, o] for s in subj for o in self.base[p][s] if o in obj]
                )

        return result

    def load(self, filename):
        """
        Carga la base de conocimiento
        """
        lines = readFile(filename)
        try:
            self.importFromRaw("".join(lines))
        except Exception as e:
            raise Exception(
                "[ERROR]: Base de conocimiento mal configurada. Cargue otra"
            )

    def añadirInfo(self, subject, predicado, object):
        """
        Añade la tripleta sujeto, predicado, objeto a la base de conocimiento
        """
        if predicado not in self.base.keys():
            self.base[predicado] = dict()

        if subject not in self.base[predicado]:
            # crea el conjunto que guardara los objetos
            self.base[predicado][subject] = set()

        self.base[predicado][subject].add(object)

    def añadirEquivalencia(self, t1, t2):
        """
        Para un predicado @t1 añade su equivalente @t2
        """
        if t1 not in self.equivalencias.keys():
            self.equivalencias[t1] = set([t1])
        if t2 not in self.equivalencias.keys():
            self.equivalencias[t2] = set([t2])

        self.equivalencias[t1].add(t2)
        self.equivalencias[t2].add(t1)

    def importFromRaw(self, joinedLines):
        """
        Separa las afirmaciones por ".", extrae tripletas y las añade a la base de conocimiento
        """
        subjectDescription = joinedLines.split(" .")[:-1]
        for s in subjectDescription:
            s = s.strip()
            subject = None
            for afirmacion in s.split(" ;"):
                # Añadimos a la base de conocimiento cada afirmacion del sujeto
                equivalencia = re.search(
                    r"^((wd)?t\d+:\w+) (wd)?t:P1628 ((wd)?t\d+:\w+)$", afirmacion
                )
                if equivalencia:
                    eq = equivalencia.groups()
                    t1 = eq[0]
                    t2 = eq[3]
                    self.añadirEquivalencia(t1, t2)
                else:
                    subject, predicado, object = self.processRelation(
                        afirmacion, subject
                    )
                    self.añadirInfo(subject, predicado, object)

    def processRelation(self, relation, subject):
        """
        Procesa la afirmacion del sujeto y devuelve la tripleta RDF subject, predicado, object
        """
        if '"' in relation:
            # literales
            if subject is None:
                relation = re.search(
                    r'^(wd:Q\d+|q\d+:\w+) (wdt:P\d+|t\d+:\w+) (".+")', relation
                )
                subject, predicado, object = relation.groups()
            else:
                relation = re.search(r'(wdt:P\d+|t\d+:\w+) (".+")', relation)
                predicado, object = relation.groups()
        else:
            # sin literales
            if subject is None:
                relation = re.search(
                    r"^(wd:Q\d+|q\d+:\w+) (wdt:P\d+|t\d+:\w+) (wd:Q\d+|q\d+:\w+)",
                    relation,
                )
                subject, predicado, object = relation.groups()

            else:
                relation = re.search(
                    r"(wdt:P\d+|t\d+:\w+) (wd:Q\d+|q\d+:\w+)", relation
                )
                predicado, object = relation.groups()

        return subject, predicado, object

    def save(self, base_nueva):
        """
        Guarda la base de conocimiento vigente en un archivo sin sobreescribir
        """
        try:
            f = open(
                f"{base_nueva}", "x"
            )  # Evita sobreescribir una base de conocimiento que ya existe
            for pred in self.base:
                for subj in self.base[pred]:
                    for obj in self.base[pred][subj]:
                        f.write(f"{subj} {pred} {obj} .\n")

            # Guardamos las equivalencias también
            f.write(f"\n# EQUIVALENCIAS\n")

            equivalencias1v1 = []
            for clave, equivalentes in self.equivalencias.items():
                for eq in equivalentes:
                    if clave < eq:
                        equivalencias1v1.append([clave, eq])

            for eq1, eq2 in equivalencias1v1:
                f.write(f"{eq1} wdt:P1628 {eq2} .\n")
            f.close()
        except FileExistsError as e:
            raise FileExistsError(
                f"[ERROR]: La base de conocimiento {base_nueva} ya existe"
            )
