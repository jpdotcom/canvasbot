import React, {useState,useEffect} from "react"
import { useParams } from "react-router-dom"
import AIAssistant from "./AIAssistant" 
import { API_URL } from "../config"
import Header from "./Header"

function AssignmentView(){

  
    const [assignment,setAssignment] = useState<any>(null)


    const [loading, setLoading] = useState(true);

    useEffect(()=>{
        const loadAssignment = async () =>{
            const stored = localStorage.getItem("selectedAssignment");
            if (stored){
                setAssignment(JSON.parse(stored))
                setLoading(false);
            }

        };
        loadAssignment();
    },[])


    if (loading){
        return <div className="container mt-5"> Loading... </div>
    }
    if (!assignment){
        return <div className="container mt-5"> Assignment not found</div>
    }

    const formatDate = (dateString: string) => {
        const options: Intl.DateTimeFormatOptions = {
          year: "numeric",
          month: "long",
          day: "numeric",
        };
        return new Intl.DateTimeFormat("en-US", options).format(new Date(dateString));
      };
    return     <>
    <Header/>
    <div className="container mt-4">
        <div className="row">
        {/* Assignment Details - Left Side */}
        <div className="col-md-8" >
            <div className="card">
            <div className="card-body">
                <h2 className="card-title fw-bold">{assignment.title}</h2>
                <p className="text-muted mb-3">
                <span className="badge bg-primary">
                    Due: {formatDate(assignment.due_date)}
                </span>
                </p>
                <hr />
                <h5 className="fw-bold mt-4">Description</h5>
                <p className="card-text">{assignment.description}</p>
                
                {/* Add more assignment details here */}
                {assignment.instructions && (
                <>
                    <h5 className="fw-bold mt-4">Instructions</h5>
                    <p>{assignment.instructions}</p>
                </>
                )}
                
                {assignment.resources && (
                <>
                    <h5 className="fw-bold mt-4">Resources</h5>
                    <ul>
                    {assignment.resources.map((resource: string, idx: number) => (
                        <li key={idx}>{resource}</li>
                    ))}
                    </ul>
                </>
                )}
            </div>
            </div>
        </div>

        {/* AI Assistant - Right Side */}
        <div className="col-auto" >
            <div className="sticky-top" style={{ top: "20px" }}>
            <AIAssistant assignmentContext={assignment} />
            </div>
        </div>
        </div>
    </div> 
    </>
   

    
   
    
}
    
export default AssignmentView;