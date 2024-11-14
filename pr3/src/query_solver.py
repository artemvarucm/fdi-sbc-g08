import pandas as pd
from knowledge import Knowledge
import re


class QuerySolver:
    """
    Clase encargada de realizar las consultas a la base de conocimiento
    """

    def preprocess(self, queryStr):
        """
        Separa las clausulas select y where para utilizarlas posteriormente en nuestro motor
        """
        selectRegex = re.search(r"(?s)select(.*)where", queryStr)
        grSel = selectRegex.groups()
        selectColumns = re.sub(r"[\s\n]", "", grSel[0]).split(",")

        whereRegex = re.search(r"(?s){(.*)}", queryStr)
        grWhe = whereRegex.groups()

        whereClauses = [l.strip() for l in grWhe[0].split(" .")][:-1]

        return selectColumns, whereClauses

    def query(self, queryStr, knowledge: Knowledge):
        """
        Distinguir tres tipos (depende de que variable existia antes de la clausula)
        1. ?var1 predicado ?var2
        2. ?var predicado obj
        3. subj predicado ?var
        """

        selectColumns, whereClauses = self.preprocess(queryStr)
        dfResponse = pd.DataFrame()
        for clause in whereClauses:
            subj, pred, obj = clause.split(" ")

            # dependiendo de la clausula, operamos o bien directamente con la entidad o con un conjunto de ellas
            processedSubj, processedPred, processedObj = [subj], pred, [obj]
            if subj.startswith("?"):
                processedSubj = dfResponse[subj] if subj in dfResponse.columns else None
                if obj.startswith("?"):
                    # caso 1
                    processedObj = (
                        dfResponse[obj] if obj in dfResponse.columns else None
                    )
            elif obj.startswith("?"):
                # caso 3
                processedObj = dfResponse[obj] if obj in dfResponse.columns else None
            try:
                dfKnowledge = pd.DataFrame(
                    knowledge.findBy(processedSubj, processedPred, processedObj),
                    columns=[subj, obj],
                )
            except Exception as e:
                print(e)
                continue

            if dfResponse.shape[0] == 0:
                dfResponse = dfKnowledge
            else:
                dfResponse = dfResponse.merge(dfKnowledge, how="outer")

        return dfResponse[selectColumns]
