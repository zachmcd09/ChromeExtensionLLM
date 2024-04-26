import json
import requests
import torch
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

def test_encode_endpoint():
    url = "http://127.0.0.1:5000/encode"
    text = ["I love playing soccer", "The Eiffel Tower is in Paris"]

    response = requests.post(url, json={'text': text})

    if response.status_code == 200:
        embeddings = json.loads(response.content)["embeddings"]
        assert len(embeddings) == len(text)
    else:
        raise Exception("Failed to test encode endpoint")

def test_search_endpoint():
    url = "http://127.0.0.1:5000/search"
    
    # Prepare test data
    query = ["Where is the Eiffel Tower?"]
    documents = [
        "I love playing soccer",
        "The Eiffel Tower is in Paris",
        "Visit the Colosseum in Rome"
    ]

    # Encode the query and documents before sending them to the API
    encoded_query = SentenceTransformer('all-MiniLM-L6-v2').encode(query, convert_to_tensor=True)
    encoded_documents = SentenceTransformer('all-MiniLM-L6-v2').encode(documents, convert_to_tensor=True)

    # Compute cosine similarities and rank the documents according to relevance
    scores = torch.nn.functional.cosine_similarity(encoded_query.unsqueeze(0), encoded_documents, dim=-1).squeeze().tolist()
    ranked_docs = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)

    # Prepare request data
    request_data = {
        "query": query[0],
        "documents": documents
    }

    response = requests.post(url, json=request_data)

    if response.status_code == 200:
        results = json.loads(response.content)["results"]
        assert len(results) == len(ranked_docs)
        for r, (doc, rank) in zip(results, ranked_docs):
            assert r['documents'] == doc and abs(r['score'] - rank) < 0.1
    else:
        raise Exception("Failed to test search endpoint")

if __name__ == '__main__':
    try:
        test_encode_endpoint()
        test_search_endpoint()
        print("All tests passed.")
    except Exception as e:
        print(f"Test failed: {e}")
