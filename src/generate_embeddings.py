from sentence_transformers import SentenceTransformer
import json
import os

def main():
    """
    Generates sentence embeddings for the blog posts and saves them to a file.
    """
    # Load the blog posts
    posts_path = "data/blog_posts.json"
    with open(posts_path, "r") as f:
        blog_posts = json.load(f)

    # Load a pre-trained sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings for each post
    post_contents = [post['title'] + ". " + post['content'] for post in blog_posts]
    embeddings = model.encode(post_contents, show_progress_bar=True)

    # Save the embeddings to a file
    # We'll also store the corresponding URLs to map embeddings back to posts
    embedding_data = {
        "urls": [post['url'] for post in blog_posts],
        "embeddings": embeddings.tolist() # Convert numpy array to list for JSON
    }

    output_path = "data/embeddings.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(embedding_data, f)

    print(f"Successfully generated and saved embeddings for {len(blog_posts)} blog posts.")

if __name__ == "__main__":
    main()
