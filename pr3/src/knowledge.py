from utils import readFile
import re

class Knowledge:
    """
    Guardamos como diccionario de lista de diccionarios relacion:{a:b}
    """
    def __init__(self, filename):
        self.base = dict()
        self.load(filename)

    def load(self, filename):
        self.processSubjects(readFile(filename))
    
    def añadirInfo(self, subject, predicado, object):
        if predicado not in self.base.keys() or not self.base[predicado]:
            self.base[predicado] = dict()

        self.base[predicado][subject] = object
    
    def processSubjects(self, lines):
        subjectDescription = "".join(lines).split(" .")[:-1]
        for s in subjectDescription:
            subject = None
            for relation in s.split(" ;"):
                subject, predicado, object = self.processRelation(relation, subject)
                self.añadirInfo(subject, predicado, object)
            
    def processRelation(self, relation, subject):
        # FIXME, matchear los literales con comillas
        if subject is None:
            # FIXME, matchea predicados incorrectos, ej tenis2:P31, solo deberia de hacerlo para t\d o wdt
            relation = re.search(r"^(q\d+:\w+) ((wd)?t\w*:\w+) (q\d+:\w+)", relation)
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