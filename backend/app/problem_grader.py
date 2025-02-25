from typing import Dict
import json

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from backend.app.vectorstore import get_vector_db

SYSTEM_ROLE_PROMPT = """
    You are a knowledgeable grading assistant that evaluates student answers based on provided context.
    You should determine if answers are correct and provide constructive feedback.
"""

USER_ROLE_PROMPT = """
    Grade the following student answer based on the provided context about {query}.
    
    Context: {context}
    
    Question: {problem}
    Student Answer: {answer}
    
    Evaluate if the answer is correct and provide brief feedback. Start with either "Correct" or "Incorrect" 
    followed by a brief explanation of why. Focus on the accuracy based on the context provided.
    
    Always begin your response with "Correct" or "Incorrect" and then provide a brief explanation of why.

    Your response should be direct and clear, for example:
    "Correct. The answer accurately explains [reason]" or 
    "Incorrect. While [partial understanding], the answer misses [key point]"
"""

class ProblemGradingPipeline:
    def __init__(self):
        self.chat_prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_ROLE_PROMPT),
            ("user", USER_ROLE_PROMPT)
        ])
        
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        self.retriever = get_vector_db().as_retriever(search_kwargs={"k": 2})
        
        self.rag_chain = (
            {
                "context": self.retriever, 
                "query": RunnablePassthrough(),
                "problem": RunnablePassthrough(),
                "answer": RunnablePassthrough()
            }
            | self.chat_prompt
            | self.llm
            | StrOutputParser()
        )

    async def grade(self, query: str, problem: str, answer: str) -> str:
        """
        Asynchronously grade a student's answer to a problem using RAG for context-aware evaluation.
        
        Args:
            query (str): The topic/context to use for grading
            problem (str): The question being answered
            answer (str): The student's answer to evaluate
            
        Returns:
            str: Grading response indicating if the answer is correct and providing feedback
        """
        return await self.rag_chain.ainvoke({
            "query": query,
            "problem": problem,
            "answer": answer
        }) 