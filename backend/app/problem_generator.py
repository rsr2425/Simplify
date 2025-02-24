from typing import List
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from backend.app.vectorstore import get_vector_db

class ProblemGenerator:
    def __init__(self):
        # Initialize prompts
        self.system_role_prompt = """
            You are a helpful assistant that generates questions based on a given context.
        """

        self.user_role_prompt = """
            Based on the following context about {query}, generate 5 relevant and specific questions.
            Make sure the questions can be answered using only the provided context.

            Context: {context}

            Generate 5 questions that test understanding of the material in the context.
            
            Return only a json object with the following format:
            {{
                "questions": ["question1", "question2", "question3", "question4", "question5"]
            }}
        """

        # Initialize chain components
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_role_prompt),
            ("user", self.user_role_prompt)
        ])
        
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.retriever = get_vector_db().as_retriever(search_kwargs={"k": 2})
        
        # Build the RAG chain
        self.rag_chain = (
            {"context": self.retriever, "query": RunnablePassthrough()}
            | self.chat_prompt
            | self.llm
            | StrOutputParser()
        )

    def generate_problems(self, query: str) -> List[str]:
        """
        Generate problems based on the user's query using RAG.
        
        Args:
            query (str): The topic to generate questions about
            
        Returns:
            List[str]: A list of generated questions
        """
        raw_result = self.rag_chain.invoke(query)
        result = json.loads(raw_result)
        return result["questions"]