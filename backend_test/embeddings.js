// embedding_model.js
module.exports = EmbeddingModel;


const EmbeddingModel = require('./scripts/embedding_model');
const axios = require('axios');
const SentenceTransformer = require('sentence-transformers');


class EmbeddingModel {
  constructor() {
    this.model = new SentenceTransformer('nomic-ai/nomic-embed-text-v1.5-GGUF').then(model => model);
   }

  async generateEmbedding(text) {
    const model = await this.model; // Ensure the model is loaded before generating embeddings]
    this.getEmbedding
    return model.encode(text);
  }

  async searchDocumentsSimilarity(query, topK) {
    const queryEmbedding = await this.generateEmbedding(query);
    let similarities = {};

    for (const [document, embedding] of Object.entries(this.documentEmbeddings)) {
      const cosineSimilarity = this.cosineSimilarity(queryEmbedding, embedding);
      similarities[document] = cosineSimilarity;
     }

     // Sort documents by similarity score in descending order and return the top K
    return Object.entries(similarities)
       .sort((a, b) => b[1] - a[1])
       .slice(0, topK)
       .map(entry => entry[0]); // Return only document names
  }

  async cosineSimilarity(vecA, vecB) {
    const dotProduct = vecA.reduce((sum, a, idx) => sum + a * vecB[idx], 0);
    const magnitudeA = Math.sqrt(vecA.reduce((sum, val) => sum + val ** 2, 0));
    const magnitudeB = Math.sqrt(vecB.reduce((sum, val) => sum + val ** 2, 0));
    return dotProduct / (magnitudeA * magnitudeB);
  }
  async generateEmbedding(text) {
      if (this.embeddingCache[text]) {
        return this.embeddingCache[text];
      }
      const embedding = await this.embeddingModel.generateEmbedding(text);
      this.embeddingCache[text] = embedding;
      return embedding;
    }

  async sendToBackend(endpoint, data) {
    try {
      const response = await axios.post(`http://localhost:5000/${endpoint}`, data);
      return response.data;
     } catch (error) {
       // Handle errors appropriately
      throw new Error(`Error sending data to backend: ${error}`);
  }
  }

  async sendToOpenAI(prompt) {
    const data = {
      model: 'codegemma/codegemma-2b',
      prompt: prompt,
      max_tokens: 150,
      temperature: 0.5,
     };
    try {
      const response = await axios.post('https://api.openai.com/v1/engines/codegemma/completions', data, {
        headers: {
           'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
           'Content-Type': 'application/json',
         },
       });
      return response.data;
     } catch (error) {
       // Handle errors appropriately
      throw new Error(`Error sending data to OpenAI: ${error}`);
    }
  }

  async getEmbedding(inputText) {
    try {
      const response = await fetch('http://localhost:3000/embeddings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: [inputText] })
      });
  
      const { embeddings } = await response.json();
      return embeddings[0];  // Assuming only one embedding is needed
    } catch (error) {
      console.error('Error retrieving embeddings:', error);
    }
  }

  // Function to update DOM content globally
  async updateDomContent(newDomContent) {
  currentDomContent = newDomContent;
  domUpdated = true;
  }
}
