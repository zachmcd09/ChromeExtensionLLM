import torch
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)

data = {"context": "", "text": "", "embeddings": []}

# Load the pre-trained S-BERT model

# Manually specify the directory where you downloaded the model files
model_directory = 'all-MiniLM-L6-v2'

# Load the model from the local directory
model = SentenceTransformer(model_directory)

@app.route('/encode', methods=['POST'])
def encode_text():
    """
    Encode the input text to semantic embeddings using S-BERT.
    """
    data = request.json
    text = data['text']
    embeddings = model.encode(text)
    return jsonify({'embeddings': embeddings.tolist()})

@app.route('/search', methods=['POST'])
def search():
    """
    Perform a semantic search based on the input query and return ranked results.
    """
    data = request.json
    query = data['query']
    documents = data['documents']
    
    # Encode the query and documents
    query_embedding = model.encode(query)
    document_embeddings = model.encode(documents, convert_to_tensor=True)
    
    # Compute cosine similarities between query and documents
    cos_scores = torch.nn.functional.cosine_similarity(query_embedding.unsqueeze(0), document_embeddings, dim=-1)
    scores = cos_scores.squeeze().tolist()
    
    # Rank the documents according to relevance
    ranked_docs = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    
    return jsonify({'results': ranked_docs})

if __name__ == '__main__':
    app.run()
