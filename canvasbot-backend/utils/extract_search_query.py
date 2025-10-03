import requests
def extract_search_query(user_message: str) -> str:
    """
    Extract the core search intent from a conversational message.
    
    Examples:
    - "what does question 3 mean about the math project" -> "question 3 math project"
    - "when is my calculus homework due?" -> "calculus homework due date"
    - "tell me about the essay assignment" -> "essay assignment"
    """
    
    extraction_prompt = f"""Extract the key search terms from this user question. 
Focus on:
- Course names (math, calculus, history, etc.)
- Assignment types (homework, project, essay, quiz, etc.)
- Specific details (question numbers, topics, etc.)
- Remove filler words like "what", "when", "tell me", "about", etc.

User question: "{user_message}"

Return ONLY the extracted search terms, nothing else."""

    # Use your LLM to extract
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",  # or whatever model you're using
            "prompt": extraction_prompt,
            "stream": False
        }
    )
    
    extracted_query = response.json()["response"].strip()
    return extracted_query