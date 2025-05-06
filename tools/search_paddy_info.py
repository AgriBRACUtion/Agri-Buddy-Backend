from langchain_core.tools import Tool
# from core. import search_rice_varieties
from core.retriever import get_chroma_retriever
from langchain.schema import Document
from typing import List, Optional
import logging # Import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def search_rice_varieties(query: str, variety_type: Optional[str] = None, top_k: int = 3) -> List[Document]:
    """
    Searches for rice varieties across all collections or a specific one.
    
    Args:
        query (str): The search query
        variety_type (str, optional): Specific rice variety type to search.
                                     One of: "Aman/আমন", "Aus/আউস", or "Boro/বোরো". 
                                     If None, searches all varieties.
        top_k (int): Number of results to return per collection
        
    Returns:
        List[Document]: List of relevant documents
    """
    logging.info(f"Searching for query='{query}', variety_type='{variety_type}', top_k={top_k}") # Log input

    results = []
    
    if variety_type:
        # Search in specific collection
        try:
            logging.info(f"Getting retriever for collection: {variety_type}")
            retriever = get_chroma_retriever(variety_type, top_k)
            logging.info(f"Retriever obtained. Searching documents for query: '{query}'")
            results = retriever.get_relevant_documents(query)
            logging.info(f"Retrieved {len(results)} documents for '{query}' in '{variety_type}'.")
            # Log retrieved content for inspection (optional, can be verbose)
            # for i, doc in enumerate(results):
            #    logging.info(f"Doc {i+1}: {doc.page_content[:200]}...") # Log first 200 chars
        except Exception as e:
            logging.error(f"Error during retrieval from collection '{variety_type}': {e}", exc_info=True)
            results = [] # Ensure results is empty on error
    else:
        # Search in all collections
        logging.info("No variety_type specified, searching all collections.")
        for rice_type in ["Aman", "Aus", "Boro"]:
            try:
                logging.info(f"Getting retriever for collection: {rice_type}")
                retriever = get_chroma_retriever(rice_type, top_k)
                logging.info(f"Retriever obtained. Searching documents for query: '{query}' in {rice_type}")
                retrieved_docs = retriever.get_relevant_documents(query)
                results.extend(retrieved_docs)
                logging.info(f"Retrieved {len(retrieved_docs)} documents for '{query}' in '{rice_type}'.")
            except Exception as e:
                logging.error(f"Error during retrieval from collection '{rice_type}': {e}", exc_info=True)

    logging.info(f"Total documents found across all searches: {len(results)}")
    return results



paddy_info_tool = Tool(
    name="paddy_info_tool",
    func=search_rice_varieties,
    description="Retrieves detailed information about paddy which will be retrieve in {variety_type} collection. Use this tool to find information about specific rice varieties like 'BRRI dhan29', 'BRRI হাইব্রিড ধান৫', 'বিআর১০', etc., specifying the season (Aman, Aus, or Boro) if known."
)