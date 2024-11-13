from utils import readFile
import re


class Knowledge:
    """
    Guardamos como diccionario de lista de diccionarios relacion:{a:b}
    """

    def __init__(self):
        self.base = dict()

    def findBy(self, subj, pred, obj):
        if subj is None:
            return [[k, v] for k, v in self.base[pred].items() if v in obj]
        elif obj is None:
            return [[s, self.base[pred][s]] for s in subj]

    def load(self, filename):
        lines = readFile(filename)
        self.processSubjects("".join(lines))
        # print(self.base)

    def añadirInfo(self, subject, predicado, object):
        if predicado not in self.base.keys():
            self.base[predicado] = dict()
        elif subject not in self.base[predicado]:
            self.base[subject] = dict()

        self.base[predicado][subject] = object

    def processSubjects(self, joinedLines):
        subjectDescription = joinedLines.split(" .")[:-1]
        for s in subjectDescription:
            s = s.strip()  # FIXME - control de errores
            subject = None
            for relation in s.split(" ;"):
                subject, predicado, object = self.processRelation(relation, subject)
                self.añadirInfo(subject, predicado, object)
        # print(self.base)

    def processRelation(self, relation, subject):
        if '"' in relation:
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
        f = f = open(
            f"{base_nueva}", "x"
        )  # Evita sobreescribir una base de conocimiento que ya existe
        for pred in self.base:
            for subj in self.base[pred]:
                f.write(f"{subj} {pred} {self.base[pred][subj]} .\n")
        f.close()
