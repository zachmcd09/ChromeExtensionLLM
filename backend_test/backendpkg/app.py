from fastapi import FastAPI, HTTPException
from sentence_transformers import util
from langchain.text_splitter import RecursiveCharacterTextSplitter
from huggingface_hub import snapshot_download
import numpy as np
from bs4 import BeautifulSoup
import argparse
import requests
#import faiss
import re

app = FastAPI()
LMCLIENT = "http://localhost:1234"


class LMStudioEmbedder:
    def __init__(self, dom, query):
        self.page = extract_text_from_tags(dom)
        self.query = query

        self.page_embeddings = np.array(LMStudioEmbedder.get_embeddings(split_into_chunks(self.page)))
        self.query_embeddings = np.array(LMStudioEmbedder.get_embeddings(split_into_chunks(self.query)))
        self.total_embeddings = np.array(self.page_embeddings + self.query_embeddings)
        #self.index = faiss.IndexFlatL2(self.total_embeddings.shape[1])
        #self.index.add(self.total_embeddings)
        #self.index.nprobe = 10
        #self.index.verbose = True
        #self.index.show_nearest(self.lmstudio_embeddings, 10)
    
    def get_embeddings(self, chunks, model="nomic-ai/nomic-embed-text-v1.5-GGUF"):
        for text in enumerate(chunks):
            text = text.replace("\n", " ")
            text.strip("\n")

            response = requests.post(LMCLIENT, json={'text': text})
            if response.status_code == 200:
                # Parse the JSON response to extract the embedding array
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    embedding_data = data['data'][0]  # Assuming the first item contains the embedding
                    if 'embedding' in embedding_data:
                        return np.array(embedding_data['embedding'])
                    else:
                        raise Exception("Missing 'embedding' field in response.")
                else:
                    raise Exception("Missing or invalid 'data' field in response.")
            else:
                # Handle error appropriately
                raise Exception(f"Error retrieving embedding from LMStudio: {response.text}")


def split_into_chunks(text, chunk_size=500):
    # Split the text into tokens (words and punctuation)
    tokens = re.findall(r'\w+|[^\w\s]', text)
    
    # Group tokens into chunks of desired size
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    
    # Join each chunk back into a string
    chunked_texts = [' '.join(chunk) for chunk in chunks]
    
    return chunked_texts

# Example usage:
text = "Your very long text goes here..."
chunked_texts = split_into_chunks(text, 500)
for i, chunk in enumerate(chunked_texts):
    print(f"Chunk {i+1}: {chunk}")


class SemanticSearch:
    def __init__(self, LMStudioEmbedder, text, query):
        self.splitter = split_into_chunks(text)
        self.model = LMStudioEmbedder

    @app.get("/search/{documents}>>>{query}")
    def search(self, query: str, chunks: list[float]):
        """
        Perform a semantic search over the embedded chunks given a query.
        """
        try:
            
            # Ensure that document embeddings are provided as a numpy array
            chunk_embeddings = np.array(chunks)

            # Calculate cosine similarity between query embedding and each document embedding
            similarities = util.pytorch_cos_sim(LMStudioEmbedder.query_embeddings, chunk_embeddings)[0]
            
            # Sort documents based on similarities (in descending order)
            sorted_doc_indices = np.argsort(-similarities)
            print(sorted_doc_indices)
            return {"sorted_documents": sorted_doc_indices.tolist()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    
def extract_text_from_tags(html_content):
    """
    Extracts text from HTML content focusing on specified tags like <p>, <h1>, <h2>, etc.
    
    :param html_content: str, the HTML content
    :return: list of str, a list containing extracted text from specified tags
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    tags_of_interest = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    extracted_texts = []
    
    for tag in tags_of_interest:
        for element in soup.find_all(tag):
            extracted_texts.append(element.get_text(strip=True))
    
    return extracted_texts


if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Semantic Search with Sentence Transformers and LangChain.')
    #parser.add_argument('--text', type=str, required=True, help='Input large text block.')
    
    #parser.add_argument('--query', type=str, required=True, help='Input query to search within text.')
    text = "I was born Feb. 12, 1809, in Hardin County, Kentucky. My parents were both born in Virginia, of undistinguished families–second families, perhaps I should say. My mother, who died in my tenth year, was of a family of the name of Hanks…. My father … removed from Kentucky to … Indiana, in my eighth year…. It was a wild region, with many bears and other wild animals still in the woods. There I grew up…. Of course when I came of age I did not know much. Still somehow, I could read, write, and cipher … but that was all."
    query = "When was lincoln born?"
    #args = parser.parse_args()
    
    lmstudio = LMStudioEmbedder(text, query)
    
    search = SemanticSearch(lmstudio, text, query)
    
    
    results = search.search(extract_text_from_tags(text), query)
    for result in results:
        print(f"Chunk: {result[0]}, Similarity Score: {result[1]:.1f}, Chunk Text: {result[2]}")