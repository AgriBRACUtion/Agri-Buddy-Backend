from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List, Optional

def get_chroma_retriever(collection_name: str, top_k: int = 3):
    """
    Creates a retriever for the specified Chroma collection of rice varieties.
    
    Args:
        collection_name (str): Name of the collection to retrieve from.
                              Should be one of: "Aman", "Aus", or "Boro"
        top_k (int): Number of documents to retrieve. Defaults to 3.
        
    Returns:
        A retriever object that can perform similarity search on the specified collection.
    """
    # Initialize embeddings model
    embeddings = OpenAIEmbeddings()
    
    # Connect to the existing Chroma collection
    db_path = f"database/chroma_db/chroma_dhan - {collection_name}"
    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=db_path
    )
    
    # Create retriever with similarity search
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    
    return retriever

def search_rice_varieties(query: str, variety_type: Optional[str] = None, top_k: int = 3) -> List[Document]:
    """
    Searches for rice varieties across all collections or a specific one.
    
    Args:
        query (str): The search query
        variety_type (str, optional): Specific rice variety type to search.
                                     One of: "Aman", "Aus", or "Boro". 
                                     If None, searches all varieties.
        top_k (int): Number of results to return per collection
        
    Returns:
        List[Document]: List of relevant documents
    """
    results = []
    
    if variety_type:
        # Search in specific collection
        retriever = get_chroma_retriever(variety_type, top_k)
        results = retriever.get_relevant_documents(query)
    else:
        # Search in all collections
        for rice_type in ["Aman", "Aus", "Boro"]:
            retriever = get_chroma_retriever(rice_type, top_k)
            results.extend(retriever.get_relevant_documents(query))
    
    return results




def get_diseases_retriever(top_k: int = 3) -> Retriever:
    """
    Creates a retriever for the diseases guideline collection.
    
    Args:
        top_k (int): Number of results to return
        
    Returns:
        A retriever object that can perform similarity search on the diseases collection.
    """
    # Initialize embeddings model
    embeddings = OpenAIEmbeddings()
    
    # Connect to the existing Chroma collection
    db_path = "database/chroma_db/chroma_diseases_guideline - Sheet1"
    vectorstore = Chroma(
        collection_name="diseases_guideline",
        embedding_function=embeddings,
        persist_directory=db_path
    )
    
    # Create retriever with similarity search
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    
    return retriever

def search_diseases_info(query: str, top_k: int = 3) -> List[Document]:
    """
    Searches for disease information in the diseases guideline collection.
    
    Args:
        query (str): The search query to find relevant disease information
        top_k (int): Number of results to return
        
    Returns:
        List[Document]: List of relevant documents with disease information
    """
    # Get the diseases retriever
    retriever = get_diseases_retriever(top_k)
    
    # Get relevant documents
    results = retriever.get_relevant_documents(query)
    
    # Convert disease_type names to Bangla
    for doc in results:
        # Extract the disease type from the document
        if hasattr(doc, 'metadata') and 'diseases_type' in doc.metadata:
            disease_type = doc.metadata['diseases_type']
            # Map to Bangla name based on the document content
            if "ধানের পাতা পোড়া" in doc.page_content:
                doc.metadata['diseases_type_bangla'] = "ধানের পাতা পোড়া"
            elif "ধানের পাতার লালচে রেখা" in doc.page_content:
                doc.metadata['diseases_type_bangla'] = "ধানের পাতার লালচে রেখা"
            elif "ব্যাকটেরিয়াজনিত ঝাঁকুনি" in doc.page_content:
                doc.metadata['diseases_type_bangla'] = "ব্যাকটেরিয়াজনিত ঝাঁকুনি"
            elif "ধানের ব্লাস্ট" in doc.page_content:
                doc.metadata['diseases_type_bangla'] = "ধানের ব্লাস্ট"
    
    return results


