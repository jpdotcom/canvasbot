import React, { useEffect, useState } from "react";
import "./UpcomingAssignments.css"
import Assignment from "./Assignment";
interface Assignment {
  title: string;
  description: string;
  due_date: string;
  id: number
  user_id: number 
  course_name: string
}

function UpcomingAssignments() {
  
  const [showAll, setShowAll] = React.useState(false); // State to toggle showing all assignments

  

  //Load in assignments from local storage
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  useEffect(() => {
    const storedAssignments = localStorage.getItem("assignments");
    console.log(storedAssignments?.length);
    if (storedAssignments) {
      setAssignments(JSON.parse(storedAssignments));
    }
  }, []);

  const assignmentDueFuture = (a: Assignment) => {
    const currentDate = new Date();
    
     
     return new Date(a.due_date) >= currentDate 
     
 }


  // Format the date using Intl.DateTimeFormat
  const formatDate = (dateString: string) => {
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    return new Intl.DateTimeFormat("en-US", options).format(new Date(dateString));
  };

  // Determine which assignments to show
  const assignmentsDueThisWeek = assignments.filter(assignmentDueFuture);
  assignmentsDueThisWeek.sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime());

  const visibleAssignments = showAll ? assignmentsDueThisWeek : assignmentsDueThisWeek.slice(0, 5);
  return (
    <div>
      <h4 className="fw-bold mb-3">Upcoming Assignments</h4>
      <ul className="list-group">
        {visibleAssignments.map((a, idx) => (
            <Assignment 
            idx={idx}
            title={a.title}
            description={a.description}
            due_date={a.due_date}
            user_id={a.user_id}
            course_name={a.course_name}
            id={a.id}
          />
        ))}
      </ul>
      {/* Show All button */}
      {assignmentsDueThisWeek.length > 5 && !showAll && (
        <button
          className="btn btn-primary mt-3"
          onClick={() => setShowAll(true)}
        >
          Show All
        </button>
      )}
    </div>
  );
}

export default UpcomingAssignments;
