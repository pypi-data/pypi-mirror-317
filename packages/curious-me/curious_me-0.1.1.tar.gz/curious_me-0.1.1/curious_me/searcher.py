from sentence_transformers import CrossEncoder
from typing import List, Dict

from .vector_store import ResearchPaperSearch


class ResearchPaperReranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """
        Initialize the reranker with a cross-encoder model

        Args:
            model_name: Name of the cross-encoder model to use for reranking
        """
        self.cross_encoder = CrossEncoder(model_name)

    def rerank(
        self, query: str, initial_results: List[Dict], top_k: int = None
    ) -> List[Dict]:
        """
        Rerank the initial search results using cross-encoder

        Args:
            query: Original search query
            initial_results: List of initial search results from vector search
            top_k: Number of results to return after reranking (defaults to all)

        Returns:
            List of reranked results with updated scores
        """
        if not initial_results:
            return []

        # Prepare pairs for cross-encoder
        pairs = [(query, result["text"]) for result in initial_results]

        # Get cross-encoder scores
        cross_scores = self.cross_encoder.predict(pairs)

        # Create new results with cross-encoder scores
        reranked_results = []
        for idx, (score, result) in enumerate(zip(cross_scores, initial_results)):
            reranked_result = result.copy()
            reranked_result.update(
                {
                    "initial_score": result["similarity_score"],
                    "rerank_score": float(score),  # Convert numpy float to Python float
                }
            )
            reranked_results.append(reranked_result)

        # Sort by rerank score in descending order
        reranked_results = sorted(
            reranked_results, key=lambda x: x["rerank_score"], reverse=True
        )

        # Return top_k results if specified
        if top_k is not None:
            reranked_results = reranked_results[:top_k]

        return reranked_results


class EnhancedResearchPaperSearch:
    def __init__(self, vector_store_path: str = "research_papers_store"):
        """
        Initialize the enhanced search utility with both vector search and reranking

        Args:
            vector_store_path: Path to the saved vector store
        """
        self.base_searcher = ResearchPaperSearch(vector_store_path)
        self.reranker = ResearchPaperReranker()

    def search(self, query: str, initial_k: int = 10, final_k: int = 3) -> List[Dict]:
        """
        Perform enhanced search with reranking

        Args:
            query: Search query string
            initial_k: Number of results to retrieve from vector search
            final_k: Number of results to return after reranking

        Returns:
            List of reranked search results
        """
        # Get initial results
        initial_results = self.base_searcher.search(query, k=initial_k)

        # Rerank results
        reranked_results = self.reranker.rerank(query, initial_results, top_k=final_k)

        return reranked_results

    def pretty_print_results(self, results: List[Dict]):
        """
        Print search results in a readable format

        Args:
            results: List of reranked search results
        """
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}")
            print("=" * 50)
            print(f"Paper: {result['paper_name']}")
            print(f"Initial Score: {result['initial_score']:.4f}")
            print(f"Rerank Score: {result['rerank_score']:.4f}")
            print("-" * 50)
            print("Relevant Text:")
            print(result["text"])
            print("=" * 50)
