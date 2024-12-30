import unittest
from unittest.mock import patch
from moto import mock_aws
import boto3
from .mock_embeddings import MockEmbeddings
from langchain_s3_cached_embeddings import S3CachedEmbeddings, CacheBehavior


class TestS3CachedEmbeddings(unittest.TestCase):
    
    def setUp(self):
        """Setup method to initialize the objects before each test."""
        # Mocking the S3 service using moto
        self.mock_s3 = mock_aws()
        self.mock_s3.start()

        # Create an S3 bucket for the mock
        self.bucket_name = "test-bucket"
        self.prefix = "test-prefix"
        
        # Initialize the mock embeddings and the S3CachedEmbeddings object
        self.mock_embeddings = MockEmbeddings()
        self.s3_cached_embeddings = S3CachedEmbeddings(
            embeddings=self.mock_embeddings,
            bucket=self.bucket_name,
            prefix=self.prefix,
            cache_behavior=CacheBehavior.NO_CACHE
        )
        self.texts = ["doc1", "doc2", "doc3"]  # Sample input texts for embedding

        # Create the S3 bucket (since we are mocking, this will be an in-memory bucket)
        s3_client = boto3.client('s3', region_name="us-east-1")
        s3_client.create_bucket(Bucket=self.bucket_name)

    def tearDown(self):
        """Cleanup after each test."""
        # Stop the mock S3 service after each test
        self.mock_s3.stop()

    @patch("langchain_s3_cached_embeddings.S3CachedEmbeddings._upload_content_in_batches")
    @patch("langchain_s3_cached_embeddings.S3CachedEmbeddings._retrieve_content_in_batches")
    def test_embed_documents_no_cache(self, mock_retrieve, mock_upload):
        """Test that embed_documents works as expected with NO_CACHE behavior."""
        # Mock the retrieval to return empty (simulate no cache hit)
        mock_retrieve.return_value = []

        embeddings = self.s3_cached_embeddings.embed_documents(self.texts)

        self.assertEqual(len(embeddings), 3)
        for embedding in embeddings:
            self.assertEqual(len(embedding), 300)
        
    
        mock_upload.assert_called()

if __name__ == "__main__":
    unittest.main()