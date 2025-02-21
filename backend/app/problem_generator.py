from typing import List

class ProblemGenerator:
    def generate_problems(self, query: str) -> List[str]:
        """
        Generate problems based on the user's query.
        """
        # For MVP, returning random sample questions
        sample_questions = [
            "What is the main purpose of this framework?",
            "How do you install this tool?",
            "What are the key components?",
            "Explain the basic workflow",
            "What are the best practices?"
        ]
        return sample_questions