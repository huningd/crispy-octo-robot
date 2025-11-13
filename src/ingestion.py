import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import os
import re

def create_index(posts):
    """Creates a simple keyword index from the blog posts."""
    index = {}
    for post in posts:
        # Combine title and content for indexing
        text_to_index = post['title'] + " " + post['content']
        # Simple tokenization and normalization
        words = re.findall(r'\b\w+\b', text_to_index.lower())

        for word in set(words): # Use set to count each word once per doc
            if word not in index:
                index[word] = []
            index[word].append(post['url'])

    return index

def main():
    """
    Fetches blog posts from the RSS feed, scrapes their content,
    saves the data to a JSON file, and creates a keyword index.
    """

    # URL of the RSS feed
    rss_url = "https://huningd.github.io/dev-blog/feed_rss_created.xml"

    # Fetch the RSS feed
    response = requests.get(rss_url)
    response.raise_for_status()

    # Parse the XML
    root = ET.fromstring(response.content)

    blog_posts = []

    # Iterate over each item in the RSS feed
    for item in root.findall(".//item"):
        # Extract the post URL
        post_url = item.find("link").text

        # Filter out non-post URLs (like category pages)
        if not re.search(r'/\d{4}/\d{2}/\d{2}/', post_url):
            continue

        # Fetch the post content
        post_response = requests.get(post_url)
        post_response.raise_for_status()

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(post_response.content, "html.parser")

        # Extract the title
        title = soup.find("h1").text

        # Extract the publication date
        pub_date = item.find("pubDate").text

        # Extract the full text content
        content_html = soup.find("article")
        if content_html:
            content = content_html.get_text()
            # Remove the title from the content to avoid duplication
            content = content.replace(title, "").strip()
        else:
            content = ""

        # Add the post to our list
        blog_posts.append({
            "title": title,
            "url": post_url,
            "pub_date": pub_date,
            "content": content
        })

    # Save the blog posts to a JSON file
    posts_output_path = "data/blog_posts.json"
    os.makedirs(os.path.dirname(posts_output_path), exist_ok=True)
    with open(posts_output_path, "w") as f:
        json.dump(blog_posts, f, indent=4)

    print(f"Successfully ingested {len(blog_posts)} blog posts.")

    # Create and save the index
    index = create_index(blog_posts)
    index_output_path = "data/index.json"
    with open(index_output_path, "w") as f:
        json.dump(index, f, indent=4)

    print(f"Successfully created index with {len(index)} keywords.")

if __name__ == "__main__":
    main()
