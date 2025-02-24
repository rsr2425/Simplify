from typing import List

# from backend.app.vectorstore import get_vector_db
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_openai import ChatOpenAI


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