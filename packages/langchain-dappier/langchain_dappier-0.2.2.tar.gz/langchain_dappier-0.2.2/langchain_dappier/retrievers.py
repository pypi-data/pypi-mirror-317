"""Dappier retrievers."""

import os
from typing import Any, List, Literal, Optional

from dappier import Dappier, DappierAsync
from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class DappierRetriever(BaseRetriever):
    """Dappier retriever.

    Setup:
        Install ``langchain-dappier`` and set environment variable
        ``DAPPIER_API_KEY``.

        .. code-block:: bash

            pip install -U langchain-dappier
            export DAPPIER_API_KEY="your-api-key"

    Key init args:
        data_model_id: str
            Data model ID, starting with dm_.
            You can find the available data model IDs at:
            [Dappier marketplace.](https://platform.dappier.com/marketplace)
        k: int
            Number of documents to return.
        ref: Optional[str]
            Site domain where AI recommendations are displayed.
        num_articles_ref: int
            Minimum number of articles from the ref domain specified.
            The rest will come from other sites within the RAG model.
        search_algorithm: Literal[
            "most_recent",
            "most_recent_semantic",
            "semantic",
            "trending"
        ]
            Search algorithm for retrieving articles.
        api_key: Optional[str]
            The API key used to interact with the Dappier APIs.

    Instantiate:
        .. code-block:: python

            from langchain_dappier import DappierRetriever

            retriever = DappierRetriever(
                data_model_id="dm_01jagy9nqaeer9hxx8z1sk1jx6"
            )

    Usage:
        .. code-block:: python

            query = "latest tech news"

            retriever.invoke(query)

    Use within a chain:
        .. code-block:: python

            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.runnables import RunnablePassthrough
            from langchain_openai import ChatOpenAI

            prompt = ChatPromptTemplate.from_template(
                \"\"\"Answer the question based only on the context provided.

            Context: {context}

            Question: {question}\"\"\"
            )

            llm = ChatOpenAI(model="gpt-3.5-turbo-0125")


            chain = (
                RunnablePassthrough.assign(
                    context=(lambda x: x["question"]) | retriever
                )
                | prompt
                | ChatOpenAI(model="gpt-4-1106-preview")
                | StrOutputParser()
            )

            chain.invoke(
                {
                    "question": (
                        "What are the key highlights and outcomes from the latest "
                        "events covered in the article?"
                    )
                }
            )
    """

    data_model_id: str
    """Data model ID, starting with dm_."""
    k: int = 3
    """Number of documents to return."""
    ref: Optional[str] = None
    """Site domain where AI recommendations are displayed."""
    num_articles_ref: int = 0
    """Minimum number of articles from the ref domain specified.
    The rest will come from other sites within the RAG model."""
    search_algorithm: Literal[
        "most_recent", "most_recent_semantic", "semantic", "trending"
    ] = "most_recent"
    """Search algorithm for retrieving articles."""
    api_key: Optional[str] = None
    """The API key used to interact with the Dappier APIs."""

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun, **kwargs: Any
    ) -> List[Document]:
        """Get documents relevant to a query.

        Args:
            query: String to find relevant documents for
            run_manager: The callabacks handler to use
        Returns:
            List of relevant documents
        """
        try:
            if not self.data_model_id:
                raise ValueError("Data model id is not initialized.")
            dp_client = Dappier(api_key=self.api_key or os.environ["DAPPIER_API_KEY"])
            response = dp_client.get_ai_recommendations(
                query=query,
                data_model_id=self.data_model_id,
                similarity_top_k=kwargs.get("k", self.k),
                ref=self.ref,
                num_articles_ref=self.num_articles_ref,
                search_algorithm=self.search_algorithm,
            )
            return self._extract_documents(response=response)
        except Exception as e:
            raise ValueError(f"Error while retrieving documents: {e}") from e

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
        **kwargs: Any,
    ) -> List[Document]:
        """Asynchronously get documents relevant to a query.
        Args:
            query: String to find relevant docuements for
            run_manager: The callbacks handler to use
        Returns:
            List of relevant documents
        """
        try:
            dp_client = DappierAsync(
                api_key=self.api_key or os.environ["DAPPIER_API_KEY"]
            )
            async with dp_client as client:
                response = await client.get_ai_recommendations_async(
                    query=query,
                    data_model_id=self.data_model_id,
                    similarity_top_k=kwargs.get("k", self.k),
                    ref=self.ref,
                    num_articles_ref=self.num_articles_ref,
                    search_algorithm=self.search_algorithm,
                )
                return self._extract_documents(response=response)
        except Exception as e:
            raise ValueError(f"Error while retrieving documents: {e}") from e

    def _extract_documents(self, response: Any) -> List[Document]:
        """Extract documents from an api response"""

        from dappier.types import AIRecommendationsResponse

        docs: List[Document] = []
        rec_response: AIRecommendationsResponse = response
        if rec_response.response is None or rec_response.response.results is None:
            return docs
        for doc in rec_response.response.results:
            docs.append(
                Document(
                    page_content=doc.summary,
                    metadata={
                        "title": doc.title,
                        "author": doc.author,
                        "source_url": doc.source_url,
                        "image_url": doc.image_url,
                        "pubdata": doc.pubdate,
                    },
                )
            )
        return docs
