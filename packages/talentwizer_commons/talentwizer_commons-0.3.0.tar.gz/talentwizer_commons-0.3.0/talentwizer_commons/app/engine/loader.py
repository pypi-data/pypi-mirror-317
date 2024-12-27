import os
from llama_index.core.readers import SimpleDirectoryReader


def get_documents():
    path = r""+os.environ["DATA_DIR"]
    return SimpleDirectoryReader(path).load_data()
