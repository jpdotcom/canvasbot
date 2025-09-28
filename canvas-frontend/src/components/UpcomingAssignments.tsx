import React, { useEffect, useState } from "react";

interface Assignment {
  title: string;
  description: string;
  due_date: string;
}

function UpcomingAssignments() {
  const [assignments, setAssignments] = React.useState<Assignment[]>([]);
  const [showAll, setShowAll] = React.useState(false); // State to toggle showing all assignments

  const get_assignments = async () => {
    try {
      const response_user_id = await fetch(
        'http://localhost:8000/users/by_email/' + localStorage.getItem("user_email")
      );
      const user_data = await response_user_id.json();
      const user_id = user_data.id;

      const response2 = await fetch('http://localhost:8000/assignments/all/' + user_id);
      const assignments_data = await response2.json();

      setAssignments(assignments_data);
    } catch (error) {
      console.error("Error fetching assignments:", error);
    }
  };

  useEffect(() => {
    get_assignments();
  }, []);

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
  const visibleAssignments = showAll ? assignments : assignments.slice(0, 5);

  return (
    <div>
      <h4 className="fw-bold mb-3">Upcoming Assignments</h4>
      <ul className="list-group">
        {visibleAssignments.map((a, idx) => (
          <li key={idx} className="list-group-item">
            <p className="fw-medium mb-1">{a.title}</p>
            <p className="text-muted small mb-1">{a.description}</p>
            <span className="text-primary small fw-bold">Due: {formatDate(a.due_date)}</span>
          </li>
        ))}
      </ul>
      {/* Show All button */}
      {assignments.length > 5 && !showAll && (
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
