import React from "react";

function AssignmentSummary(){
  const countAssingmentsDueThisWeek = () => {
     const currentDate = new Date();
      const endOfWeek = new Date();
      endOfWeek.setDate(currentDate.getDate() + (7 - currentDate.getDay()));
      console.log(endOfWeek);
      const assignment = localStorage.getItem("assignments");
      if (assignment) {
        const assignments = JSON.parse(assignment);
        console.log(assignment)
        const dueThisWeek = assignments.filter((a: {title:string, due_date: string | number | Date ; }) => {
          
          const dueDate = new Date(a.due_date);
          
          const isDueThisWeek =  dueDate >= currentDate && dueDate <= endOfWeek;
          if (isDueThisWeek) {
            console.log(a.title + " is due this week");
          }
          return isDueThisWeek;
        });
        return dueThisWeek.length;
      }
      return 0;
  }
  return (
    <div className="d-flex flex-column flex-sm-row align-items-center border rounded p-3 bg-primary bg-opacity-10 gap-3">
      <div className="flex-grow-1">
        <h5 className="fw-bold">Assignments Due This Week</h5>
        <p className="text-muted mb-0">
          You have {countAssingmentsDueThisWeek()} assignments due this week. Stay on top of your coursework!
        </p>
      </div>
      <div
        className="rounded"
        style={{
          width: "160px",
          height: "100px",
          backgroundImage:
            "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBVQ6ccaXHO3lHAZoxeL_OqNzpVVI8FsvmhaFbR2ZNcEUzuMr0oAS2I7DAn4KMfMxEIRa-muaec5_w6LhpSjceVWOy4x1ZKY10KKcQk1SA00-yLkxCtEHq9G1JeSOeFKuCCSZjA0bpUClt7uDg9IZgXx4Dvt_YoedHzcTOg6i5d3Q4jcoZRkJ_KfJ5W9COBKy63UtYnEmvezObF9eZFXj0JqEZDbp1fiAh1lBztM0nofXOtdLOU6x95SCLrF6glhhV8BkE3TFvjJL4')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />
    </div>
  );
};

export default AssignmentSummary;
