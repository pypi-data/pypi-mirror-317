import logging
import os
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.core.indices import VectorStoreIndex

from app.engine.context import create_service_context
from app.engine.mongo import get_mongo_store

def get_index():
    try:
        logger = logging.getLogger("uvicorn")
        logger.info("Connecting to index from MongoDB...")
        # service_context = create_service_context()
        store = get_mongo_store()
        # print('store is :: ' + str(store.db_name))
        # store = get_mongo_store()
        index = VectorStoreIndex.from_vector_store(store)
       
        logger.info("Finished connecting to index from MongoDB.")
        return index
    except Exception as e:
        logger.error(f"Error while connecting to index: {e}")
        # Handle the error as required
        return None  # Or raise the exception again if needed
    

