import pandas as pd
from knowledge import Knowledge
import re
from excepciones import QueryException, CustomException, ErrorLiteralQueryException



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

        whereClauses = [l.strip() for l in grWhe[0].split(" .")]
        if whereClauses[-1] == "":
            whereClauses = whereClauses[:-1]
        else:
            raise QueryException("[ERROR] Falta el punto al final del where.")

        return selectColumns, whereClauses

    def query(self, queryStr, knowledge: Knowledge):
        """
        Realiza la consulta a la base de conocimiento
        Distinguir tres tipos (depende de que variable existia antes de la clausula)
        1. ?var1 predicado ?var2
        2. ?var predicado obj
        3. subj predicado ?var
        """

        selectColumns, whereClauses = self.preprocess(queryStr)
        dfResponse = pd.DataFrame()
        for clause in whereClauses:
            try:
                if '"' in clause:
                    obj = self.extractLiteral(clause)
                    subj, pred = clause.split(" ")[:2]

                else:
                    subj, pred, obj = clause.split(" ")

                # dependiendo de la clausula, operamos o bien directamente con la entidad o con un conjunto de ellas
                processedSubj, processedPred, processedObj = [subj], pred, [obj]
                if subj.startswith("?"):
                    # casos 1 y 2
                    processedSubj = (
                        dfResponse[subj].unique() if subj in dfResponse.columns else None
                    )
                    if obj.startswith("?"):
                        # caso 1
                        processedObj = (
                            dfResponse[obj].unique() if obj in dfResponse.columns else None
                        )
                elif obj.startswith("?"):
                    # caso 3
                    processedObj = (
                        dfResponse[obj].unique() if obj in dfResponse.columns else None
                    )
                # try:
                dfKnowledge = pd.DataFrame(
                    knowledge.findBy(processedSubj, processedPred, processedObj),
                    columns=[subj, obj],
                )
                # except Exception as e:
                #    print(e)
                #    continue

                if dfResponse.shape[0] == 0:
                    dfResponse = dfKnowledge
                else:
                    how = "right"  # para filtrar
                    if processedSubj is None or processedObj is None:
                        how = "outer"  # sobre todo para añadir nuevas columnas
                    dfResponse = dfResponse.merge(dfKnowledge, how=how)

                return dfResponse[selectColumns]
            except CustomException as e:
                print(f" {e}. No se tendrá en cuenta la clausula {clause}")
    
    def extractLiteral(self, whereClause):
        """
        Extrae el objeto literal en el where de la query
        """
        principio_cadena = whereClause.find('"') + 1
        final_cadena = whereClause.find('"', principio_cadena)
        
        if principio_cadena != -1 and final_cadena != -1:
            return whereClause[principio_cadena:final_cadena].strip()
        else:
            raise ErrorLiteralQueryException() 

