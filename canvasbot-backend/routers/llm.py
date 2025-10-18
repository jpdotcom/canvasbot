from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
import db 
import schemas
import crud 
import canvas_api
from dotenv import load_dotenv 
import os 
from typing import List
from utils.extract_search_query import *
from  utils.cosine_similiarity import *
from utils.embeddings import *
from utils.answerQuery import *
from utils.workload import *
router = APIRouter(prefix='/llm', tags=["llm"])


@router.post('/semantic_search', response_model=List[int])

def semantic_search(request: schemas.SemanticSearchRequest, database: Session = Depends(db.get_db)):
    
    query = request.query
    user_id = request.user_id
    top_k = request.top_k if request.top_k else 3

    """
    Perform semantic search on assignments for a given user.

    Args:
        query (str): The search query.
        user_id (int): The ID of the user whose assignments to search.
        top_k (int): The number of top similar assignments to return. Default is 3.
        database (Session): The database session.

    Returns:
        List[int]: A list of assignment IDs that are most similar to the query.
    """
    # Retrieve all assignments for the user
    assignments = crud.get_all_assignments_by_user(user_id=user_id, db=database)
    
    if not assignments:
        raise HTTPException(status_code=404, detail="No assignments found for the user.")
    
    # Extract embeddings and assignment IDs
    embeddings = [assignment.embedding for assignment in assignments if assignment.embedding is not None]
    #assignment_ids = [assignment.id for assignment in assignments if assignment.embedding is not None]
    
    if not embeddings:
        raise HTTPException(status_code=404, detail="No embeddings found for the user's assignments.")
    
    parsed_query = extract_search_query(query);
    print(parsed_query);
    query_embedding = get_embeddings(parsed_query)
    similarities = [[assignment,cosine_similarity(query_embedding, emb)] for (assignment,emb) in zip(assignments, embeddings)]
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_similar = similarities[:top_k]
    similar_assignment_ids = [assignment.id for assignment, _ in top_similar]
    
    return similar_assignment_ids

@router.post('/generate_response',response_model = str)
def generate_response(prompt: schemas.LLMQuery):
    return answerQuery(prompt);

@router.get('/get_workload/{user_id}', response_model = str)    
def generate_workload(user_id:int, database: Session = Depends(db.get_db)):
    
    assignments=crud.get_all_current_assignments_by_user(user_id, db=database)
    
    return getWorkload(assignments)