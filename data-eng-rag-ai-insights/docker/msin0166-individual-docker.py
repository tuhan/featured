import os
import requests
import neptune
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from statistics import mean
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEPTUNE_API_TOKEN = os.getenv("NEPTUNE_API_TOKEN")
NEPTUNE_PROJECT = os.getenv("NEPTUNE_PROJECT")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Init embedding + vectorstores
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_paths = {
    "eu_ai_act": "store/eu_ai_act_db",
    "hn_story": "store/hn_story_db",
    "hn_comment": "store/hn_comment_db",
    "llm_benchs_transparency": "store/llm_benchs_transparency_db"
}
stores = {
    name: Chroma(persist_directory=path, embedding_function=embedding)
    for name, path in vector_paths.items()
}

# Initialize Flask app
app = Flask(__name__)

@app.route("/rag", methods=["POST"])
def rag_query():
    neptune_run = neptune.init_run(project=NEPTUNE_PROJECT, api_token=NEPTUNE_API_TOKEN)
    neptune_run["debug/start"] = "RAG request received"

    try:
        data = request.get_json()
        query = data.get("question")
        top_k = int(data.get("top_k", 3))
        if not query:
            return jsonify({"error": "Missing 'question' field"}), 400

        docs, scores = [], []
        for name, store in stores.items():
            results = store.similarity_search_with_score(query, k=top_k)
            for doc, score in results:
                doc.metadata["source"] = name
                doc.metadata["similarity"] = score
                docs.append(doc)
                scores.append(score)

        context = "\n\n".join([f"[{doc.metadata['source']}] {doc.page_content.strip()}" for doc in docs])
        avg_similarity = round(mean(scores), 4) if scores else None
        min_similarity = round(min(scores), 4) if scores else None

        prompt = f"""
You are an expert assistant in AI policy.

Only use the context provided to answer the user's question. Do not invent or guess. If the context is not sufficient, respond with:
"I cannot answer this confidently based on the provided sources."

Always cite sources using [source].

Context:
{context}

Question:
{query}

Answer:
"""
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_URL, headers=headers, json=payload)

        if response.status_code == 200:
            json_resp = response.json()
            answer = json_resp["candidates"][0]["content"]["parts"][0]["text"]
            hallucination_flag = "I cannot answer" in answer

            # Neptune logging
            neptune_run["question"] = query
            neptune_run["answer"] = answer
            neptune_run["prompt/full"] = prompt
            neptune_run["retrieval/avg_similarity"].log(avg_similarity)
            neptune_run["retrieval/min_similarity"].log(min_similarity)
            neptune_run["hallucination/flagged"] = hallucination_flag
            neptune_run["sources"] = list(set(doc.metadata["source"] for doc in docs))

            return jsonify({
                "question": query,
                "answer": answer,
                "sources": list(set(doc.metadata["source"] for doc in docs)),
                "avg_similarity": avg_similarity,
                "hallucination_flag": hallucination_flag
            })

        else:
            neptune_run["error/gemini_status"] = response.status_code
            neptune_run["error/gemini_text"] = response.text
            return jsonify({"error": response.text}), response.status_code

    except Exception as e:
        neptune_run["error/exception"] = str(e)
        return jsonify({"error": "Internal error", "details": str(e)}), 500

    finally:
        neptune_run.stop()

# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)