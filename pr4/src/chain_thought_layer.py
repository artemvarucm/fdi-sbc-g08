class ChainThoughtLayer:
    """Chain of Thoughts, capa que permite explicar mejor la respuesta"""

    def chat(self, ollama, messagesHistory, query):
        # prompt con instrucciones para el chain of thoughts
        messagesHistory.append(
            {
                "role": "system",
                "content": f"""
                Keep in mind your previous response 
                (in which you used the information we provided you to answer the query "{query}")
                and remember that the user wants to know why you gave that answer.
                
                To explain your reasoning step by step, follow this structure.

                1. Identify the problem the user has.
                2. Break it into subproblems.
                3. Analyze each subproblem in detail.
                4. Solve each subproblem and remember why you took each decision.Your solving process should feel like unpolished notes—messy, exploratory, and authentic. Remember your full thought process, including missteps, dead ends, and course corrections
                5. Combine and connect the results of all subproblems to create a final conclusion. Seek deep patterns: "I’m seeing a connection -", "This ties back to -". Link broader implications: "This means -", "If this holds, then -

                Always show your full reasoning process, even for simple problems. If the solution requires assumptions, make them explicit.

                Use linkers to make your response more natural, and not explicitly showing the steps you follow.

                """,
            }
        )

        response = ollama.chat(messagesHistory)

        messagesHistory.append(response["message"])
        # prompt para quedarnos con lo mejor de la versión sin chain of thoughts y la versión con chain of thoughts
        messagesHistory.append(
            {
                "role": "system",
                "content": """
                  Analyze previous the conclusion you reached before. If there is any contradiction try to solve it: "before I thought - now I think -".
                  If you cannot solve it, just admit it "I hadn't thought about it, maybe I should give it another turn"
                  Tell the user, with clear explanations, how you reached the previous conclusion.
                  Avoid unnecessary information so the user has a better experience.

            """,
            }
        )

        response = ollama.chat(messagesHistory)

        messagesHistory.append(response["message"])
