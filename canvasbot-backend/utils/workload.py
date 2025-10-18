from schemas import AssignmentResponse
from datetime import datetime
import requests
import json
def format_assignments_for_prompt(assignments: list[AssignmentResponse]):
    lines = []
    for a in assignments:
        lines.append(
            f"Course: {a.course_name}\n"
            f"Title: {a.title}\n"
            f"Due: {a.due_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Description: {a.description}\n"
            "----"
        )
    return "\n".join(lines)


def getWorkload(assignments: list[AssignmentResponse]):
    formatted = format_assignments_for_prompt(assignments)
    today = datetime.now().strftime("%B %d, %Y")
    today_iso = datetime.now().strftime("%Y-%m-%d")
    
    # First prompt: Get structured JSON analysis with action plan
    analysis_prompt = f"""
You are an academic planning assistant. Today's date is {today} ({today_iso}).

## Your Task
Analyze the provided assignment list and create:
1. A week-by-week workload breakdown
2. A detailed action plan for completing assignments on time

## Input Format
Each assignment includes:
- Course name
- Title
- Description
- Due date (YYYY-MM-DD format)

## Analysis Requirements

### Weekly Grouping
- Group assignments by week (Monday–Sunday)
- Start from this current week
- Cover the next 4–6 weeks or until all assignments are accounted for

### Action Planning
For each assignment, determine:
- When to START working on it (based on complexity and due date)
- Suggested days to work on it
- Estimated effort level (low/medium/high)
- Whether it conflicts with other assignments

## Output Format
Return ONLY a valid JSON object (no markdown, no extra text):

{{
  "summary": "2-3 sentence overview of overall workload trends",
  "current_date": "{today_iso}",
  "weekly_breakdown": [
    {{
      "week_start": "YYYY-MM-DD",
      "week_end": "YYYY-MM-DD",
      "week_number": 1,
      "num_assignments": 3,
      "intensity": "light|moderate|heavy|very heavy",
      "assignments_due": [
        {{
          "course": "Course Name",
          "title": "Assignment Title",
          "due_date": "YYYY-MM-DD",
          "description": "Brief description"
        }}
      ],
      "workload_notes": "Brief analysis of this week's workload"
    }}
  ],
  "action_plan": [
    {{
      "assignment": {{
        "course": "Course Name",
        "title": "Assignment Title",
        "due_date": "YYYY-MM-DD"
      }},
      "start_date": "YYYY-MM-DD",
      "suggested_work_days": ["YYYY-MM-DD", "YYYY-MM-DD"],
      "effort_level": "low|medium|high",
      "estimated_hours": 5,
      "priority": "high|medium|low",
      "notes": "Why start on this date, any conflicts or considerations"
    }}
  ],
  "recommendations": [
    "Strategic planning suggestions based on workload patterns"
  ]
}}

## Guidelines for Action Planning
- Start major projects 1-2 weeks before due date
- Start medium assignments 3-7 days before due date
- Start small assignments 1-3 days before due date
- Consider weekends for larger blocks of work
- Avoid scheduling too many assignments on the same day
- Flag weeks with multiple deadlines as needing early starts

## Assignments
{formatted}

Remember: Output ONLY the JSON object.
"""
    
    print("=== Analysis Prompt ===")
    print(analysis_prompt)
    
    # First API call: Get structured analysis
    analysis_response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2",
            "messages": [
                {"role": "user", "content": analysis_prompt}
            ],
            "stream": False,
            "format": "json"
        }
    )
    
    if analysis_response.status_code != 200:
        return {"error": "Failed to get analysis from Ollama", "details": analysis_response.text}
    
    # Extract JSON analysis
    analysis_content = analysis_response.json().get("message", {}).get("content", "").strip()
    
    # Clean up response (remove markdown code blocks if present)
    if analysis_content.startswith("```"):
        analysis_content = analysis_content.split("```")[1]
        if analysis_content.startswith("json"):
            analysis_content = analysis_content[4:]
        analysis_content = analysis_content.strip()
    
    print("\n=== Raw JSON Analysis ===")
    print(analysis_content)
    
    # Parse JSON
    try:
        workload_data = json.loads(analysis_content)
    except json.JSONDecodeError as e:
        return {"error": "Failed to parse JSON response", "details": str(e), "raw": analysis_content}
    
    # Second prompt: Convert JSON to human-friendly format with list structure
    formatting_prompt = f"""
You are a friendly academic advisor. Convert the following workload analysis into a clear, structured breakdown for a student.

## Workload Data (JSON):
{json.dumps(workload_data, indent=2)}

## Your Task
Create a well-organized response with these sections:

### 1. OVERVIEW
A brief 2-3 sentence summary of the workload situation.

### 2. WEEKLY BREAKDOWN
For each week, use this format:
**Week [number]: [Date Range]** - [Intensity Indicator]
- [num] assignments due this week
- Assignment 1: [Course] - [Title] (Due: [Date])
- Assignment 2: [Course] - [Title] (Due: [Date])
- Notes: [Brief workload commentary]

### 3. ACTION PLAN
For each assignment, use this format:
**[Course] - [Assignment Title]**
- Due: [Date]
- Start working: [Date]
- Priority: [High/Medium/Low]
- Estimated effort: [X hours, effort level]
- Recommended schedule:
  - [Day 1]: [What to do]
  - [Day 2]: [What to do]
  - [Day 3]: [What to do]
- Notes: [Any important considerations]

### 4. KEY RECOMMENDATIONS
List 3-5 strategic tips as bullet points.

### 5. TIPS FOR SUCCESS
A brief encouraging note with 2-3 practical tips.

## Style Guidelines
- Use clear headings and bullet points throughout
- Use intensity indicators: 🟢 Light, 🟡 Moderate, 🟠 Heavy, 🔴 Very Heavy
- Keep it scannable and easy to follow
- Be specific about dates and actions
- Focus on actionable guidance

Today's date is {today}.

Write the structured breakdown now:
"""
    
    print("\n=== Formatting Prompt ===")
    print(formatting_prompt)
    
    # Second API call: Get human-friendly format
    formatting_response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2",
            "messages": [
                {"role": "user", "content": formatting_prompt}
            ],
            "stream": False
        }
    )
    
    if formatting_response.status_code != 200:
        return {
            "error": "Failed to get formatted response from Ollama",
            "details": formatting_response.text,
            "raw_analysis": workload_data
        }
    
    # Extract formatted content
    formatted_breakdown = formatting_response.json().get("message", {}).get("content", "").strip()
    
    print("\n=== Human-Friendly Breakdown ===")
    print(formatted_breakdown)
    
    # Return both structured data and human-friendly format
    return formatted_breakdown