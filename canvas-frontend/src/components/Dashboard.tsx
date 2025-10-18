import React from "react";

import Header from "./Header";
import AssignmentSummary from "./AssignmentSummary";
import UpcomingAssignments from "./UpcomingAssignments";
import AIInsights from "./AIInsights";
import AIAssistant from "./AIAssistant";
import {useLocation} from 'react-router-dom';
import { useEffect } from "react";
function Dashboard() { 
    console.log("dashboard");
    const [name,setName] = React.useState(""); 
    useEffect(() => {
        const storedName = localStorage.getItem("name");
        if (storedName) {
            setName(storedName);
        }
    }, []);

  return (
    <div className="d-flex flex-column min-vh-100 bg-light text-dark">
      <Header />

      <main className="d-flex flex-grow-1 gap-4 p-4">
        <div className="flex-grow-1 d-flex flex-column gap-4">
          <h1 className="h3 fw-bold"> Welcome back {name}!</h1>

          <AssignmentSummary />
          <UpcomingAssignments />
          <AIInsights />
        </div>

        {/* <aside className="d-none d-lg-flex">
          <AIAssistant />
        </aside> */}
      </main>
    </div>
  );
};

export default Dashboard;
