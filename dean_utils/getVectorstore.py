from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from langchain_qdrant import QdrantVectorStore
import hashlib
from dean_utils.defaults import qdrant_local_url
from dean_utils.defaults import logger


"""
This code creates a hash for every chunk and checks to see if that chunk already exists in the
vector database.  This is to avoid storing the same vector twice in the database, which would
badly bias retrieval performance.
"""


def get_document_hash(doc_content):
    """Generate a unique hash for the document content."""
    return hashlib.md5(doc_content.encode()).hexdigest()

def getVectorstore(document, file_path, embedding_model, collection_name):
    # Add a unique hash to your documents
    for doc in document:
        doc.metadata['content_hash'] = get_document_hash(doc.page_content)

    client = QdrantClient(url=qdrant_local_url)

    # If the collection exists, then we need to check to see if our document is already
    # present, in which case we would not want to store it again.
    if client.collection_exists(collection_name):
        logger.info("Collection exists")
        qdrant_vectorstore = QdrantVectorStore.from_existing_collection(
            embedding=embedding_model,
            collection_name=collection_name,
            url=qdrant_local_url
        )
        
        # Check for existing documents and only add new ones
        existing_hashes = set()
        new_docs = []
        
        # Get all existing hashes
        scroll_filter = rest.Filter(
            should=[
                rest.FieldCondition(
                    key="metadata.content_hash",
                    match=rest.MatchValue(value=doc.metadata['content_hash'])
                ) for doc in document
            ]
        )
        
        scroll_results = client.scroll(
            collection_name=collection_name,
            scroll_filter=scroll_filter,
            limit=len(document)  # Adjust this if you have a large number of documents
        )
        
        existing_hashes = set(point.payload.get('metadata', {}).get('content_hash') for point in scroll_results[0])
        
        for doc in document:
            if doc.metadata['content_hash'] not in existing_hashes:
                new_docs.append(doc)
        
        if new_docs:
            qdrant_vectorstore.add_documents(new_docs)
        
        logger.info(f"Added {len(new_docs)} new documents")
        logger.info(f"Skipped {len(existing_hashes)} existing documents")
    else: 
        logger.info("Collection does not exist")                           #So we go ahead and just add the documents
        qdrant_vectorstore = QdrantVectorStore.from_documents(
            documents=document,
            embedding=embedding_model,
            collection_name=collection_name,
            url=qdrant_local_url
        )
    return qdrant_vectorstore