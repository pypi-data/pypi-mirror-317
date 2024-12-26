# langchain-dappier

This package contains the LangChain integration with Dappier

## Installation

```bash
pip install -U langchain-dappier
```

And you should configure credentials by setting the following environment variables:

```bash
export DAPPIER_API_KEY="your-api-key-here"
```

## Retrievers

`DappierRetriever` class exposes chat models from Dappier.

**Parameters:**

- `data_model_id` (str): Data model ID, starting with `dm_`. You can find the available data model IDs at [Dappier marketplace](https://platform.dappier.com/marketplace).
- `k` (int): Number of documents to return.
- `ref` (Optional[str]): Site domain where AI recommendations are displayed.
- `num_articles_ref` (int): Minimum number of articles from the specified `ref` domain. The rest will come from other sites within the RAG model.
- `search_algorithm` (Literal["most_recent", "most_recent_semantic", "semantic", "trending"]): Search algorithm for retrieving articles.
- `api_key` (Optional[str]): The API key used to interact with the Dappier APIs.

```python
from langchain_dappier import DappierRetriever

retriever = DappierRetriever(
    data_model_id="dm_01jagy9nqaeer9hxx8z1sk1jx6"
)

query = "latest tech news"

retriever.invoke(query)
```
