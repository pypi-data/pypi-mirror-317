# langchain-s3-cached-embeddings

Proxies _**any**_ langchain `Embeddings` class such as `OpenAIEmbeddings`, `GoogleGenerativeAIEmbeddings`, persisting all generated embeddings to S3. This allows subsequent calls to _optionally_ leverage the cached embeddings, avoiding additional and unecessary cost of re-embedding. 
## Install

```bash
pip install langchain-s3-cached-embeddings
```

## Usage

```python
from langchain_s3_text_loaders import S3DirectoryLoader

   embeddings = S3EmbeddingsConduit(
        embeddings=OpenAIEmbeddings(model=model), # required
        bucket="my-embeddings-bucket", # required
        prefix="my-optional-prefix",
        filenaming_function=lamdba x: f"{x[0]}-{x[1].embedding.txt"}, # optional function to name your embedding file
        cache_behavior=CacheBehavior.NO_CACHE, # set to #CacheBehavior.ONLY_CACHE to use previously cached embeddings
    )

```

## License
MIT
