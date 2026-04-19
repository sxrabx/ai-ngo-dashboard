import os
import chromadb
from chromadb.utils import embedding_functions

# Option 2 Implemented: This uses the lightweight 'all-MiniLM-L6-v2' Sentence Transformer automatically!
emb_fn = embedding_functions.DefaultEmbeddingFunction()

# Option 3 Implemented: Persistent ChromaDB Vector Store
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'vectordb')
# Ensure path exists
os.makedirs(DB_PATH, exist_ok=True)
client = chromadb.PersistentClient(path=DB_PATH)

def init_volunteer_db(volunteers):
    """
    Creates or Updates the vector database with volunteer profiles.
    We convert their textual skills into numerical 'semantic vectors'.
    """
    collection = client.get_or_create_collection(name="volunteers", embedding_function=emb_fn)
    
    # Create the text document to be embedded (e.g. "Health, First Aid, Medical")
    documents = [", ".join(v.get('skills', ['General'])) for v in volunteers]
    ids = [str(v['id']) for v in volunteers]
    
    # Upsert ignores duplicates if they already exist with the same ID
    collection.upsert(documents=documents, ids=ids)
    
def query_semantic_match(task_description: str, n_results: int = 10):
    """
    Queries the database. Turns the task_description into a vector and finds
    the mathematical nearest neighbors (highest semantic overlap).
    """
    try:
        collection = client.get_collection(name="volunteers", embedding_function=emb_fn)
        results = collection.query(query_texts=[task_description], n_results=n_results)
        
        if not results or not results['ids']:
            return []
            
        return results['ids'][0]
    except Exception as e:
        print(f"ChromaDB Query Error: {e}")
        return []
