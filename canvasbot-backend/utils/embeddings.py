import requests 
import json
def get_embeddings(text: str):


    
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    
    embedding = response.json()["embedding"]

    #turn dict_embedding into sqlAlechemy Json object

    return embedding