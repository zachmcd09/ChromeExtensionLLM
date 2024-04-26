import { LMStudioClient } from "@lmstudio/sdk";

const client = new LMStudioClient({
  baseUrl: "ws://127.0.0.1:8080",
});

await client.llm.load("NousResearch/Hermes-2-Pro-Mistral-7B-GGUF", {
    noHup: true,
    identifier: "my-model",

  });
  
  // The model stays loaded even after the client disconnects
  const myModel = client.llm.get("my-model");
