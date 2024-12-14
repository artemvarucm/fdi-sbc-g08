from utils import readFile
from ollama_controller import OllamaController
import os
from pathlib import Path


class RAG:
    """
    Clase encargada de hacer el prompt engineering con ollama (intermediario)
    """

    def __init__(self, bases_conocimiento, model, chain_of_thought):
        self.knowledge = self.loadKnowledge(bases_conocimiento)
        self.messagesHistory = self.getPrompts(chain_of_thought)
        self.ollama = OllamaController(model)

    def loadKnowledge(self, bases_conocimiento):
        return {
            # Historia de las marcas


            # Pilotos Formula 1


            # Modelos de coches de las marcas
            "ferrari": Path(bases_conocimiento, "ferrari.txt"),

        }

    def processKnowledge(self, query):
        contextLines = []
        for k in self.knowledge.keys():
            if k in query.lower():
                contextLines.extend(readFile(self.knowledge[k]))

        print(" ".join(contextLines))
        return " ".join(contextLines)

    def chat(self, query):
        processed = self.processKnowledge(query)
        self.messagesHistory.extend(
            [
                {
                    "role": "system",
                    "content": (
                        f"For the next user query use the following context {processed}."
                        if processed
                        else "Try to find information from your own knowledge."
                    ),
                },
                {
                    "role": "user",
                    "content": query,
                },
            ]
        )
        response = self.ollama.chat(self.messagesHistory)

        # Añadimos la respuesta de ollama al historial
        self.messagesHistory.append(response["message"])

        return response["message"]["content"]

    def switchModel(self, model):
        return self.ollama.setModel(model)

    def getPrompts(self, chain_of_thought):
        prompts = [
            {
                "role": "system",
                "content": """
                You are a salesman that helps people to find out which car is available and
                why is it better from the knowledge base we will provide you. 
                You must be efficient, using only the right information to answer the response from the user.
            """,
            },
            {
                "role": "system",
                "content": """
                 If you do not find the information in the knowledge we provide you, 
                 answer whatever you consider relevant. 
            """,
            },
        ]

        if chain_of_thought:
            prompts.append(
                {
                    "role": "system",
                    "content": """
                    Write in a raw, real-time stream-of-consciousness style, as if actively solving a problem. Your response should feel like unpolished notes—messy, exploratory, and authentic. Show your full thought process, including missteps, dead ends, and course corrections. Use markers to signal mental states: Insights: "Wait -", "Hold on -", "Oh -", "Suddenly seeing -", "This connects to -". Testing: "Testing with -", "Breaking this down -", "Running an example -", "Checking if -". Problems: "Stuck on -", "This doesn’t work because -", "Need to figure out -", "Not quite adding up -". Progress: "Making headway -", "Starting to see the pattern -", "Explains why -", "Now it makes sense -". Process: "Tracing the logic -", "Following this thread -", "Unpacking this idea -", "Exploring implications -". Uncertainty: "Maybe -", "Could be -", "Not sure yet -", "Might explain -". Transitions: "This leads to -", "Which means -", "Building on that -", "Connecting back to -".

                    Lean into real-time realizations: "Wait, that won't work because…" or "Ah, I missed this…" Show evolving understanding through short paragraphs, with natural pauses where ideas shift. Structure your thought evolution as follows: Begin with an initial take: "This might work because…" or "At first glance…" Identify problems or angles: "Actually, this doesn’t hold up because…" Test examples or counterexamples: "Let me try -", "What happens if -". Seek deeper patterns: "I’m seeing a connection -", "This ties back to -". Link broader implications: "This means -", "If this holds, then -".

                    Admit confusion openly: "I don’t get this yet", "Something’s missing here". Reveal partial understanding: "I see why X, but not Y". Show failures and iterations: "Still not right - trying another approach". Embrace a debugging mindset, treating ideas like code—break them into steps, test logic, reveal failure modes, and iterate. Skip introductions and conclusions. Stop when you solve the problem or find clear next steps. Use short, direct sentences to mimic real-time thinking. The goal is to capture the messy, evolving nature of problem-solving and thought refinement.
                """,
                }
            )

        return prompts
