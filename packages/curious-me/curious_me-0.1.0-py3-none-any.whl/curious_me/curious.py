import os
from threading import Thread
import time
from typing import TYPE_CHECKING
from urllib.request import urlretrieve
import arxiv
from tqdm import tqdm

from curious_me.rag import ResearchPaperRAG
from curious_me.vector_store import ResearchPaperVectorStore

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI


class Curious:
    def __init__(
        self,
        topics: list[str],
        llm: "ChatOpenAI",
        max_papers: int = 25,
        skip_search: bool = False,
    ):

        self.topics = topics
        self.pdf_folder = "research_papers"
        self.llm = llm
        self.max_results = max_papers
        if not skip_search:
            self.search_papers()
            self.build_vec_store()
        self.rag = ResearchPaperRAG(self.llm)

    def search_papers(self):
        """
        Search research papers based on the query and topic
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        pdf_folder_path = os.path.join(current_path, self.pdf_folder)
        current_year = time.localtime().tm_year
        if not os.path.exists(pdf_folder_path):
            os.makedirs(pdf_folder_path)

        print("Searching and fetching research papers...")
        threads: list[Thread] = []
        for topic in self.topics:
            threads.append(
                Thread(
                    target=self.fetch_research_papers,
                    args=(pdf_folder_path, current_year, topic),
                )
            )
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("All papers fetched successfully!")

    def fetch_research_papers(self, pdf_folder_path, current_year, topic):
        search = arxiv.Search(
            query=topic,
            max_results=self.max_results
            * 4,  # Increase initial results to refine later
            sort_by=arxiv.SortCriterion.Relevance,
        )
        papers = []
        for result in arxiv.Client().results(search):
            paper_info = {
                "title": result.title,
                "summary": result.summary,
                "authors": result.authors,
                "published": result.published,
                "arxiv_id": result.entry_id,
                "link": result.pdf_url,
            }
            papers.append(paper_info)

        def compute_relevance_score(paper):
            # Example: Weight based on keyword matches and recency (simple placeholder logic)
            keyword_matches = sum(
                1
                for keyword in topic.split()
                if keyword.lower() in paper["summary"].lower()
            )
            recency_score = 1 / (
                (current_year - paper["published"].year) + 1
            )  # Simulate recency score
            return keyword_matches * 10 + recency_score  # Combine scores

        for paper in papers:
            paper["relevance_score"] = compute_relevance_score(paper)
            # Step 3: Sort papers by relevance score and recency
        papers = sorted(papers, key=lambda x: x["relevance_score"], reverse=True)
        papers = papers[: self.max_results]

        for paper in papers:
            try:
                link = paper["link"]
                short_id = paper["arxiv_id"].split("arxiv.org/abs/")[-1]
                path = os.path.join(pdf_folder_path, f"{short_id}.pdf")
                urlretrieve(link, path)
            except Exception as e:
                print(f"Error downloading paper: {e}")

    def build_vec_store(self):
        """
        Build a RAG model for the research papers
        """
        print("Building vector store...")
        vec_store = ResearchPaperVectorStore(pdf_folder=self.pdf_folder)
        vec_store.build_vector_store()
        print("Vector store built successfully!")

    def ask(self, query: str) -> str:
        """
        Process any query related to research papers - including questions, requests for summaries,
        explanations, or study notes. Uses chain-of-thought reasoning to determine the best response.

        Args:
            query (str): The input query (question, request for summary, explanation, etc.)

        Returns:
            str: Generated response based on research papers
        """
        # First, use chain-of-thought to analyze the query and extract relevant topic
        cot_prompt = """
        Think through this step by step:
        1. What is the core topic or research area being asked about?
        2. What kind of information or analysis is being requested?
        3. What specific aspects of the topic should the literature review focus on?
        
        Provide your analysis in the following format:
        Topic: [core research topic]
        Focus: [specific aspects to focus on]
        """

        messages = [
            {"role": "system", "content": cot_prompt},
            {"role": "user", "content": query},
        ]

        analysis = self.llm.invoke(messages).content.strip()

        # Extract topic from the analysis
        topic_line = [
            line for line in analysis.split("\n") if line.startswith("Topic:")
        ][0]
        topic = topic_line.replace("Topic:", "").strip()

        # Generate comprehensive literature review
        literature_review = self.rag.generate_literature_review(
            topic=topic,
            initial_k=30,
            final_k=8,
            organization_style="chronological",
            include_metadata=False,
        )

        # Use chain-of-thought reasoning to generate the appropriate response
        synthesis_prompt = """
        You are a research expert tasked with synthesizing academic literature to provide valuable insights.
        
        Think through this step by step:
        1. Analyze the user's request carefully - are they asking for:
        - An answer to a specific question
        - A summary of research
        - An explanation of concepts
        - Study notes
        - Something else
        
        2. Consider what aspects of the literature review are most relevant
        
        3. Determine how to best structure the response to meet their needs
        
        Then provide a response that:
        - Directly addresses their request
        - Uses specific evidence and citations from the literature
        - Maintains academic rigor while being clear and accessible
        - Acknowledges any limitations in the available evidence
        - Organizes information in a way that best serves their purpose
        
        Literature Review:
        {literature_review}
        
        User Request:
        {query}
        """

        messages = [
            {
                "role": "system",
                "content": synthesis_prompt.format(
                    literature_review=literature_review, query=query
                ),
            },
            {"role": "user", "content": "Please provide your response."},
        ]

        response = self.llm.invoke(messages).content.strip()
        return response

    def get_review(self, topic: str) -> str:
        """
        Generate a literature review for a specific topic

        Args:
            topic (str): The core research topic for the literature review

        Returns:
            str: Generated literature review
        """
        literature_review, sources = self.rag.generate_literature_review(
            topic=topic,
            initial_k=30,
            final_k=8,
            organization_style="chronological",
            include_metadata=True,
        )
        return literature_review

    def get_citation(self, claim: str) -> str:
        """
        Generate a citation for a specific topic

        Args:
            topic (str): The core research topic for the citation

        Returns:
            str: Generated citation
        """
        citation, sources = self.rag.generate_citation_evidence(claim)
        return citation
