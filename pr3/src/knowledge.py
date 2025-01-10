from utils import readFile
import re
from excepciones import FileAlreadyExistsException, SPARQLFormatException


class Knowledge:
    """
    Clase encargada de almacenar y gestionar
    la base de conocimiento y las equivalencias
    La estructura es asi: {<relacion> : { <sujeto> : set(<objeto>) }}
    """

    def __init__(self, knowledge_path):
        self.base = dict()
        self.equivalencias = dict()
        self.load(knowledge_path)

    def findBy(self, subj, pred, obj):
        """
        Devuelve una lista de parejas [subj, obj] dada una de las clausulas del where (Si es None, se trata de un alias)
        """
        if pred not in self.base and pred not in self.equivalencias:
            return []

        if pred in self.equivalencias:
            # escogemos predicados que tienen alguna afirmacion
            pred = [p for p in self.equivalencias.get(pred, []) if p in self.base]
        else:
            pred = [pred]
        result = []
        if subj is None and obj is None:
            # subj y obj son aliases
            for p in pred:
                result.extend(
                    [
                        [s, o]
                        for s in self.base.get(p, [])
                        for o in self.base[p].get(s, [])
                    ]
                )
        elif subj is None:
            # subj es alias
            for p in pred:
                result.extend(
                    [
                        [s, o]
                        for s in self.base.get(p, [])
                        for o in self.base[p].get(s, [])
                        if o in obj
                    ]
                )
        elif obj is None:
            # obj es alias
            for p in pred:
                result.extend([[s, o] for s in subj for o in self.base[p].get(s, [])])
        else:
            # filtramos filas
            for p in pred:
                result.extend(
                    [[s, o] for s in subj for o in self.base[p].get(s, []) if o in obj]
                )

        return result

    def load(self, filename):
        """
        Carga la base de conocimiento
        """
        print(f'[INFO] Cargando "{filename}".')
        lines = readFile(filename)
        OK = self.importFromRaw(" ".join(lines))
        error_msg = ""
        if not OK:
            error_msg = f" excluyendo los errores"
        print(f"[INFO] Base de conocimiento cargada{error_msg}.")

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
        Devuelve true si no han habido errores
        """
        hasErrors = False
        subjectDescription = joinedLines.split(" .")[:-1]
        for s in subjectDescription:
            try:
                s = s.strip()
                if "wdt:p1628" in s.lower():
                    # Es una equivalencia, vemos si está correctamente formulada
                    correct = False
                    if len(s.split(" ")) == 3:
                        t1, eq, t2 = s.split(" ")
                        if eq.lower() == "wdt:p1628":
                            correct = True
                            self.añadirEquivalencia(t1, t2)
                    if not correct:
                        raise SPARQLFormatException(
                            f"[ERROR]: SPARQL incorrecto, la equivalencia '{s} .' debe ser: <predicado1> wdt:p1628 <predicado2> ."
                        )

                else:
                    subject = None
                    for afirmacion in s.split(" ;"):
                        # Añadimos a la base de conocimiento cada afirmacion del sujeto
                        subject, predicado, object = self.processRelation(
                            afirmacion, subject
                        )
                        self.añadirInfo(subject, predicado, object)

            except SPARQLFormatException as e:
                hasErrors = True
                print(e)

        last = joinedLines.split(" .")[-1]
        if last != "":
            # Fallo si no se añade el último punto
            print(
                f"[ERROR]: SPARQL incorrecto, falta el punto de finalizacion al final de '{last}'."
            )
            hasErrors = True

        return not hasErrors

    def processRelation(self, relation, subject):
        """
        Procesa la afirmacion del sujeto y devuelve la tripleta RDF subject, predicado, object
        """
        relation = relation.strip()
        if '"' in relation:
            # hay literales
            if subject is None:
                parts = re.search(r'^(\S+) (\S+) ("[^"]+")$', relation)
                if parts:
                    subject, predicado, object = parts.groups()
                else:
                    raise SPARQLFormatException(
                        f"[ERROR]: SPARQL incorrecto, secuencia '{relation}' debe ser: <sujeto> <predicado> \"<objeto literal>\""
                    )
            else:
                parts = re.search(r'^(\S+) ("[^"]+")$', relation)
                if parts:
                    predicado, object = parts.groups()
                else:
                    raise SPARQLFormatException(
                        f"[ERROR]: SPARQL incorrecto, secuencia '{relation}' debe ser: <predicado> \"<objeto literal>\""
                    )

        else:
            # no hay literales
            parts = relation.split(" ")  # separamos por espacios
            if subject is None:
                if len(parts) == 3:
                    subject, predicado, object = parts
                else:
                    raise SPARQLFormatException(
                        f"[ERROR]: SPARQL incorrecto, secuencia '{relation}' debe ser: <sujeto> <predicado> <objeto>"
                    )
            else:
                if len(parts) == 2:
                    predicado, object = parts
                else:
                    raise SPARQLFormatException(
                        f"[ERROR]: SPARQL incorrecto, secuencia '{relation}' debe ser: <predicado> <objeto>"
                    )

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
                f.write(f"{eq1} wdt:p1628 {eq2} .\n")
            f.close()
        except FileExistsError as e:
            raise FileAlreadyExistsException(
                f"[ERROR]: La base de conocimiento {base_nueva} ya existe."
            )
