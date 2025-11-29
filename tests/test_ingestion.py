import os
import unittest
from unittest.mock import patch, MagicMock
from src.ingestion import main as ingestion_main

class TestIngestion(unittest.TestCase):

    @patch('src.ingestion.requests.get')
    def test_ingestion_creates_files(self, mock_get):
        # Mock the RSS feed response
        mock_rss_response = MagicMock()
        mock_rss_response.status_code = 200
        mock_rss_response.content = b"""
        <rss>
            <channel>
                <item>
                    <title>My First Dev Post</title>
                    <link>https://huningd.github.io/dev-blog/blog/2025/03/25/my-first-dev-post/</link>
                    <pubDate>Tue, 25 Mar 2025 14:02:23 +0000</pubDate>
                </item>
            </channel>
        </rss>
        """

        # Mock the blog post response
        mock_post_response = MagicMock()
        mock_post_response.status_code = 200
        mock_post_response.content = b"""
        <html>
            <head>
                <title>My First Dev Post</title>
            </head>
            <body>
                <h1>My First Dev Post</h1>
                <article>I've been exploring MkDocs lately...</article>
            </body>
        </html>
        """

        # Set the side effect for the mock
        mock_get.side_effect = [mock_rss_response, mock_post_response]

        # Clean up any existing files
        if os.path.exists("data/blog_posts.json"):
            os.remove("data/blog_posts.json")
        if os.path.exists("data/index.json"):
            os.remove("data/index.json")

        # Run the ingestion script
        ingestion_main()

        # Check that the files were created
        self.assertTrue(os.path.exists("data/blog_posts.json"))
        self.assertTrue(os.path.exists("data/index.json"))

if __name__ == "__main__":
    unittest.main()
