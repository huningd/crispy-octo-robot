from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Get the absolute path of the directory containing main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Setup for templates using an absolute path
templates_path = os.path.join(BASE_DIR, "src", "templates")
templates = Jinja2Templates(directory=templates_path)

# Load blog posts and embeddings
posts_path = os.path.join(BASE_DIR, "data", "blog_posts.json")
with open(posts_path, "r") as f:
    blog_posts = json.load(f)

embeddings_path = os.path.join(BASE_DIR, "data", "embeddings.json")
with open(embeddings_path, "r") as f:
    embedding_data = json.load(f)
    post_urls = embedding_data["urls"]
    post_embeddings = np.array(embedding_data["embeddings"])

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main page with a search form."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...)):
    """Processes the search query using semantic search and returns results."""
    # Encode the user's query
    query_embedding = model.encode([query])[0]

    # Calculate cosine similarity between the query and all post embeddings
    similarities = cosine_similarity([query_embedding], post_embeddings)[0]

    # Get the indices of the top 3 most similar posts
    top_indices = np.argsort(similarities)[-3:][::-1]

    # Retrieve the corresponding posts
    results = []
    for i in top_indices:
        # Find the post corresponding to the URL
        url = post_urls[i]
        for post in blog_posts:
            if post["url"] == url:
                results.append(post)
                break

    return templates.TemplateResponse("index.html", {"request": request, "results": results, "query": query})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
