import openai  # Ensure you have the OpenAI Python library installed
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain.prompts import ChatPromptTemplate
import shutil
import settings
import sys
from langchain.chat_models import ChatOpenAI

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"] 
CROMA_PATH = "chroma"

# Get query text from command line input
query_text = input("Enter your query text: ")

db = Chroma(persist_directory=CROMA_PATH, embedding_function=OpenAIEmbeddings())

results = db.similarity_search_with_relevance_scores(query_text, k=2)

if len(results) == 0 or results[0][1] < 0.7:
	print(f"Unable to find matching results.")
	sys.exit()

PROMPT_TEMPLATE="""
You are a Formala 1 Expert, and you will answer questions ina fun engaging way as if you are a comentator using the following content: 
{context}

--- 

Answer the question based on the above context: {query}
"""

context_text="\n\n---\n\n".join([ doc.page_content for doc, score in results])
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#raise Exception(prompt_template)
prompt = prompt_template.format(context=context_text, query=query_text)

model = ChatOpenAI()
response_text = model.predict(prompt)

#sources = [doc.metadata.get("source", None) for doc, _score in results]
formatted_response = f"Response: {response_text}"
print(formatted_response)
