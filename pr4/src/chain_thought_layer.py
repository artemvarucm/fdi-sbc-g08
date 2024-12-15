class ChainThoughtLayer:
    """Chain of Thoughts, capa que permite explicar mejor la respuesta"""

    def chat(self, ollama, messagesHistory, query):
        # prompt con instrucciones para el chain of thoughts
        messagesHistory.append(
            {
                "role": "system",
                "content": """
                Rewrite your previous response,
                in which you used the context provided to give another answer to the query "{query}"

                You are a logical assistant who always explains your reasoning step by step before arriving at an answer.

                1. Identify the problem or goal.
                2. Break it into smaller steps or subproblems.
                3. Analyze each step in detail.
                4. Solve each step with clear explanations.
                5. Combine the results to form a final answer or conclusion.

                Always show your full reasoning process, even for simple problems. If the solution requires assumptions, make them explicit.
                If there's ambiguity, outline multiple possible paths and explain which is most likely.

                Use linkers to make your response more natural, and not explicitly showing the steps you follow.
                Do not write setntences like "Step 1: identify the problem"
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
                Summarize the information from the previous response,
                removing unnecessary information,
                but keeping the natural styles and explanations
            """,
            }
        )

        response = ollama.chat(messagesHistory)

        messagesHistory.append(response["message"])
