class ChainThoughtLayer:
    def chat(self, ollama, messagesHistory, query):
        messagesHistory.append(
            {
                "role": "system",
                "content": """
            Rewrite the previous response in a raw, real-time stream-of-consciousness style, as if actively solving a problem. Your response should feel like unpolished notes—messy, exploratory, and authentic. Show your full thought process, including missteps, dead ends, and course corrections. Use markers to signal mental states: Insights: "Wait -", "Hold on -", "Oh -", "Suddenly seeing -", "This connects to -". Testing: "Testing with -", "Breaking this down -", "Running an example -", "Checking if -". Problems: "Stuck on -", "This doesn't work because -", "Need to figure out -", "Not quite adding up -". Progress: "Making headway -", "Starting to see the pattern -", "Explains why -", "Now it makes sense -". Process: "Tracing the logic -", "Following this thread -", "Unpacking this idea -", "Exploring implications -". Uncertainty: "Maybe -", "Could be -", "Not sure yet -", "Might explain -". Transitions: "This leads to -", "Which means -", "Building on that -", "Connecting back to -".

            Lean into real-time realizations: "Wait, that won't work because…" or "Ah, I missed this…" Show evolving understanding through short paragraphs, with natural pauses where ideas shift. Structure your thought evolution as follows: Begin with an initial take: "This might work because…" or "At first glance…" Identify problems or angles: "Actually, this doesn't hold up because…" Test examples or counterexamples: "Let me try -", "What happens if -". Seek deeper patterns: "I'm seeing a connection -", "This ties back to -". Link broader implications: "This means -", "If this holds, then -".

            Admit confusion openly: "I don't get this yet", "Something's missing here". Reveal partial understanding: "I see why X, but not Y". Show failures and iterations: "Still not right - trying another approach". Embrace a debugging mindset, treating ideas like code—break them into steps, test logic, reveal failure modes, and iterate. Skip introductions and conclusions. Stop when you solve the problem or find clear next steps. Use short, direct sentences to mimic real-time thinking. The goal is to capture the messy, evolving nature of problem-solving and thought refinement.
        """,
            }
        )

        response = ollama.chat(messagesHistory)

        messagesHistory.append(response["message"])

        messagesHistory.append(
            {
                "role": "system",
                "content": """
            Now, taking into consideration your previious two answers, explain it better.
            """,
            }
        )

        response = ollama.chat(messagesHistory)

        messagesHistory.append(response["message"])
