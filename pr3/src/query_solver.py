import pandas as pd
from knowledge import Knowledge

class QuerySolver:
    """
    Distinguir tres tipos (depende de que variable existia antes de la clausula)
    1. ?var1 predicado ?var2
    2. ?var predicado obj
    3. subj predicado ?var
    """
    def query(self, queryStr, knowledge: Knowledge):
        selectColumns = ["?pers", "?relig"]
        # se puede hacer un set para evitar aplicar 2 reglas repetidas
        whereClauses = ["?pers wdt:P31 q8:persona", "?pers t8:religion ?relig"]
        
        
        dfResponse = pd.DataFrame()
        for clause in whereClauses:
            subj, pred, obj = clause.split(' ')
            
            # dependiendo de la clausula, operamos o bien directamente con la entidad o con un conjunto de ellas
            processedSubj, processedPred, processedObj = [subj], pred, [obj]
            if subj.startswith('?'):
                processedSubj = dfResponse[subj] if subj in dfResponse.columns else None
                if obj.startswith('?'):
                    # caso 1
                    processedObj = dfResponse[obj] if obj in dfResponse.columns else None
            elif obj.startswith('?'):
                # caso 3
                processedObj = dfResponse[obj] if obj in dfResponse.columns else None
            
            dfKnowledge = pd.DataFrame(knowledge.findBy(processedSubj, processedPred, processedObj), columns=[subj, obj])
            #print(dfKnowledge.head()) 

            if dfResponse.shape[0] == 0:
                dfResponse = dfKnowledge
            else:
                dfResponse = dfResponse.merge(dfKnowledge, how='outer') # FIXME pensar si es left, right o outer...

            #print(dfResponse.head()) 

        return dfResponse[selectColumns]