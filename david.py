import warnings

# To suppress all warnings
warnings.filterwarnings("ignore")

# To suppress a specific warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time
from common import *
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
import math

def generate_academic_reference(data):
    reference = ""
    if 'author' in data and data['author'] != 'Unknown':
        reference += data['author'] + ". "
    if 'published on' in data:
        reference += "(" + data['published on'] + "). "
    if 'source' in data:
        reference += "\033[4m" + data['source'] + "\033[0m" + ". "  # Making the link underlined
    return reference.strip()

def url_to_readable_text(urls):
    readable_texts = []
    for url in urls:
        # Split the URL by "/"
        parts = url.split("/")

        # Get the last part of the URL
        last_part = parts[-1]

        # Split the last part by "."
        filename_parts = last_part.split(".")

        # Extract the date from the filename
        date = filename_parts[0]

        # Replace "-" with " " in the date
        date = date.replace("-", " ")

        # Extract the article name from the filename
        article_name = filename_parts[1]

        # Remove the leading and trailing quotes from the article name
        article_name = article_name.strip("'")

        # Replace "-" with " " in the article name
        article_name = article_name.replace("-", " ")

        # Capitalize the first letter of each word in the article name
        article_name = article_name.title()

        # Construct the human-readable text
        readable_text = f"On {date},  '{article_name}'"
        
        readable_texts.append(readable_text)

    return readable_texts


# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"] 
CROMA_PATH = "chroma"

# Get query text from command line input

# Call the function to print the intro
print_colorful_intro("Wellcome to my chat Room")

query_text = input("\033[1;31mAsk me any F1 Related Question: \033[0m")

db = Chroma(persist_directory=CROMA_PATH, embedding_function=OpenAIEmbeddings())

results = db.similarity_search_with_relevance_scores(query_text, k=5)

if len(results) == 0 or results[0][1] < 0.7:
	print(f"Unable to find matching results.")
	sys.exit()

PROMPT_TEMPLATE="""
You are a Formala 1 Expert Named David, and you will answer questions in a fun engaging way as if you are a comentator using the following content, you don't need to introduce your self: 
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

formatted_response = f"\n\n{response_text}"
print("\n\n\033[1;34mMy Response: \033[0m")
print(formatted_response)

print("\n\n\033[1;34mMy Sources \033[0m")
for doc, _score in results:
    print("\033[1;32m%s%% \033[0m %s" % (math.ceil(_score * 100), generate_academic_reference(doc.metadata) ) )


