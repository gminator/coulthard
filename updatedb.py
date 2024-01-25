import openai  # Ensure you have the OpenAI Python library installed
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
import shutil
import settings

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"] 

def delete_chroma_directory():
    """Delete the 'Chroma' directory if it exists."""
    chroma_directory = os.path.join(os.getcwd(), "chroma")
    if os.path.exists(chroma_directory):
        shutil.rmtree(chroma_directory)
        print(f"Deleted Chroma directory at '{chroma_directory}'")
    else:
        print("Chroma directory does not exist.")

def read_files_in_directory(limit=None, encoding='utf-8', errors='ignore'):
    """Read files in the 'RAG' directory located in the current working directory."""
    directory_path = os.path.join(os.getcwd(), "RAG")
    
    # Get a list of files sorted by their filenames (which include the date)
    files_sorted = sorted(os.listdir(directory_path), reverse=True)
    
    # Initialize variables to track the number of files read and the file contents
    file_count = 0
    file_contents = []

    # Iterate over sorted files
    for filename in files_sorted:
        # Check if the limit has been reached
        if limit is not None and file_count >= limit:
            break
        
        # Read file contents
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding=encoding, errors=errors) as file:
                file_contents.append(file.read())
                file_count += 1
    
    return file_contents

delete_chroma_directory()
documents = [ Document(page_content=t)for t in read_files_in_directory()]

print("%s Documents" % len(documents))

CROMA_PATH = "chroma"

db = Chroma.from_documents(documents, OpenAIEmbeddings(), persist_directory=CROMA_PATH)