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
    
    # First prompt: Get structured JSON analysis with detailed action plan
    analysis_prompt = f"""
You are an academic planning assistant. Today's date is {today} ({today_iso}).

## Your Task
Analyze the provided assignments and create a DETAILED day-by-day action plan for completing each one.

## Analysis Requirements

### 1. Assess Each Assignment
For each assignment, determine:
- Complexity level (simple/moderate/complex) based on the description
- Estimated total hours needed
- Suggested number of work sessions
- Specific start date (not just "start early")

### 2. Create Day-by-Day Work Plans
For EACH assignment, break down the work into specific daily tasks:
- Assign specific dates for each work session
- Define what to accomplish each day
- Estimate hours for each session
- Ensure realistic daily workloads (2-4 hours per assignment per day max)

### 3. Smart Scheduling Rules
- Complex assignments: Start 7-14 days before due date, spread over multiple sessions
- Moderate assignments: Start 3-7 days before, 2-3 work sessions
- Simple assignments: Start 1-3 days before, 1-2 work sessions
- Avoid scheduling more than 2 major tasks on the same day
- Prefer starting work on weekdays (Monday-Thursday) when possible
- Leave buffers before due dates for review/revision

## Output Format
Return ONLY valid JSON (no markdown):

{{
  "summary": "Overview of workload and planning strategy",
  "current_date": "{today_iso}",
  "weekly_overview": [
    {{
      "week_start": "YYYY-MM-DD",
      "week_end": "YYYY-MM-DD",
      "total_assignments_due": 3,
      "total_work_sessions": 8,
      "intensity": "light|moderate|heavy|very heavy"
    }}
  ],
  "detailed_action_plan": [
    {{
      "assignment": {{
        "course": "Course Name",
        "title": "Assignment Title",
        "due_date": "YYYY-MM-DD"
      }},
      "complexity": "simple|moderate|complex",
      "total_estimated_hours": 6,
      "priority": "high|medium|low",
      "start_date": "YYYY-MM-DD",
      "daily_schedule": [
        {{
          "date": "YYYY-MM-DD",
          "day_name": "Monday",
          "session_number": 1,
          "estimated_hours": 2,
          "specific_tasks": [
            "Read assignment requirements carefully",
            "Research topic and gather sources",
            "Create outline or plan"
          ]
        }},
        {{
          "date": "YYYY-MM-DD",
          "day_name": "Wednesday",
          "session_number": 2,
          "estimated_hours": 2,
          "specific_tasks": [
            "Complete first draft of sections 1-2",
            "Work on main analysis or problem-solving"
          ]
        }},
        {{
          "date": "YYYY-MM-DD",
          "day_name": "Friday",
          "session_number": 3,
          "estimated_hours": 2,
          "specific_tasks": [
            "Finish remaining sections",
            "Review and edit for clarity",
            "Proofread and format",
            "Submit assignment"
          ]
        }}
      ],
      "strategic_notes": "Why this schedule works, any conflicts to watch for"
    }}
  ],
  "key_dates_summary": [
    {{
      "date": "YYYY-MM-DD",
      "workload": "Work on [Assignment 1] (2h) + [Assignment 2] (1h)",
      "total_hours": 3
    }}
  ],
  "recommendations": [
    "Specific advice for managing this workload"
  ]
}}

## Critical Instructions
1. The "daily_schedule" array must have SPECIFIC dates, not placeholders
2. Each work session must have concrete, actionable tasks
3. Break large assignments into 2-4 work sessions
4. Be realistic about time estimates
5. Account for assignment complexity in the schedule
6. Avoid overloading any single day

## Assignments
{formatted}

Remember: Output ONLY the JSON object with real dates and specific daily tasks.
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
        return f"Error: Failed to get analysis from Ollama - {analysis_response.text}"
    
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
        return f"Error: Failed to parse JSON response - {str(e)}\n\nRaw content:\n{analysis_content}"
    
    # Second prompt: Convert JSON to human-friendly format with specific daily guidance
    formatting_prompt = f"""
You are a friendly academic advisor. Convert the following detailed workload analysis into a clear, actionable guide.

## Workload Data (JSON):
{json.dumps(workload_data, indent=2)}

## Your Task
Create a student-friendly breakdown with these sections:

### 1. 📋 OVERVIEW
2-3 sentences summarizing the workload and overall strategy.

### 2. 📅 YOUR WEEKLY SCHEDULE
For each week, show:
**Week [number]: [Date Range]** [Intensity emoji]
- X assignments due | Y total work sessions planned
- Brief notes on this week's intensity

### 3. 🎯 DETAILED ACTION PLAN
For EACH assignment, use this EXACT format:

**[Course Name] - [Assignment Title]**
📌 Due: [Day, Month Date] | Priority: [High/Medium/Low] | Total Time: [X hours]

**Your Work Schedule:**
→ **[Day Name, Month Date]** (Session 1 - [X] hours)
   • [Specific task 1]
   • [Specific task 2]
   • [Specific task 3]

→ **[Day Name, Month Date]** (Session 2 - [X] hours)
   • [Specific task 1]
   • [Specific task 2]

→ **[Day Name, Month Date]** (Session 3 - [X] hours)
   • [Specific task 1]
   • [Specific task 2]

💡 Strategy: [Why this schedule works, any important notes]

---

### 4. 📆 DAY-BY-DAY CALENDAR
Show the busiest days:

**[Day Name, Month Date]:**
- 9:00 AM - 11:00 AM: Work on [Assignment 1] - [Tasks]
- 2:00 PM - 4:00 PM: Work on [Assignment 2] - [Tasks]
Total: [X] hours of focused work

**[Day Name, Month Date]:**
- [Time]: Work on [Assignment] - [Tasks]
Total: [X] hours

### 5. 💡 KEY RECOMMENDATIONS
- [Specific tip 1]
- [Specific tip 2]
- [Specific tip 3]

### 6. ✨ FINAL TIPS
Brief encouraging message with 2-3 practical tips.

## Critical Formatting Rules
- Use actual day names and dates (e.g., "Monday, October 21" not "Day 1")
- List specific tasks for each work session, not vague descriptions
- Include time estimates for every session
- Use clear visual separators (→, •, ---)
- Make it scannable with bold headings
- Use emojis sparingly for section markers only

Today's date is {today}.

Write the detailed breakdown now:
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
        return f"Error: Failed to get formatted response from Ollama - {formatting_response.text}"
    
    # Extract formatted content
    formatted_breakdown = formatting_response.json().get("message", {}).get("content", "").strip()
    
    print("\n=== Human-Friendly Breakdown ===")
    print(formatted_breakdown)
    
    return formatted_breakdown