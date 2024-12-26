from typing import Any, List, Dict, Optional, Tuple, Union
from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage


from .searcher import EnhancedResearchPaperSearch


class ResearchPaperRAG:
    def __init__(
        self,
        llm: ChatOpenAI,
        vector_store_path: str = "research_papers_store",
    ):
        """
        Initialize the RAG system

        Args:
            vector_store_path: Path to the saved vector store
            model_name: Name of the LLM model to use
            temperature: Temperature setting for the LLM
        """
        self.searcher = EnhancedResearchPaperSearch(vector_store_path)
        self.llm = llm

        # System prompt for research writing assistance
        self.system_prompt = """You are a research assistant helping to write academic content. 
        Your task is to help answer questions and generate text using the provided research paper excerpts as references.
        
        Guidelines:
        - Use the provided excerpts to support your response
        - Cite the papers using [Author] format where Author is the filename
        - Be precise and academic in tone
        - If the retrieved excerpts are not relevant, acknowledge this
        - Synthesize information from multiple sources when possible
        - Be explicit about any limitations in the provided excerpts
        """

    def _format_context(self, results: List[Dict]) -> Tuple[str, List[str]]:
        """
        Format search results into context string and track sources

        Args:
            results: List of search results

        Returns:
            Tuple of (formatted context string, list of source papers)
        """
        context_parts = []
        sources = []

        for i, result in enumerate(results, 1):
            # Extract paper name without .pdf extension
            paper_name = result["paper_name"].replace(".pdf", "")
            sources.append(paper_name)

            # Format the excerpt with paper reference
            context_parts.append(
                f"Excerpt {i} from [{paper_name}]:\n{result['text'].strip()}\n"
            )

        return "\n\n".join(context_parts), sources

    def _build_prompt(
        self, query: str, context: str, response_format: Optional[str] = None
    ) -> List:
        """
        Build the chat prompt with system message, context, and query

        Args:
            query: User's query
            context: Formatted context from search results
            response_format: Optional specific format for the response

        Returns:
            List of chat messages
        """
        format_instruction = ""
        if response_format:
            format_instruction = f"\nPlease provide your response in the following format: {response_format}"

        messages = [
            SystemMessage(content=self.system_prompt + format_instruction),
            HumanMessage(
                content=f"""Here are relevant excerpts from research papers:

{context}

Based on these excerpts, please help with the following query:
{query}"""
            ),
        ]

        return messages

    def generate_response(
        self,
        query: str,
        initial_k: int = 10,
        final_k: int = 5,
        response_format: Optional[str] = None,
        return_sources: bool = False,
    ) -> Union[str, Tuple[str, List[str]]]:
        """
        Generate a response using RAG

        Args:
            query: User's research-related query
            initial_k: Number of initial search results
            final_k: Number of results after reranking
            response_format: Optional specific format for the response
            return_sources: Whether to return the source papers

        Returns:
            Generated response or tuple of (response, source papers) if return_sources=True
        """
        # Get search results
        results = self.searcher.search(query, initial_k=initial_k, final_k=final_k)

        if not results:
            response = "I couldn't find any relevant excerpts from the research papers to answer your query."
            return (response, []) if return_sources else response

        # Format context and track sources
        context, sources = self._format_context(results)

        # Build prompt and generate response
        messages = self._build_prompt(query, context, response_format)
        response = self.llm.invoke(messages).content

        return (response, sources) if return_sources else response

    def generate_literature_review(
        self,
        topic: str,
        initial_k: int = 15,
        final_k: int = 8,
        organization_style: str = "chronological",
        include_metadata: bool = False,
        focus_areas: Optional[List[str]] = None,
    ) -> Tuple[str, List[str]]:
        """
        Generate a comprehensive literature review on a topic with improved organization and depth.

        Args:
            topic: Research topic for the literature review
            initial_k: Number of initial search results (default: 15)
            final_k: Number of results after reranking (default: 8)
            organization_style: How to organize the review - "chronological", "thematic", or "methodological"
            include_metadata: Whether to include paper metadata in the review
            focus_areas: Optional list of specific aspects to focus on

        Returns:
            Tuple of (literature review text, source papers, metadata)
        """
        # Build focus area string if provided
        focus_instruction = ""
        if focus_areas:
            focus_instruction = (
                f"\nPlease specifically address these aspects: {', '.join(focus_areas)}"
            )

        # Enhanced format instruction with better structure and organization
        format_instruction = f"""
        Please organize this literature review {organization_style}ly, following this structure:

        1. Executive Summary (2-3 sentences)
            - Core research question/topic
            - Brief overview of the field's current state
            - Key findings preview

        2. Background and Context
            - Historical development of the research area
            - Key theoretical frameworks
            - Critical definitions and concepts

        3. Main Body Analysis
            - Detailed synthesis of research findings
            - Integration of multiple perspectives
            - Clear delineation of agreements and contradictions
            - Critical evaluation of methodologies used{focus_instruction}

        4. Research Gaps and Future Directions
            - Identify understudied areas
            - Highlight methodological limitations
            - Suggest promising research directions

        5. Conclusion
            - Synthesize major themes
            - Assess the overall state of research
            - Implications for theory and practice

        Citation and Cross-referencing Guidelines:
        - For each major claim or finding, cite multiple sources that support or contradict it
        - Use phrases like "Several studies [Author1, Author2, Author3] have found..."
        - When presenting contradictory findings, cite all relevant sources: "While [Author1] argues X, [Author2] and [Author3] demonstrate Y"
        - Group related findings from multiple sources: "The importance of Z has been established through multiple studies [Author1, Author2, Author3]"
        - When synthesizing themes, reference multiple supporting works: "A common theme across studies [Author1, Author2, Author3] is..."
        - For methodological discussions, compare approaches across multiple studies
        - Highlight when multiple independent studies reach similar conclusions
        - Note when findings are supported by only a single source versus multiple sources

        Additional Guidelines:
        - Maintain clear transitions between sections
        - Use topic sentences to guide reader understanding
        - Compare and contrast findings across studies
        - Highlight methodological strengths and limitations
        - Include specific examples and evidence
        {f'- Address each focus area: {", ".join(focus_areas)}' if focus_areas else ''}
        """

        # Build the search query with expanded context
        expanded_query = f"""
        Topic: {topic}
        Required information:
        - Recent developments and historical context
        - Key theoretical frameworks
        - Major findings and contradictions
        - Research gaps and future directions
        - Evidence and counter-evidence from multiple sources
        """

        # Get response with enhanced format
        response, sources = self.generate_response(
            query=expanded_query,
            initial_k=initial_k,
            final_k=final_k,
            response_format=format_instruction,
            return_sources=True,
        )

        # Extract and organize metadata about the sources
        metadata = {}
        if include_metadata:
            metadata = {
                "source_distribution": {
                    "total_sources": len(sources),
                    "unique_sources": len(set(sources)),
                },
                "topic": topic,
                "organization_style": organization_style,
                "focus_areas": focus_areas if focus_areas else [],
                "search_parameters": {
                    "initial_k": initial_k,
                    "final_k": final_k,
                },
            }

        return response, sources

    def generate_citation_evidence(
        self, claim: str, initial_k: int = 8, final_k: int = 3
    ) -> Tuple[str, List[str]]:
        """
        Find evidence to support or refute a research claim

        Args:
            claim: Research claim to evaluate
            initial_k: Number of initial search results
            final_k: Number of results after reranking

        Returns:
            Tuple of (evidence analysis, source papers)
        """
        format_instruction = """
        Provide:
        1. Analysis of how the evidence supports or challenges the claim
        2. Direct quotes from papers where relevant
        3. Clear citations for all evidence
        4. Assessment of the strength of evidence
        """

        response, sources = self.generate_response(
            query=f"Evaluate the following research claim with evidence: {claim}",
            initial_k=initial_k,
            final_k=final_k,
            response_format=format_instruction,
            return_sources=True,
        )

        return response, sources
