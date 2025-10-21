import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
interface AssignmentInfo{
    title: string;
    description: string;
    due_date: string;
    id: number
    user_id: number 
    course_name: string
    idx: number
  }

interface assignmentContextInfo{
    title: string;
    description: string;
    due_date: string;
    id: number
    user_id: number 
    course_name: string
   
}
function Assignment( data: AssignmentInfo){
    
    const title = data.title;
    const description = data.description; 
    const due_date  = data.due_date;
    const idx = data.idx;
    const id = data.id
    const user_id = data.user_id
    const course_name = data.course_name
    const [isClicked, setClick] = useState(false)
    const navigate = useNavigate()
    const openAssignment = async () => {
        setClick(true);
        
        // Store assignment data for the new page
        
        
        const assignmentContextData : assignmentContextInfo = {title,description,due_date,id,user_id,course_name};
        localStorage.setItem('selectedAssignment', JSON.stringify(assignmentContextData));
        
        // Option 1: Using React Router
        navigate(`/assignment/`);
        
        // Option 2: Using window.location (opens in same tab)
        // window.location.href = `/assignment/${id}`;
        
        // Option 3: Open in new tab
        // window.open(`/assignment/${id}`, '_blank');
        
        setClick(false);
      };
    const formatDate = (dateString: string) => {
        const options: Intl.DateTimeFormatOptions = {
          year: "numeric",
          month: "long",
          day: "numeric",
        };
        return new Intl.DateTimeFormat("en-US", options).format(new Date(dateString));
      };
    
    return           <li key={idx} className="list-group-item" onClick={openAssignment}>
    <p className="fw-medium mb-1">{title}</p>
    <p className="text-muted small mb-1">{description}</p>
    <span className="text-primary small fw-bold">Due: {formatDate(due_date)}</span>
  </li>
}

export default Assignment;