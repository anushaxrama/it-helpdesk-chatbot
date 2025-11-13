"""
Knowledge base loader and vector store initialization
"""
import os
import pandas as pd
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeBaseLoader:
    """Loads IT knowledge base and creates vector store"""
    
    def __init__(
        self,
        csv_path: str = "data/it_knowledge.csv",
        persist_directory: str = "./chroma_db",
        collection_name: str = "it_helpdesk"
    ):
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        
    def load_csv(self) -> List[Document]:
        """Load knowledge base from CSV file"""
        logger.info(f"Loading knowledge base from {self.csv_path}")
        
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Knowledge base CSV not found: {self.csv_path}")
        
        df = pd.read_csv(self.csv_path)
        documents = []
        
        for idx, row in df.iterrows():
            # Create comprehensive document content
            content = f"""Category: {row['category']}
Issue: {row['issue']}
Priority: {row['priority']}

Solution:
{row['solution']}

Keywords: {row['keywords']}
"""
            
            # Create metadata for filtering and source attribution
            metadata = {
                "category": row['category'],
                "issue": row['issue'],
                "priority": row['priority'],
                "keywords": row['keywords'],
                "source": f"IT Knowledge Base - {row['category'].title()}",
                "doc_id": idx
            }
            
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)
        
        logger.info(f"Loaded {len(documents)} documents from knowledge base")
        return documents
    
    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """Create or load vector store"""
        logger.info("Creating vector store...")
        
        # Split documents if they're too long
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )
        
        split_docs = text_splitter.split_documents(documents)
        logger.info(f"Split into {len(split_docs)} chunks")
        
        # Create vector store with ChromaDB
        vector_store = Chroma.from_documents(
            documents=split_docs,
            embedding=self.embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory
        )
        
        logger.info(f"Vector store created with {len(split_docs)} chunks")
        return vector_store
    
    def load_existing_store(self) -> Chroma:
        """Load existing vector store"""
        logger.info("Loading existing vector store...")
        
        vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        return vector_store
    
    def initialize(self, force_reload: bool = False) -> Chroma:
        """Initialize vector store (load existing or create new)"""
        # Check if vector store already exists
        store_exists = os.path.exists(self.persist_directory)
        
        if store_exists and not force_reload:
            logger.info("Vector store exists, loading...")
            self.vector_store = self.load_existing_store()
        else:
            logger.info("Creating new vector store...")
            documents = self.load_csv()
            self.vector_store = self.create_vector_store(documents)
        
        return self.vector_store
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search knowledge base"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Call initialize() first.")
        
        # Perform similarity search
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
        
        return formatted_results


def get_quick_actions() -> List[Dict]:
    """Return predefined quick action buttons"""
    return [
        {
            "id": "reset_password",
            "label": "Reset Password",
            "description": "Help me reset my password",
            "category": "password",
            "icon": "🔑"
        },
        {
            "id": "wifi_help",
            "label": "Wi-Fi Issues",
            "description": "Help with Wi-Fi connection",
            "category": "networking",
            "icon": "📶"
        },
        {
            "id": "zoom_audio",
            "label": "Zoom Audio",
            "description": "Fix Zoom audio problems",
            "category": "audio_video",
            "icon": "🎤"
        },
        {
            "id": "printer_help",
            "label": "Printer Issues",
            "description": "Printer not working or not found",
            "category": "hardware",
            "icon": "🖨️"
        },
        {
            "id": "vpn_setup",
            "label": "VPN Setup",
            "description": "Help setting up VPN",
            "category": "networking",
            "icon": "🔒"
        },
        {
            "id": "slow_computer",
            "label": "Slow Computer",
            "description": "My computer is running slowly",
            "category": "troubleshooting",
            "icon": "🐌"
        },
        {
            "id": "software_install",
            "label": "Install Software",
            "description": "Help installing software",
            "category": "software",
            "icon": "💿"
        },
        {
            "id": "contact_support",
            "label": "Contact IT",
            "description": "Get IT support contact info",
            "category": "general",
            "icon": "📞"
        }
    ]


if __name__ == "__main__":
    # Test knowledge base loader
    loader = KnowledgeBaseLoader()
    vector_store = loader.initialize(force_reload=True)
    
    # Test search
    test_query = "How do I connect to Wi-Fi?"
    results = loader.search(test_query)
    
    print(f"\nTest query: {test_query}\n")
    for i, result in enumerate(results, 1):
        print(f"Result {i} (score: {result['score']:.3f}):")
        print(result['content'][:200] + "...\n")

