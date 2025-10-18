import schemas
import requests 
import json

def answerQuery(prompt: schemas.LLMQuery):
    query = prompt.query
    assignment = prompt.assignment
    assignment_desc = assignment.description 
    assignment_title = assignment.title 
    course_name = assignment.course_name  # Assuming this exists in your schema
    
    answer_prompt = f"""You are a helpful academic assistant helping a student understand their course assignment.

Assignment Information:
- Course: {course_name}
- Title: {assignment_title}
- Description: {assignment_desc}

Student's Question: {query}

Instructions:
1. Answer the student's question based ONLY on the assignment information provided above
2. Be clear, concise, and educational
3. If the question asks about specific parts (like "question 3"), reference that part specifically
4. If the assignment description doesn't contain enough information to fully answer, say so honestly
5. Provide helpful guidance without doing the work for them
6. If they're asking about due dates, requirements, or instructions, quote relevant parts from the description

Provide a helpful response:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",  # or your preferred model
                "prompt": answer_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,  # Balanced creativity and accuracy
                    "num_predict": 500   # Allow longer responses
                }
            }
        )
        if response.status_code == 200:
            print(answer_prompt);
            answer = response.json()["response"].strip()
            return answer
        else:
            return "I'm having trouble generating a response. Please try again. Error: " + response.status_code
            
    except Exception as e:
    
        return "I'm having trouble generating a response. Please try again. Error: " + str(e)