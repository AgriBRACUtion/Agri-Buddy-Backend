from langchain_core.tools import Tool
# from core. import search_rice_varieties
from core.retriever import get_chroma_disease_retriever
from langchain.schema import Document
from typing import List, Optional
import logging  # Import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def search_rice_disease_treatment(query: str, top_k: int = 3) -> List[Document]:
    """
    Searches for rice disease treatment, prevention, cure the collection.
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return per collection
        
    Returns:
        List[Document]: List of relevant documents
    """
    logging.info(
        f"Searching for query='{query}', top_k={top_k}")  # Log input

    results = []



    # Search in all collections
    logging.info("Searching disease collections.")
    try:
        # logging.info(f"Getting retriever for collection: {rice_type}")
        retriever = get_chroma_disease_retriever(top_k)
        logging.info(
            f"Retriever obtained. Searching documents for query: '{query}' in Diseases_Treatment")
        retrieved_docs = retriever.get_relevant_documents(query)
        results.extend(retrieved_docs)
        logging.info(
            f"Retrieved {len(retrieved_docs)} documents for '{query}' in 'Diseases_Treatment'.")
    except Exception as e:
        logging.error(
            f"Error during retrieval from collection Diseases_Treatment: {e}", exc_info=True)

    logging.info(f"Total documents found across all searches: {len(results)}")
    return results


disease_treatment_tool = Tool(
    name="disease_treatment_tool",
    func=search_rice_disease_treatment,
    description="Retrieves detailed treatment and prevention information about rice disease which will be retrieve in Diseases_Treatment collection. Use this tool to find information about specific rice disease like 'brown spot', 'ধানের পাতা পোড়া রোগ', etc., specifying everything about the disease if known."
)
