import React from "react";

const assignments = [
  {
    title: "Case Study Analysis",
    summary:
      "Analyze a case study on sustainable business practices and propose innovative solutions.",
    due: "Oct 20, 2024",
  },
  {
    title: "Marketing Presentation",
    summary:
      "Prepare a presentation on the impact of social media on modern marketing strategies.",
    due: "Oct 22, 2024",
  },
  {
    title: "AI Ethics Research Paper",
    summary:
      "Write a research paper exploring the ethical considerations in AI, focusing on bias and privacy.",
    due: "Oct 25, 2024",
  },
];

function UpcomingAssignments(){
  return (
    <div>
      <h4 className="fw-bold mb-3">Upcoming Assignments</h4>
      <ul className="list-group">
        {assignments.map((a, idx) => (
          <li key={idx} className="list-group-item">
            <p className="fw-medium mb-1">{a.title}</p>
            <p className="text-muted small mb-1">{a.summary}</p>
            <span className="text-primary small fw-bold">Due: {a.due}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default UpcomingAssignments;
