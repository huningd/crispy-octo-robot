# crispy-octo-robot
Example app for demonstrating NLWeb

## Getting Started

1.  **Create the virtual environment:**
    ```bash
    uv venv
    ```

2.  **Install dependencies:**
    ```bash
    uv pip sync --all-extras pyproject.toml
    ```

3. **Install the additional dependencies:**
    ```bash
    uv pip install requests beautifulsoup4 fastapi uvicorn python-multipart jinja2 sentence-transformers scikit-learn
    ```

4.  **Ingest the blog content:**
    Before running the application, you need to ingest the blog content and generate the embeddings.
    ```bash
    uv run python src/ingestion.py
    uv run python src/generate_embeddings.py
    ```

5.  **Run the web server:**
    ```bash
    uv run uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The application will be available at `http://localhost:8000`.

## Demo Queries

Here are some sample questions you can ask:

*   What is the main topic of this blog?
*   Tell me about MkDocs.
*   What has the author been doing lately?
*   Any posts about Python?
*   What is the first post about?
