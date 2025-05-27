from typing import List, Dict


class ChatMemory:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversation_history: List[Dict] = [
            {
                "role": "system",
                "content": (
                    "You are Nural, an intelligent internal knowledge assistant that understands "
                    "employee skills, experience, and project history. Use the provided context to "
                    "answer questions accurately. When pronouns like 'he', 'she', or 'they' are used, "
                    "refer to the last person mentioned in our conversation. Maintain conversation "
                    "context and refer back to previous questions when relevant. Be concise and helpful. Also give a follow up question at the"
                )
            }
        ]

    def add_interaction(self, context: str, question: str, answer: str) -> None:
        """Add a Q&A interaction with its context to the conversation history."""
        # Format the prompt to include both context and conversation history
        prompt = f"""Context from knowledge base:
{context}

User Question: {question}"""
        
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": answer})

        # Keep conversation history at a manageable size
        while len(self.conversation_history) > self.max_history * 2 + 1:  # +1 for system message
            # Remove oldest Q&A pair but keep system message
            self.conversation_history.pop(1)
            self.conversation_history.pop(1)

    def get_history(self) -> List[Dict]:
        """Get the current conversation history."""
        return self.conversation_history

    def clear(self) -> None:
        """Clear conversation history while keeping system message."""
        system_msg = self.conversation_history[0]
        self.conversation_history = [system_msg] 