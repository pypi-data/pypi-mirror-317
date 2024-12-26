import os
from typing import List, Dict
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
import pymupdf
from tqdm import tqdm


class ResearchPaperVectorStore:
    def __init__(
        self,
        pdf_folder: str = "research_papers",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        """
        Initialize the vector store builder

        Args:
            pdf_folder: Path to folder containing PDF files
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        pdf_folder_path = os.path.join(current_path, pdf_folder)
        self.pdf_folder = Path(pdf_folder_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize the free HuggingFace embeddings

        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        self.vector_store = None
        self.vector_store_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), f"{pdf_folder}_store"
        )
        if os.path.exists(self.vector_store_path):
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text content from a PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content
        """
        text = ""
        try:
            with pymupdf.open(pdf_path) as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            return ""
        return text

    def create_documents(self) -> List[Document]:
        """
        Create document objects from PDFs with metadata

        Returns:
            List of Document objects
        """
        documents = []

        for pdf_file in tqdm(self.pdf_folder.glob("*.pdf")):
            text = self.extract_text_from_pdf(pdf_file)
            if text:
                # Split text into chunks
                chunks = self.text_splitter.split_text(text)

                # Create Document objects with metadata
                for chunk in chunks:
                    doc = Document(
                        page_content=chunk,
                        metadata={
                            "source": pdf_file.name,
                            "filename": pdf_file.stem,
                        },
                    )
                    documents.append(doc)

                # print(f"Processed: {pdf_file.name}")

        return documents

    def build_vector_store(self) -> FAISS:
        """
        Build and save the FAISS vector store


        Returns:
            FAISS vector store object
        """
        # Create documents from PDFs
        documents = self.create_documents()

        if not documents:
            raise ValueError("No documents were processed successfully")

        # Create FAISS vector store
        print("Creating vector store...")

        with tqdm(total=len(documents), desc="Ingesting documents") as pbar:
            for d in documents:
                if self.vector_store:
                    self.vector_store.add_documents([d])
                else:
                    self.vector_store = FAISS.from_documents([d], self.embeddings)
                pbar.update(1)

        # vector_store = FAISS.from_documents(documents, self.embeddings)
        print("Vector store created successfully!")

        # Save the vector store
        print(f"Saving vector store to: {self.vector_store_path}")
        self.vector_store.save_local(self.vector_store_path)
        print(f"Vector store saved successfully!")
        return self.vector_store


class ResearchPaperSearch:
    def __init__(self, vector_store_name: str = "research_papers_store"):
        """
        Initialize the search utility

        Args:
            vector_store_name: name of the vector store file
        """
        # Initialize the same embeddings as used for creating the vector store
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        # Load the vector store
        current_path = os.path.dirname(os.path.abspath(__file__))
        vector_store_name = os.path.join(current_path, vector_store_name)
        self.vector_store = FAISS.load_local(
            vector_store_name, self.embeddings, allow_dangerous_deserialization=True
        )

    def search(self, query: str, k: int = 3) -> List[Dict]:
        """
        Search for relevant passages

        Args:
            query: Search query string
            k: Number of results to return

        Returns:
            List of dictionaries containing matched text and metadata
        """
        # Perform the similarity search
        results = self.vector_store.similarity_search_with_score(query, k=k)

        # Format the results
        formatted_results = []
        for doc, score in results:
            formatted_results.append(
                {
                    "text": doc.page_content,
                    "paper_name": doc.metadata["source"],
                    "similarity_score": float(
                        score
                    ),  # Convert numpy float to Python float for JSON serialization
                }
            )

        return formatted_results

    def pretty_print_results(self, results: List[Dict]):
        """
        Print search results in a readable format

        Args:
            results: List of search results
        """
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}")
            print("=" * 50)
            print(f"Paper: {result['paper_name']}")
            print(f"Similarity Score: {result['similarity_score']:.4f}")
            print("-" * 50)
            print("Relevant Text:")
            print(result["text"])
            print("=" * 50)


# Example usage
"""
# Build and save the vector store
pdf_folder = "research_papers"  # Replace with your PDF folder path
vector_store_builder = ResearchPaperVectorStore(pdf_folder)
vector_store = vector_store_builder.build_vector_store()

"""
