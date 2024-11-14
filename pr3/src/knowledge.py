from utils import readFile
import re


class Knowledge:
    """
    Clase encargada de almacenar y gestionar
    la base de conocimiento y las equivalencias
    como diccionario que tiene como clave <relacion> y como valor otro diccionario {<sujeto>:<objeto>}
    """

    def __init__(self):
        self.base = dict()
        self.equivalencias = dict()

    def findBy(self, subj, pred, obj):
        """
        Devuelve una lista de parejas [subj, obj]
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
        if subj is None:
            for p in pred:
                result.extend([[k, v] for k, v in self.base[p].items() if v in obj])
        elif obj is None:
            for p in pred:
                result.extend([[s, self.base[[p]][s]] for s in subj])

        return result

    def load(self, filename):
        """
        Carga la base de conocimiento
        """
        lines = readFile(filename)
        self.processSubjects("".join(lines))

    def añadirInfo(self, subject, predicado, object):
        """
        Añade la tripleta sujeto, predicado, objeto a la base de conocimiento
        """
        if predicado not in self.base.keys():
            self.base[predicado] = dict()
        elif subject not in self.base[predicado]:
            self.base[subject] = dict()

        self.base[predicado][subject] = object

    def añadirEquivalencia(self, t1, t2):
        """Para un predicado añade su equivalente"""
        if t1 not in self.equivalencias.keys():
            self.equivalencias[t1] = set([t1])
        if t2 not in self.equivalencias.keys():
            self.equivalencias[t2] = set([t2])

        self.equivalencias[t1].add(t2)
        self.equivalencias[t2].add(t1)

    def processSubjects(self, joinedLines):
        """
        Separa los sujetos y los va añadiendo a la base de conocimiento
        """
        subjectDescription = joinedLines.split(" .")[:-1]
        for s in subjectDescription:
            s = s.strip()  # FIXME - control de errores
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
        Procesa la afirmacion del sujeto
        """
        if '"' in relation:
            # literales
            if subject is None:
                relation = re.search(r'^(q\d+:\w+) ((wd)?t\w*:\w+) (".+")', relation)
                gr = relation.groups()
                subject = gr[0]
                predicado = gr[1]
                object = gr[3]
            else:
                relation = re.search(r'((wd)?t\w*:\w+) (".+")', relation)
                gr = relation.groups()
                predicado = gr[0]
                object = gr[2]
        else:
            # sin literales
            if subject is None:
                # FIXME, matchea predicados incorrectos, ej tenis2:P31, solo deberia de hacerlo para t\d o wdt
                relation = re.search(
                    r"^(q\d+:\w+) ((wd)?t\w*:\w+) (q\d+:\w+)", relation
                )
                gr = relation.groups()
                subject = gr[0]
                predicado = gr[1]
                object = gr[3]
            else:
                relation = re.search(r"((wd)?t\w*:\w+) (q\d+:\w+)", relation)
                gr = relation.groups()
                predicado = gr[0]
                object = gr[2]
        return subject, predicado, object

    def save(self, base_nueva):
        """
        Guarda la base de conocimiento vigente en un archivo .ttl
        """
        try:
            f = open(
                f"{base_nueva}", "x"
            )  # Evita sobreescribir una base de conocimiento que ya existe
            for pred in self.base:
                for subj in self.base[pred]:
                    f.write(f"{subj} {pred} {self.base[pred][subj]} .\n")

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
