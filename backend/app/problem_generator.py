from operator import itemgetter
from typing import List
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from backend.app.vectorstore import get_vector_db

MODEL = "gpt-3.5-turbo"

SYSTEM_ROLE_PROMPT = """
    You are a helpful assistant that generates questions based on a given context.
"""

USER_ROLE_PROMPT = """
    Based on the following context about {query}, generate 5 relevant and specific questions.
    Make sure the questions can be answered using only the provided context.

    Context: {context}

    Generate 5 questions that test understanding of the material in the context.
    
    Return only a json object with the following format:
    {{
        "questions": ["question1", "question2", "question3", "question4", "question5"]
    }}
"""


class ProblemGenerationPipeline:
    def __init__(self, return_context: bool = False, embedding_model_id: str = None):
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_ROLE_PROMPT),
            ("user", USER_ROLE_PROMPT)
        ])
        
        self.llm = ChatOpenAI(model=MODEL, temperature=0.7)
        self.retriever = get_vector_db(embedding_model_id).as_retriever(search_kwargs={"k": 2})
        
        # TODO: This is a hack to get the context for the questions. Very messy interface.
        self.return_context = return_context
        if not return_context:
            self.rag_chain = (
                {"context": self.retriever, "query": RunnablePassthrough()}
                | self.chat_prompt
                | self.llm
                | StrOutputParser()
            )
        else:
            # response looks like: {response: str, context: List[Document]}
            self.rag_chain = (
                {"context": itemgetter("query") | self.retriever, "query": itemgetter("query")}
                | RunnablePassthrough.assign(context=itemgetter("context"))
                | {"response": self.chat_prompt | self.llm | StrOutputParser(), "context": itemgetter("context")}
            )

    def generate_problems(self, query: str, debug: bool = False) -> List[str]:
        """
        Generate problems based on the user's query using RAG.
        
        Args:
            query (str): The topic to generate questions about
            
        Returns:
            List[str]: A list of generated questions
        """
        raw_result = self.rag_chain.invoke(query)
        if debug:
            print(raw_result)
        # raw_result is a dict with keys "response" and "context" when return_context is True
        if self.return_context:
            return raw_result
        # raw_result is a string when return_context is False
        else:
            return json.loads(raw_result)["questions"]